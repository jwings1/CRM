"""Deterministic audit: read the Sinergia export, rebuild each record's trail from creation onward,
check it against the reference model (rules.py), and produce the amended records.

Every finding is written to the run folder as soon as it is found (findings.jsonl), so a
partial run is still usable. Pure stdlib + rules.py.
"""
from __future__ import annotations

import csv
import io
import json
import re
import unicodedata
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from . import rules as R

FILES = ["aziende", "contatti", "opportunita", "righe_offerta", "listino", "ticket", "attivita", "utenti",
         "storico_fasi"]


# ============================================================ I/O
def read_export(src: str | Path) -> dict[str, list[dict]]:
    """Zip (any name, any folder inside) or a folder of the nine CSVs. ';' separated, CP1252."""
    src = Path(src)
    out: dict[str, list[dict]] = {}

    def _parse(name: str, raw: bytes):
        text = raw.decode("cp1252", errors="replace")
        out[name] = list(csv.DictReader(io.StringIO(text, newline=""), delimiter=";"))

    if src.is_dir():
        for f in FILES:
            p = next(src.rglob(f"{f}.csv"), None)
            if p:
                _parse(f, p.read_bytes())
    else:
        with zipfile.ZipFile(src) as z:
            for n in z.namelist():
                stem = Path(n).stem.lower()
                if stem in FILES and n.lower().endswith(".csv"):
                    _parse(stem, z.read(n))
    missing = [f for f in FILES if f not in out]
    if missing:
        raise ValueError(f"export is missing {missing}")
    return out


class Sink:
    """Append-only JSONL writer, flushed per line: results survive an interrupted run."""

    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.f = path.open("w", encoding="utf-8")
        self.n = 0

    def write(self, obj: dict):
        self.f.write(json.dumps(obj, ensure_ascii=False, default=str) + "\n")
        self.f.flush()
        self.n += 1

    def close(self):
        self.f.close()


# ============================================================ findings
SEVERITY = {"high": 3, "medium": 2, "low": 1, "info": 0}


@dataclass
class Audit:
    run_dir: Path
    owner_policy: str = "empty"
    findings: Sink = None
    counts: Counter = field(default_factory=Counter)
    judgment: list = field(default_factory=list)    # items handed to the agent

    def __post_init__(self):
        self.findings = Sink(self.run_dir / "findings.deterministic.jsonl")

    def flag(self, code: str, entity: str, id_legacy: str, severity: str, message: str, *,
             fix: dict | None = None, evidence: dict | None = None, judgment: bool = False):
        rec = {"source": "rule", "code": code, "entity": entity, "id_legacy": id_legacy, "severity": severity,
               "message": message}
        if fix:
            rec["fix"] = fix            # {field, old, new, confidence}
        if evidence:
            rec["evidence"] = evidence
        if judgment:
            rec["needs_judgment"] = True
            self.judgment.append(rec)
        self.findings.write(rec)
        self.counts[code] += 1


def cd_raw_or(r: dict) -> str | None:
    return (r.get("data_chiusura") or "").strip() or None


def _txt(v):  # trimmed + mojibake-repaired
    return R.fix_text(v or "")


def _ts(d: datetime | None) -> str | None:
    return d.isoformat(sep=" ") if d else None


def _norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\b(s\.?\s?p\.?\s?a|s\.?\s?r\.?\s?l\.?\s?s?|s\.?\s?n\.?\s?c|s\.?\s?a\.?\s?s)\.?\b", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


class UnionFind:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def _merge_rows(rows: list[dict], fields: list[str], order_key) -> tuple[dict, dict]:
    """[RICHIESTE all] survivor = most recently modified row; each field = most recent row that filled it.
    Returns (merged, conflicts {field: [distinct non-empty values]})."""
    rows = sorted(rows, key=order_key, reverse=True)
    merged, conflicts = {}, {}
    for f in fields:
        vals = [r[f] for r in rows if r.get(f) not in (None, "")]
        merged[f] = vals[0] if vals else ""
        distinct = list(dict.fromkeys(str(v).lower() for v in vals))
        if len(distinct) > 1:
            conflicts[f] = list(dict.fromkeys(vals))
    return merged, conflicts


# ============================================================ the audit
def run(export: dict[str, list[dict]], run_dir: Path, owner_policy: str = "empty") -> dict:
    A = Audit(run_dir, owner_policy)
    trails = {k: Sink(run_dir / "trails" / f"{k}.jsonl") for k in ("users", "companies", "contacts", "deals", "products", "tickets")}
    clean: dict[str, list[dict]] = {}

    # ---------------------------------------------------------- users
    users = {}
    for u in export["utenti"]:
        uid = u["id_utente"].strip()
        users[uid] = {"id": uid, "nome": _txt(u["nome"]), "cognome": _txt(u["cognome"]),
                      "email": (u["email"] or "").strip().lower(), "ruolo": _txt(u["ruolo"]),
                      "responsabile": (u["responsabile"] or "").strip() or None,
                      "attivo": R.is_active_user(u["attivo"])}

    def manager_chain(uid):
        seen, cur = set(), users.get(uid, {}).get("responsabile")
        while cur and cur not in seen:
            seen.add(cur)
            if users.get(cur, {}).get("attivo"):
                return cur
            cur = users.get(cur, {}).get("responsabile")
        return None

    for u in users.values():
        u["successore"] = None if u["attivo"] else manager_chain(u["id"])
        trails["users"].write(u)
        if not u["attivo"]:
            A.flag("US-INACTIVE", "users", u["id"], "info", f"{u['email']} has left; follows nothing (R3)",
                   evidence={"manager_chain_successor": u["successore"]})
    clean["users"] = list(users.values())

    def _ascii(s):
        return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))

    name_idx = defaultdict(set)
    for u in users.values():
        n, c = _ascii(u["nome"]), _ascii(u["cognome"])
        for key in (f"{n} {c}", f"{c} {n}", f"{c} {n[:1]}", f"{n[:1]} {c}"):
            name_idx[re.sub(r"[^a-z ]", "", key).strip()].add(u["id"])

    def resolve_user(raw: str) -> tuple[str | None, str]:
        """returns (user id or None, how)"""
        s = (raw or "").strip()
        if not s:
            return None, "empty"
        if s.upper() in users:
            return s.upper(), "code"
        key = re.sub(r"[^a-z ]", "", _ascii(s).replace(".", " ")).strip()
        key = re.sub(r"\s+", " ", key)
        hits = name_idx.get(key, set())
        if len(hits) == 1:
            return next(iter(hits)), "name"
        return None, "ambiguous" if hits else "unknown"

    def owner_out(uid: str | None, entity: str, idl: str, code_prefix: str) -> str | None:
        """[RICHIESTE R3] only people who work here today follow deals and tickets."""
        if not uid:
            return None
        u = users[uid]
        if u["attivo"]:
            return u["email"]
        succ = u["successore"]
        new = users[succ]["email"] if (A.owner_policy == "manager" and succ) else None
        A.flag(f"{code_prefix}-OWNER-INACTIVE", entity, idl, "medium",
               f"followed by {u['email']}, who has left",
               fix={"field": "owner", "old": u["email"], "new": new, "confidence": "high",
                    "alternative": users[succ]["email"] if succ else None,
                    "policy": A.owner_policy})
        return new

    # ---------------------------------------------------------- companies  [R1, R7]
    raw_co = []
    for r in export["aziende"]:
        idl = r["id_azienda"].strip()
        if R.is_deleted(r["cancellato"]):
            A.flag("GEN-DELETED", "companies", idl, "info", "marked deleted in Sinergia: not migrated")
            continue
        if R.has_mojibake(r["ragione_sociale"]):
            A.flag("GEN-MOJIBAKE", "companies", idl, "low", "broken accents repaired",
                   fix={"field": "name", "old": r["ragione_sociale"], "new": _txt(r["ragione_sociale"]), "confidence": "high"})
        d = R.domain(r["sito_web"])
        if (r["sito_web"] or "").strip() and not d:
            A.flag("CO-BAD-DOMAIN", "companies", idl, "low", "website is not a domain",
                   fix={"field": "domain", "old": r["sito_web"], "new": None, "confidence": "high"})
        raw_co.append({"id_legacy": idl, "name": _txt(r["ragione_sociale"]), "domain": d, "city": _txt(r["citta"]),
                       "state": _txt(r["provincia"]).upper(), "partita_iva": R.piva_from_note(r["note"]),
                       "note": _txt(r["note"]), "um": R.parse_dt(r["ultima_modifica"]), "raw_site": r["sito_web"]})

    uf = UnionFind()
    by_dom, by_piva = defaultdict(list), defaultdict(list)
    for c in raw_co:
        uf.find(c["id_legacy"])
        if c["domain"]:
            by_dom[c["domain"]].append(c["id_legacy"])
        if c["partita_iva"]:
            by_piva[c["partita_iva"]].append(c["id_legacy"])
    for grp in list(by_dom.values()) + list(by_piva.values()):
        for x in grp[1:]:
            uf.union(grp[0], x)
    groups = defaultdict(list)
    co_by_id = {c["id_legacy"]: c for c in raw_co}
    for c in raw_co:
        groups[uf.find(c["id_legacy"])].append(c)

    company_map = {}          # any legacy id (alive) -> survivor legacy id
    companies = {}
    order = lambda c: (c["um"] or datetime.min, c["id_legacy"])
    for grp in groups.values():
        merged, conflicts = _merge_rows(grp, ["id_legacy", "name", "domain", "city", "state", "partita_iva", "note"], order)
        surv = max(grp, key=order)["id_legacy"]
        merged["id_legacy"] = surv
        doms = list(dict.fromkeys(c["domain"] for c in sorted(grp, key=order, reverse=True) if c["domain"]))
        merged["domain"] = doms[0] if doms else None
        merged["additional_domains"] = doms[1:]
        merged["merged_from"] = sorted(c["id_legacy"] for c in grp if c["id_legacy"] != surv)
        for c in grp:
            company_map[c["id_legacy"]] = surv
        if len(grp) > 1:
            why = sorted({"domain" if c["domain"] and c["domain"] in doms else "partita_iva" for c in grp})
            for c in grp:
                if c["id_legacy"] != surv:
                    A.flag("CO-DUPLICATE", "companies", c["id_legacy"], "medium",
                           f"same company as {surv} (same {'/'.join(why)}): merged",
                           fix={"field": "merge_into", "old": c["id_legacy"], "new": surv, "confidence": "high"})
            if "partita_iva" in conflicts:
                A.flag("CO-PIVA-CONFLICT", "companies", surv, "high",
                       "merged rows carry different VAT numbers", evidence={"values": conflicts["partita_iva"],
                       "rows": [c["id_legacy"] for c in grp]}, judgment=True)
            if "name" in conflicts and len({_norm_name(n) for n in conflicts["name"]}) > 1:
                A.flag("CO-NAME-CONFLICT", "companies", surv, "medium",
                       "rows merged by domain/VAT have different names",
                       evidence={"names": conflicts["name"], "domains": doms}, judgment=True)
        companies[surv] = merged
        trails["companies"].write({"id_legacy": surv, "versions": [
            {"id_legacy": c["id_legacy"], "ultima_modifica": _ts(c["um"]), "name": c["name"], "domain": c["domain"],
             "partita_iva": c["partita_iva"], "city": c["city"]} for c in sorted(grp, key=order)],
            "result": {k: merged[k] for k in ("name", "domain", "additional_domains", "partita_iva", "city", "state")}})

    clean["companies"] = list(companies.values())

    def ref_company(raw: str, entity: str, idl: str, prefix: str) -> str | None:
        x = (raw or "").strip()
        if not x:
            return None
        if x in company_map:
            s = company_map[x]
            if s != x:
                A.counts[f"{prefix}-COMPANY-REMAPPED"] += 1
            return s
        A.flag(f"{prefix}-COMPANY-GONE", entity, idl, "low", f"company {x} is deleted or missing: reference cleared",
               fix={"field": "id_azienda", "old": x, "new": None, "confidence": "high"})
        return None

    # ---------------------------------------------------------- contacts  [R2]
    raw_ct = []
    for r in export["contatti"]:
        idl = r["id_contatto"].strip()
        if R.is_deleted(r["cancellato"]):
            A.flag("GEN-DELETED", "contacts", idl, "info", "marked deleted in Sinergia: not migrated")
            continue
        for f in ("nome", "cognome"):
            if R.has_mojibake(r[f]):
                A.flag("GEN-MOJIBAKE", "contacts", idl, "low", "broken accents repaired",
                       fix={"field": f, "old": r[f], "new": _txt(r[f]), "confidence": "high"})
        em = R.email(r["email"])
        if (r["email"] or "").strip() and not em:
            A.flag("CT-INVALID-EMAIL", "contacts", idl, "low", "not a valid email: treated as absent (R2)",
                   fix={"field": "email", "old": r["email"], "new": None, "confidence": "high"})
        lc = R.lifecycle(r["tipo"])
        if (r["tipo"] or "").strip() and not lc:
            A.flag("CT-LIFECYCLE-UNKNOWN", "contacts", idl, "medium", f"unknown relationship stage {r['tipo']!r}")
        raw_ct.append({"id_legacy": idl, "firstname": _txt(r["nome"]), "lastname": _txt(r["cognome"]), "email": em,
                       "phone": (r["telefono"] or "").strip(), "company_raw": (r["id_azienda"] or "").strip(),
                       "lifecyclestage": lc, "um": R.parse_dt(r["ultima_modifica"])})
    ct_groups = defaultdict(list)
    for c in raw_ct:
        ct_groups[c["email"] or f"__solo__{c['id_legacy']}"].append(c)
    contact_map, contacts = {}, {}
    for key, grp in ct_groups.items():
        order_c = lambda c: (c["um"] or datetime.min, c["id_legacy"])
        merged, conflicts = _merge_rows(grp, ["firstname", "lastname", "email", "phone", "company_raw", "lifecyclestage"], order_c)
        surv = max(grp, key=order_c)["id_legacy"]
        merged["id_legacy"] = surv
        merged["merged_from"] = sorted(c["id_legacy"] for c in grp if c["id_legacy"] != surv)
        for c in grp:
            contact_map[c["id_legacy"]] = surv
        if len(grp) > 1:
            for c in grp:
                if c["id_legacy"] != surv:
                    A.flag("CT-DUPLICATE", "contacts", c["id_legacy"], "medium", f"same email as {surv}: merged",
                           fix={"field": "merge_into", "old": c["id_legacy"], "new": surv, "confidence": "high"})
            real = {f: v for f, v in conflicts.items() if f in ("firstname", "lastname", "company_raw")}
            if real:
                A.flag("CT-MERGE-CONFLICT", "contacts", surv, "medium",
                       "rows with the same email disagree on " + ", ".join(real), evidence=real,
                       judgment="firstname" in real or "lastname" in real)
        merged["company"] = ref_company(merged.pop("company_raw"), "contacts", surv, "CT")
        contacts[surv] = merged
        if len(grp) > 1:
            trails["contacts"].write({"id_legacy": surv, "versions": [
                {"id_legacy": c["id_legacy"], "ultima_modifica": _ts(c["um"]), "name": f"{c['firstname']} {c['lastname']}",
                 "company": c["company_raw"], "stage": c["lifecyclestage"]} for c in sorted(grp, key=order_c)]})
    clean["contacts"] = list(contacts.values())

    # same name + same city, no shared domain/VAT, not merged -> the agent decides (with contact email domains)
    mail_doms = defaultdict(Counter)
    for c in contacts.values():
        if c["company"] and c["email"]:
            mail_doms[c["company"]][c["email"].split("@")[1]] += 1
    by_name = defaultdict(list)
    for c in companies.values():
        by_name[(_norm_name(c["name"]), c["city"].lower())].append(c)
    for (nm, city), grp in by_name.items():
        if len(grp) > 1 and nm:
            ids = sorted(c["id_legacy"] for c in grp)
            A.flag("CO-NAME-DUP-CANDIDATE", "companies", ids[0], "medium",
                   f"{len(grp)} companies share name and city but not domain/VAT",
                   evidence={"candidates": [{**{k: c[k] for k in ("id_legacy", "name", "domain", "partita_iva", "city", "state")},
                                             "contact_email_domains": dict(mail_doms[c["id_legacy"]].most_common(3))}
                                            for c in grp]},
                   judgment=True)

    def ref_contact(raw: str) -> str | None:
        return contact_map.get((raw or "").strip())

    # ---------------------------------------------------------- products  [R4]
    prods = defaultdict(list)
    for r in export["listino"]:
        code = R.sku(r["codice_articolo"])
        if R.is_deleted(r["cancellato"]):
            A.flag("GEN-DELETED", "products", r["codice_articolo"].strip(), "info", "marked deleted: not migrated")
            continue
        prods[code].append({"raw": r["codice_articolo"], "name": _txt(r["descrizione"]), "unit": _txt(r["unita"]),
                            "price": R.parse_number(r["prezzo_listino"]), "um": R.parse_dt(r["ultima_modifica"])})
    products = {}
    for code, grp in prods.items():
        grp.sort(key=lambda p: p["um"] or datetime.min)
        last = grp[-1]
        products[code] = {"sku": code, "name": last["name"], "price": R.money(last["price"]), "unit": last["unit"]}
        trails["products"].write({"sku": code, "prices": [{"ultima_modifica": _ts(p["um"]), "price": R.money(p["price"]),
                                                          "raw_code": p["raw"].strip()} for p in grp]})
        if len(grp) > 1:
            A.flag("PR-REPUBLISHED", "products", code, "info",
                   f"published {len(grp)} times; latest price {R.money(last['price'])} kept",
                   evidence={"prices": [R.money(p["price"]) for p in grp]})
    clean["products"] = list(products.values())

    # ---------------------------------------------------------- stage history  [DATA invariants]
    hist = defaultdict(list)
    for h in export["storico_fasi"]:
        hist[h["id_opportunita"].strip()].append({
            "ts": R.parse_dt(h["data_cambio"]), "from": R.stage(h["fase_precedente"]), "to": R.stage(h["fase_nuova"]),
            "raw_to": h["fase_nuova"], "by": h["id_utente"].strip()})

    # ---------------------------------------------------------- line items  [R4]
    lines_by_deal = defaultdict(list)
    for r in export["righe_offerta"]:
        lines_by_deal[r["id_opportunita"].strip()].append(r)

    # ---------------------------------------------------------- activities index (for deal trails)
    act_by_deal = defaultdict(list)

    # ---------------------------------------------------------- deals  [R3]
    deals, deal_ids = {}, set()
    for r in export["opportunita"]:
        idl = r["id_opportunita"].strip()
        if R.is_deleted(r["cancellato"]):
            A.flag("GEN-DELETED", "deals", idl, "info", "marked deleted in Sinergia: not migrated")
            continue
        deal_ids.add(idl)
    for r in export["attivita"]:
        o = (r["id_opportunita"] or "").strip()
        if o in deal_ids and not R.is_deleted(r["cancellato"]):
            act_by_deal[o].append(r)

    line_items = []
    for r in export["opportunita"]:
        idl = r["id_opportunita"].strip()
        if idl not in deal_ids:
            continue
        flags = []
        title = _txt(r["titolo"])
        st = R.stage(r["fase"])
        if not st:
            A.flag("DL-STAGE-UNKNOWN", "deals", idl, "high", f"stage {r['fase']!r} not in the appendix")
        pipe = R.pipeline(r["pipeline"], st)
        if not (r["pipeline"] or "").strip():
            A.flag("DL-PIPELINE-MISSING", "deals", idl, "low", f"no pipeline: {pipe} (from the stage family)",
                   fix={"field": "pipeline", "old": "", "new": pipe, "confidence": "high"})
            flags.append("DL-PIPELINE-MISSING")
        if st and (st[0] == "R") != (pipe == "Rinnovi"):
            A.flag("DL-PIPELINE-STAGE-MISMATCH", "deals", idl, "high", f"stage {st} is not a {pipe} stage", judgment=True)
            flags.append("DL-PIPELINE-STAGE-MISMATCH")

        # --- trail
        h = sorted(hist.get(idl, []), key=lambda e: (e["ts"] or datetime.min))
        um = R.parse_dt(r["ultima_modifica"])
        created = h[0]["ts"] if h else None
        if not h:
            A.flag("DL-NO-HISTORY", "deals", idl, "high", "no stage history at all", judgment=True)
            flags.append("DL-NO-HISTORY")
        else:
            if h[0]["from"] is not None or h[0]["to"] not in ("V01", "R1"):
                A.flag("DL-TRAIL-BAD-CREATION", "deals", idl, "medium",
                       f"first history row is {h[0]['from']}->{h[0]['to']}, not a creation in 01/R1")
                flags.append("DL-TRAIL-BAD-CREATION")
            for a, b in zip(h, h[1:]):
                if b["from"] != a["to"]:
                    A.flag("DL-TRAIL-BROKEN-CHAIN", "deals", idl, "medium",
                           f"row at {_ts(b['ts'])} starts from {b['from']} but previous row ended in {a['to']}")
                    flags.append("DL-TRAIL-BROKEN-CHAIN")
                if a["to"] in R.CLOSED:
                    A.flag("DL-TRAIL-REOPENED", "deals", idl, "high", f"moved {a['to']}->{b['to']} after closing",
                           judgment=True)
                    flags.append("DL-TRAIL-REOPENED")
                elif R.ORDER.get(b["to"], 0) < R.ORDER.get(a["to"], 0):
                    A.flag("DL-TRAIL-BACKWARD", "deals", idl, "medium", f"moved backwards {a['to']}->{b['to']}")
                    flags.append("DL-TRAIL-BACKWARD")
                if a["ts"] and b["ts"]:
                    gap = (b["ts"] - a["ts"]).days
                    if not (R.GAP_MIN_DAYS <= gap <= R.GAP_MAX_DAYS):
                        A.flag("DL-TRAIL-GAP", "deals", idl, "low", f"{gap} days between stage changes")
                        flags.append("DL-TRAIL-GAP")
                if (a["to"] or "")[:1] != (b["to"] or "")[:1]:
                    A.flag("DL-TRAIL-MIXED-PIPELINES", "deals", idl, "high", f"{a['to']}->{b['to']} crosses pipelines",
                           judgment=True)
                    flags.append("DL-TRAIL-MIXED-PIPELINES")
            if um and h[-1]["ts"] and h[-1]["ts"] > um:
                A.flag("DL-TRAIL-AFTER-LASTMOD", "deals", idl, "medium", "stage changed after the record's last modification")
                flags.append("DL-TRAIL-AFTER-LASTMOD")
            last = h[-1]["to"]
            if st and last != st:
                if R.ORDER.get(st, 0) > R.ORDER.get(last, 0) and st not in R.CLOSED:
                    A.flag("DL-STAGE-AHEAD-OF-TRAIL", "deals", idl, "medium",
                           f"deal is in {st} but history stops at {last}: {R.ORDER[st] - R.ORDER[last]} change(s) unrecorded",
                           evidence={"history_last": last, "deal_stage": st, "last_change": _ts(h[-1]["ts"]),
                                     "ultima_modifica": _ts(um)})
                else:
                    A.flag("DL-STAGE-CONTRADICTS-TRAIL", "deals", idl, "high",
                           f"deal is in {st} but history ends in {last}", judgment=True,
                           evidence={"history": [(e["to"], _ts(e["ts"])) for e in h]})
                flags.append("DL-STAGE-VS-TRAIL")

        if st and st not in R.CLOSED and h and h[-1]["ts"] and (R.EXPORT_DATE - h[-1]["ts"]).days > 365:
            A.flag("DL-STALE-OPEN", "deals", idl, "low",
                   f"open in {st}, no stage change since {h[-1]['ts'].date()} "
                   f"({(R.EXPORT_DATE - h[-1]['ts']).days // 365} years): close or requalify before migrating",
                   evidence={"last_change": _ts(h[-1]["ts"]), "close_date": cd_raw_or(r)})
            # not added to the trail flags: the agent already judged these trails (cache stays valid)

        # --- close date  [DATA closedate_is_closing_day]
        cd_raw = (r["data_chiusura"] or "").strip()
        cd = R.parse_dt(cd_raw)
        if cd_raw and not cd:
            A.flag("DL-CLOSEDATE-UNPARSED", "deals", idl, "medium", f"close date {cd_raw!r} unreadable", judgment=True)
        closing = next((e for e in reversed(h) if e["to"] in R.CLOSED), None)
        if st in R.CLOSED:
            if closing and not cd:
                cd = closing["ts"].replace(hour=0, minute=0, second=0)
                A.flag("DL-CLOSEDATE-MISSING", "deals", idl, "medium",
                       "closed without a close date: taken from the day it was closed in the history",
                       fix={"field": "closedate", "old": cd_raw, "new": cd.date().isoformat(), "confidence": "high"})
                flags.append("DL-CLOSEDATE-MISSING")
            elif closing and cd and cd.date() != closing["ts"].date():
                A.flag("DL-CLOSEDATE-MISMATCH", "deals", idl, "medium",
                       f"close date {cd.date()} but closed in the history on {closing['ts'].date()}",
                       fix={"field": "closedate", "old": cd_raw, "new": closing["ts"].date().isoformat(),
                            "confidence": "medium"}, judgment=True)
                flags.append("DL-CLOSEDATE-MISMATCH")
            elif not cd:
                A.flag("DL-CLOSEDATE-UNKNOWN", "deals", idl, "medium", "closed, no close date, no closing row")
        if cd and created and cd.date() < created.date():
            A.flag("DL-CLOSEDATE-BEFORE-CREATION", "deals", idl, "high", f"closes {cd.date()} before it was created {created.date()}",
                   judgment=True)
            flags.append("DL-CLOSEDATE-BEFORE-CREATION")
        if cd and cd > R.EXPORT_DATE and st in R.CLOSED:
            A.flag("DL-CLOSEDATE-FUTURE", "deals", idl, "high", f"closed in the future ({cd.date()})", judgment=True)

        # --- amount & currency  [R3]
        raw_amt = r["importo"]
        amt = R.parse_number(raw_amt)
        if (raw_amt or "").strip() and amt is None:
            A.flag("DL-AMOUNT-UNPARSED", "deals", idl, "high", f"amount {raw_amt!r} unreadable", judgment=True)
        cur = R.currency(r["valuta"], raw_amt) if amt is not None else None
        if amt is not None and R.currency_conflict(r["valuta"], raw_amt):
            A.flag("DL-CURRENCY-CONFLICT", "deals", idl, "high", f"valuta {r['valuta']!r} vs amount {raw_amt!r}",
                   judgment=True)
        if amt is not None and R.is_shorthand(raw_amt):
            A.flag("DL-AMOUNT-SHORTHAND", "deals", idl, "low", f"amount written as shorthand {raw_amt!r}",
                   fix={"field": "amount", "old": raw_amt, "new": R.money(amt), "confidence": "high"})
            flags.append("DL-AMOUNT-SHORTHAND")
        if amt is not None and R.is_monthly(raw_amt):
            new = amt * 12
            A.flag("DL-MONTHLY-AMOUNT", "deals", idl, "medium", "monthly amount: renewals are annual (R3) -> x12",
                   fix={"field": "amount", "old": raw_amt, "new": R.money(new), "confidence": "high"})
            amt = new
            flags.append("DL-MONTHLY-AMOUNT")
        credit = R.is_credit_note(title)
        if credit and amt is not None and amt > 0:
            A.flag("DL-CREDIT-POSITIVE", "deals", idl, "medium", "credit note/reversal with a positive amount -> negative",
                   fix={"field": "amount", "old": raw_amt, "new": R.money(-amt), "confidence": "medium"})
            amt = -amt
            flags.append("DL-CREDIT-POSITIVE")
        if not credit and amt is not None and amt < 0:
            A.flag("DL-NEGATIVE-NOT-CREDIT", "deals", idl, "high", "negative amount on a deal that is not a credit note",
                   evidence={"title": title, "amount": raw_amt}, judgment=True)
            flags.append("DL-NEGATIVE-NOT-CREDIT")

        # --- line items: the deal is worth the total of its lines  [R4]
        lines_total = None
        rows = lines_by_deal.get(idl, [])
        if rows:
            lines_total = Decimal("0")
            for lr in rows:
                code = R.sku(lr["codice_articolo"])
                q = R.quantity(lr["quantita"]) or Decimal("0")
                pr = R.parse_number(lr["prezzo_unitario"])
                prod = products.get(code)
                lid = lr["id_riga"].strip()
                if pr is None:
                    if prod and prod["price"]:
                        pr = Decimal(prod["price"])
                        A.flag("LI-PRICE-FROM-LIST", "line_items", lid, "low", "no unit price: list price used",
                               fix={"field": "price", "old": lr["prezzo_unitario"], "new": prod["price"], "confidence": "medium"})
                    else:
                        A.flag("LI-PRICE-MISSING", "line_items", lid, "medium", "no unit price and no list price")
                        pr = Decimal("0")
                disc = R.discount_pct(lr["sconto"])
                desc = _txt(lr["descrizione"]) or (prod["name"] if prod else "")
                if not code or not prod:
                    A.flag("LI-SKU-UNKNOWN", "line_items", lid, "low", f"article {lr['codice_articolo']!r} not in the price list")
                tot = R.line_total(q, pr, disc)
                lines_total += tot
                line_items.append({"id_legacy": lid, "deal": idl, "sku": code if prod else None, "name": desc,
                                   "quantity": str(q.normalize()) if q == q.to_integral() else str(q),
                                   "price": R.money(pr), "hs_discount_percentage": str(disc.normalize()),
                                   "total": R.money(tot)})
            if amt is None or abs(amt - lines_total) > Decimal("0.01"):
                A.flag("DL-AMOUNT-VS-LINES", "deals", idl, "medium",
                       "amount differs from the total of its quote lines (R3: lines win)",
                       fix={"field": "amount", "old": raw_amt, "new": R.money(lines_total), "confidence": "high"})
                flags.append("DL-AMOUNT-VS-LINES")
            amt, cur = lines_total, "EUR"

        # --- references
        comp = ref_company(r["id_azienda"], "deals", idl, "DL")
        cids, seen = [], set()
        for c in R.split_ids(r["contatti"]):
            s = ref_contact(c)
            if not s:
                A.flag("DL-CONTACT-GONE", "deals", idl, "low", f"contact {c} deleted or missing: dropped",
                       fix={"field": "contatti", "old": c, "new": None, "confidence": "high"})
            elif s in seen:
                A.counts["DL-CONTACT-DEDUP"] += 1
            else:
                seen.add(s)
                cids.append(s)

        # --- owner  [R3]
        uid, how = resolve_user(r["id_commerciale"])
        actors = [e["by"] for e in h if e["by"] in users]
        if how in ("empty", "unknown", "ambiguous"):
            cand = Counter(actors).most_common(1)
            if cand:
                uid = cand[0][0]
                A.flag("DL-OWNER-FROM-TRAIL", "deals", idl, "medium",
                       f"owner {r['id_commerciale']!r} not a user code: the stage history is by {uid}",
                       fix={"field": "commerciale", "old": r["id_commerciale"], "new": users[uid]["email"],
                            "confidence": "high" if len(set(actors)) == 1 else "medium"})
                flags.append("DL-OWNER-FROM-TRAIL")
            elif how != "empty":
                A.flag("DL-OWNER-UNRESOLVED", "deals", idl, "medium", f"owner {r['id_commerciale']!r} unresolved",
                       judgment=True)
        elif how == "name":
            A.flag("DL-OWNER-BY-NAME", "deals", idl, "low", f"owner written as a name {r['id_commerciale']!r} -> {uid}",
                   fix={"field": "commerciale", "old": r["id_commerciale"], "new": users[uid]["email"], "confidence": "high"})
        owner = owner_out(uid, "deals", idl, "DL")

        acts = act_by_deal.get(idl, [])
        adates = sorted(d for d in (R.parse_dt(a["data"]) for a in acts) if d)
        deal = {"id_legacy": idl, "dealname": title, "pipeline": pipe, "stage": st, "amount": R.money(amt) if amt is not None else None,
                "deal_currency_code": cur if amt is not None else None, "closedate": cd.date().isoformat() if cd else None,
                "commerciale": owner, "commerciale_originale": users[uid]["email"] if uid else None,
                "company": comp, "contacts": cids, "is_credit_note": credit, "created": _ts(created),
                "ultima_modifica": _ts(um)}
        deals[idl] = deal
        trails["deals"].write({
            "id_legacy": idl, "title": title, "pipeline": pipe, "stage": st, "owner": deal["commerciale_originale"],
            "owner_active": bool(uid and users[uid]["attivo"]), "amount": deal["amount"], "currency": deal["deal_currency_code"],
            "raw_amount": raw_amt, "credit_note": credit, "close_date": deal["closedate"], "created": _ts(created),
            "last_modified": _ts(um), "lines": len(rows), "lines_total": R.money(lines_total) if lines_total is not None else None,
            "events": [{"ts": _ts(e["ts"]), "from": e["from"], "to": e["to"], "by": e["by"]} for e in h],
            "activities": {"n": len(acts), "first": _ts(adates[0]) if adates else None, "last": _ts(adates[-1]) if adates else None,
                           "types": dict(Counter(R.activity_type(a["tipo"]) for a in acts))},
            "flags": sorted(set(flags))})
    clean["deals"] = list(deals.values())
    # line items of deals that are not migrated
    for o, rows in lines_by_deal.items():
        if o not in deals:
            for lr in rows:
                A.flag("LI-DEAL-DROPPED", "line_items", lr["id_riga"].strip(), "info",
                       f"deal {o} is deleted or missing: line not migrated (R4)")
    clean["line_items"] = line_items

    # ---------------------------------------------------------- tickets  [R5]
    tickets = []
    for r in export["ticket"]:
        idl = r["id_ticket"].strip()
        if R.is_deleted(r["cancellato"]):
            A.flag("GEN-DELETED", "tickets", idl, "info", "marked deleted in Sinergia: not migrated")
            continue
        for f in ("oggetto", "descrizione"):
            if R.has_mojibake(r[f]):
                A.flag("GEN-MOJIBAKE", "tickets", idl, "low", "broken accents repaired",
                       fix={"field": f, "old": r[f][:80], "new": _txt(r[f])[:80], "confidence": "high"})
        stg = R.ticket_stage(r["stato"])
        if not stg:
            A.flag("TK-STATUS-UNKNOWN", "tickets", idl, "medium", f"status {r['stato']!r} unknown", judgment=True)
        pr = R.priority(r["priorita"])
        if (r["priorita"] or "").strip() and not pr:
            A.flag("TK-PRIORITY-UNKNOWN", "tickets", idl, "low", f"priority {r['priorita']!r} unknown")
        op_, cl = R.parse_dt(r["aperto_il"]), R.parse_dt(r["chiuso_il"])
        if stg in R.TICKET_CLOSED and not cl:
            A.flag("TK-CLOSED-NO-DATE", "tickets", idl, "medium", "closed without a close date")
        if stg and stg not in R.TICKET_CLOSED and cl:
            A.flag("TK-OPEN-WITH-CLOSE-DATE", "tickets", idl, "medium", "open but has a close date", judgment=True)
        if op_ and cl and cl < op_:
            A.flag("TK-CLOSED-BEFORE-OPENED", "tickets", idl, "high",
                   f"closed {cl} before it was opened {op_}", judgment=True,
                   evidence={"opened": _ts(op_), "closed": _ts(cl), "status": r["stato"], "subject": _txt(r["oggetto"]),
                             "description": _txt(r["descrizione"])[:400]})
        contact = ref_contact(r["id_contatto"])
        if (r["id_contatto"] or "").strip() and not contact:
            A.flag("TK-CONTACT-GONE", "tickets", idl, "low", f"contact {r['id_contatto']} deleted or missing: cleared",
                   fix={"field": "id_contatto", "old": r["id_contatto"], "new": None, "confidence": "high"})
        sender = R.ticket_sender(r["descrizione"])
        if not contact and sender:
            hit = _email_idx(contacts).get(sender)
            if hit:
                contact = hit
                A.flag("TK-CONTACT-FROM-SENDER", "tickets", idl, "low", f"no contact; sender {sender} is contact {hit}",
                       fix={"field": "id_contatto", "old": r["id_contatto"], "new": hit, "confidence": "high"})
        comp = ref_company(r["id_azienda"], "tickets", idl, "TK")
        if not comp and contact and contacts[contact]["company"]:
            # R5: the ticket is associated with the company indicated in the ticket only -> suggest, don't apply
            A.flag("TK-COMPANY-FROM-CONTACT", "tickets", idl, "info",
                   f"no company on the ticket; its contact works for {contacts[contact]['company']} (not applied: R5)")
        elif comp and contact and contacts[contact]["company"] and contacts[contact]["company"] != comp:
            A.flag("TK-CONTACT-COMPANY-MISMATCH", "tickets", idl, "low",
                   f"contact belongs to {contacts[contact]['company']}, ticket to {comp}")
        uid, how = resolve_user(r["id_utente"])
        if how not in ("code", "name"):
            A.flag("TK-OWNER-UNRESOLVED", "tickets", idl, "medium", f"owner {r['id_utente']!r} unresolved")
        owner = owner_out(uid, "tickets", idl, "TK")
        t = {"id_legacy": idl, "subject": _txt(r["oggetto"]), "content": _txt(r["descrizione"]), "stage": stg,
             "hs_ticket_priority": pr, "createdate": _ts(op_), "closed_date": _ts(cl), "assegnatario": owner,
             "contact": contact, "company": comp}
        tickets.append(t)
        trails["tickets"].write({"id_legacy": idl, "opened": _ts(op_), "closed": _ts(cl), "status_raw": r["stato"],
                                 "stage": stg, "owner": users[uid]["email"] if uid else None,
                                 "owner_active": bool(uid and users[uid]["attivo"]), "last_modified": r["ultima_modifica"]})
    clean["tickets"] = tickets

    # ---------------------------------------------------------- activities  [R6]
    activities, seen_content = [], {}
    for r in export["attivita"]:
        idl = r["id_attivita"].strip()
        if R.is_deleted(r["cancellato"]):
            A.counts["GEN-DELETED/activities"] += 1
            continue
        typ = R.activity_type(r["tipo"])
        if not typ:
            A.flag("AC-TYPE-UNKNOWN", "activities", idl, "medium", f"type {r['tipo']!r} unknown", judgment=True)
        ts = R.parse_dt(r["data"])
        if not ts:
            A.flag("AC-DATE-UNPARSED", "activities", idl, "medium", f"date {r['data']!r} unreadable")
        elif ts > R.EXPORT_DATE:
            A.flag("AC-DATE-FUTURE", "activities", idl, "medium", f"dated after the export ({ts.date()})")
        contact = ref_contact(r["id_contatto"])
        if (r["id_contatto"] or "").strip() and not contact:
            A.counts["AC-CONTACT-GONE"] += 1
        deal = (r["id_opportunita"] or "").strip()
        if deal and deal not in deals:
            A.counts["AC-DEAL-GONE"] += 1
            deal = None
        author = users.get(r["id_utente"].strip())
        if not author:
            A.flag("AC-AUTHOR-UNKNOWN", "activities", idl, "low", f"author {r['id_utente']!r} not a user")
        text = _txt(r["testo"])
        key = (typ, r["data"].strip(), text, contact, deal or "")
        if key in seen_content:
            A.flag("AC-DUPLICATE", "activities", idl, "low", f"same type, date, text and links as {seen_content[key]}",
                   fix={"field": "merge_into", "old": idl, "new": seen_content[key], "confidence": "medium"})
        else:
            seen_content[key] = idl
        activities.append({"id_legacy": idl, "type": typ, "hs_timestamp": _ts(ts), "body": text,
                           "autore": author["email"] if author else None, "contact": contact, "deal": deal or None,
                           "duplicate_of": seen_content[key] if seen_content[key] != idl else None})
    clean["activities"] = activities

    for s in trails.values():
        s.close()
    A.findings.close()
    return {"clean": clean, "counts": A.counts, "judgment": A.judgment,
            "stats": {k: len(v) for k, v in clean.items()} | {"findings": A.findings.n}}


_EIDX: dict = {}


def _email_idx(contacts: dict) -> dict:
    key = id(contacts)
    if _EIDX.get("k") != key:
        _EIDX["k"] = key
        _EIDX["v"] = {c["email"]: c["id_legacy"] for c in contacts.values() if c["email"]}
    return _EIDX["v"]
