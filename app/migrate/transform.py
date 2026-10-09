"""Sinergia rows -> CRM records. Pure function (no DB): easy to test offline.

Output (consumed by run.load):
  n          number of objects (local ids 0..n-1; the loader adds a reserved base id)
  objects    {otype: [(local_id, props, created_at|None)]}
  assocs     set of (from_type, from_local, to_type, to_local, typeId)   both directions included
  uniques    [(otype, property, value, local_id)]
  refs       [(local_id, property, local_id_of_target)]  -> property gets the target's CRM id
  dormant    [company local ids]  (R9)
  stats      counters for logs / NOTES.md
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal

from ..defaults import INVERSE
from . import normalize as N

FX = {"EUR": Decimal("1"), "USD": Decimal("0.92"), "GBP": Decimal("1.17")}
WON = {("vendite", "6"), ("rinnovi", 3)}
CLOSED = WON | {("vendite", "7"), ("rinnovi", 4)}
_OLD = datetime(1900, 1, 1, tzinfo=N.ROME)

# activity -> contact / deal typeIds
ACT_TO_CONTACT = {"notes": 202, "calls": 194, "emails": 198, "meetings": 200}
ACT_TO_DEAL = {"notes": 214, "calls": 206, "emails": 210, "meetings": 212}


class Out:
    def __init__(self):
        self.n = 0
        self.objects: dict[str, list] = defaultdict(list)
        self.assocs: set[tuple] = set()
        self.uniques: list[tuple] = []
        self.refs: list[tuple] = []
        self.stats = Counter()

    def add(self, otype: str, props: dict, created=None) -> int:
        i = self.n
        self.n += 1
        self.objects[otype].append((i, {k: v for k, v in props.items() if v not in (None, "")}, created))
        self.stats[f"obj.{otype}"] += 1
        return i

    def link(self, ft: str, fi: int, tt: str, ti: int, type_id: int) -> None:
        self.assocs.add((ft, fi, tt, ti, type_id))
        self.assocs.add((tt, ti, ft, fi, INVERSE[type_id]))


def _ts(row) -> datetime:
    return N.parse_local(row.get("ultima_modifica")) or _OLD


def _latest(rows: list[dict], getter) -> str | None:
    """Value from the most recent row that has it filled (rows sorted oldest -> newest)."""
    for r in reversed(rows):
        v = getter(r)
        if v not in (None, ""):
            return v
    return None


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.p[max(a, b)] = min(a, b)


# ------------------------------------------------------------------ users

class Users:
    def __init__(self, rows: list[dict]):
        self.by_id = {}
        self.by_name = {}
        self._cache = {}
        self._fcache = {}
        for u in rows:
            uid = self._norm_id(u.get("id_utente"))
            if not uid:
                continue
            self.by_id[uid] = u
            n, c = N.fold(u.get("nome")), N.fold(u.get("cognome"))
            for key in (f"{n} {c}", f"{c} {n}", f"{n[:1]} {c}", f"{c} {n[:1]}"):
                self.by_name.setdefault(key, uid)

    @staticmethod
    def _norm_id(raw) -> str | None:
        m = re.fullmatch(r"\s*[uU]\s*0*(\d+)\s*", raw or "")
        return f"U{int(m.group(1)):02d}" if m else None

    def resolve(self, raw: str | None) -> str | None:
        if raw in self._cache:
            return self._cache[raw]
        self._cache[raw] = v = self._resolve(raw)
        return v

    def _resolve(self, raw: str | None) -> str | None:
        uid = self._norm_id(raw)
        if uid:
            return uid if uid in self.by_id else None
        key = N.fold(raw)
        if not key:
            return None
        if key in self.by_name:
            return self.by_name[key]
        parts = key.split()
        if len(parts) >= 2:  # 'mazza e' / 't lombardo'
            for a, b in ((parts[0], parts[-1]), (parts[-1], parts[0])):
                k = f"{b[:1]} {a}" if len(b) == 1 else f"{a} {b}"
                if k in self.by_name:
                    return self.by_name[k]
        return None

    def email(self, uid: str | None) -> str | None:
        u = self.by_id.get(uid or "")
        return (u.get("email") or "").strip().lower() or None if u else None

    def follower(self, raw: str | None) -> str | None:
        """R3: deals/tickets are followed by someone who works here today: a departed owner's
        records go to their manager (responsabile), up the chain to the first active one."""
        if raw in self._fcache:
            return self._fcache[raw]
        self._fcache[raw] = v = self._follower(raw)
        return v

    def _follower(self, raw: str | None) -> str | None:
        uid, seen = self.resolve(raw), set()
        while uid and uid not in seen:
            seen.add(uid)
            u = self.by_id.get(uid)
            if u is None:
                return None
            if N.is_active(u.get("attivo")):
                return self.email(uid)
            uid = self._norm_id(u.get("responsabile"))
        return None


# ------------------------------------------------------------------ main

def transform(data: dict[str, list[dict]], ids: dict) -> dict:
    out = Out()
    st = out.stats
    users = Users(data.get("utenti", []))
    rinnovi, assistenza = ids["rinnovi"], ids["assistenza"]

    # ---------------- R1 companies: merge by domain or partita IVA
    rows = [r for r in data.get("aziende", []) if not N.is_deleted(r.get("cancellato"))]
    st["aziende.deleted"] = len(data.get("aziende", [])) - len(rows)
    doms = [N.parse_domain(r.get("sito_web")) for r in rows]
    pivas = [N.parse_piva(r.get("note")) for r in rows]
    uf = UF(len(rows))
    first: dict = {}
    for i in range(len(rows)):
        for key in (("d", doms[i]), ("p", pivas[i])):
            if key[1]:
                if key in first:
                    uf.union(first[key], i)
                else:
                    first[key] = i
    groups = defaultdict(list)
    for i in range(len(rows)):
        groups[uf.find(i)].append(i)
    comp_map: dict[str, int] = {}          # id_azienda -> company local id
    domain_index: dict[str, int] = {}      # domain (primary + additional) -> company local id
    comp_rows: dict[int, list[dict]] = {}
    for members in groups.values():
        members.sort(key=lambda i: (_ts(rows[i]), i))
        rs = [rows[i] for i in members]
        primary_domain = _latest(members, lambda i: doms[i])
        extra = []
        for i in reversed(members):
            if doms[i] and doms[i] != primary_domain and doms[i] not in extra:
                extra.append(doms[i])
        state = _latest(rs, lambda r: N.clean(r.get("provincia")))
        props = {
            "name": _latest(rs, lambda r: N.clean(r.get("ragione_sociale"))),
            "domain": primary_domain,
            "hs_additional_domains": ";".join(extra) or None,
            "city": _latest(rs, lambda r: N.clean(r.get("citta"))),
            "state": state.upper() if state else None,
            "partita_iva": _latest(members, lambda i: pivas[i]),
            "id_legacy": N.clean(rs[-1].get("id_azienda")),
        }
        cid = out.add("companies", props)
        comp_rows[cid] = rs
        if props["partita_iva"]:
            out.uniques.append(("companies", "partita_iva", props["partita_iva"], cid))
        for r in rs:
            comp_map[N.clean(r.get("id_azienda"))] = cid
        for d in [primary_domain, *extra]:
            if d:
                domain_index.setdefault(d, cid)
        if len(members) > 1:
            st["aziende.merged_groups"] += 1
            st["aziende.merged_rows"] += len(members) - 1

    # ---------------- R2 contacts: merge by valid email
    rows = [r for r in data.get("contatti", []) if not N.is_deleted(r.get("cancellato"))]
    st["contatti.deleted"] = len(data.get("contatti", [])) - len(rows)
    by_key = defaultdict(list)
    for i, r in enumerate(rows):
        em = N.parse_email(r.get("email"))
        if N.clean(r.get("email")) and not em:
            st["contatti.invalid_email"] += 1
        by_key[("e", em) if em else ("i", i)].append(r)
    contact_map: dict[str, int] = {}
    email_index: dict[str, int] = {}
    contact_company: dict[int, int] = {}
    for key, rs in by_key.items():
        rs.sort(key=_ts)
        company = _latest(rs, lambda r: comp_map.get(N.clean(r.get("id_azienda"))))
        email = key[1] if key[0] == "e" else None
        props = {
            "firstname": _latest(rs, lambda r: N.clean(r.get("nome"))),
            "lastname": _latest(rs, lambda r: N.clean(r.get("cognome"))),
            "email": email,
            "phone": _latest(rs, lambda r: N.clean(r.get("telefono"))),
            "lifecyclestage": _latest(rs, lambda r: N.lifecycle(r.get("tipo"))),
            "id_legacy": N.clean(rs[-1].get("id_contatto")),
        }
        k = out.add("contacts", props)
        for r in rs:
            contact_map[N.clean(r.get("id_contatto"))] = k
        if email:
            email_index[email] = k
        if len(rs) > 1:
            st["contatti.merged_groups"] += 1
            st["contatti.merged_rows"] += len(rs) - 1
        if company is None and email:  # R12: company from the email domain (existing companies only)
            company = domain_index.get(email.rsplit("@", 1)[1])
            if company is not None:
                st["contatti.r12_associated"] += 1
        if company is not None:
            contact_company[k] = company
            out.link("contacts", k, "companies", company, 279)
            out.link("contacts", k, "companies", company, 1)

    # ---------------- R4 price list -> products (same SKU = same article, latest price)
    prows = [r for r in data.get("listino", []) if not N.is_deleted(r.get("cancellato"))]
    by_sku = defaultdict(list)
    for r in prows:
        sku = N.parse_sku(r.get("codice_articolo"))
        if sku:
            by_sku[sku].append(r)
    product_map: dict[str, int] = {}
    product_name: dict[str, str] = {}
    versions: dict[str, list] = {}
    for sku, rs in by_sku.items():
        rs.sort(key=_ts)
        versions[sku] = [(_ts(r), N.plain_number(r.get("prezzo_listino"))) for r in rs]
        name = _latest(rs, lambda r: N.clean(r.get("descrizione")))
        price = _latest(rs, lambda r: N.plain_number(r.get("prezzo_listino")))
        product_map[sku] = out.add("products", {"hs_sku": sku, "name": name, "price": N.num_str(price)})
        product_name[sku] = name

    def list_price(sku: str, when: datetime | None):
        vs = versions.get(sku) or []
        if not vs:
            return None
        if when is not None:
            valid = [p for t, p in vs if t <= when and p is not None]
            if valid:
                return valid[-1]
        return next((p for t, p in vs if p is not None), None)

    # ---------------- stage history (closedate fallback)
    history = defaultdict(list)
    for h in data.get("storico_fasi", []):
        history[N.clean(h.get("id_opportunita"))].append((N.parse_local(h.get("data_cambio")), N.parse_stage(h.get("fase_nuova"))))

    # ---------------- quote lines grouped by deal
    lines_by_deal = defaultdict(list)
    for r in data.get("righe_offerta", []):
        lines_by_deal[N.clean(r.get("id_opportunita"))].append(r)

    # ---------------- R3 deals
    drows = [r for r in data.get("opportunita", []) if not N.is_deleted(r.get("cancellato"))]
    st["opportunita.deleted"] = len(data.get("opportunita", [])) - len(drows)
    deal_map: dict[str, int] = {}
    deal_company: dict[int, int] = {}
    revenue = defaultdict(Decimal)
    won_companies: set[int] = set()
    for r in drows:
        legacy = N.clean(r.get("id_opportunita"))
        stage = N.parse_stage(r.get("fase"))
        pipe = N.parse_pipeline(r.get("pipeline"))
        if stage and pipe and stage[0] != pipe:
            st["opportunita.pipeline_stage_conflict"] += 1
        pipe = stage[0] if stage else (pipe or "vendite")
        if stage is None:
            stage = (pipe, "1" if pipe == "vendite" else 1)
            st["opportunita.stage_missing"] += 1
        amount, cur_txt, monthly = N.parse_amount(r.get("importo"))
        currency = cur_txt or N.currency_of(r.get("valuta") or "") or "EUR"
        if monthly and amount is not None:
            amount *= 12  # renewals are annual
            st["opportunita.monthly_x12"] += 1
        close = N.parse_day(r.get("data_chiusura"))
        if close is None and stage in CLOSED:
            hits = [t for t, s in history.get(legacy, []) if s == stage and t]
            if hits:
                close = max(hits).date()
                st["opportunita.closedate_from_history"] += 1
        ref_time = N.parse_local(r.get("data_chiusura")) or _ts(r)
        # R4 lines: the deal is worth the total of its lines
        line_props = []
        for lr in lines_by_deal.get(legacy, []):
            sku = N.parse_sku(lr.get("codice_articolo"))
            qty = N.plain_number(lr.get("quantita"))
            price = N.plain_number(lr.get("prezzo_unitario"))
            if price is None and sku:
                price = list_price(sku, ref_time)
                st["righe.price_from_listino"] += 1
            disc = N.parse_discount(lr.get("sconto"))
            total = None
            if qty is not None and price is not None:
                total = (qty * price * (1 - disc / 100)).quantize(N.CENT, rounding="ROUND_HALF_UP")
            line_props.append(({
                "name": N.clean(lr.get("descrizione")) or product_name.get(sku or ""),
                "quantity": N.num_str(qty),
                "price": N.num_str(price),
                "hs_discount_percentage": N.num_str(disc) or "0",
                "amount": N.money(total),
                "hs_sku": sku,
                "id_legacy": N.clean(lr.get("id_riga")),
            }, product_map.get(sku or ""), total))
        if line_props:
            amount = sum((t for _, _, t in line_props if t is not None), Decimal(0))
            currency = "EUR"
            st["opportunita.amount_from_lines"] += 1
        props = {
            "dealname": N.clean(r.get("titolo")),
            "amount": N.money(amount),
            "deal_currency_code": currency if amount is not None else None,
            "pipeline": "default" if pipe == "vendite" else rinnovi["__pipeline__"],
            "dealstage": N.sales_stage_id(stage[1]) if pipe == "vendite" else rinnovi[N.RINNOVI_LABELS[stage[1]]],
            "closedate": N.iso_day(close),
            "commerciale": users.follower(r.get("id_commerciale")),
            "id_legacy": legacy,
        }
        d = out.add("deals", props)
        deal_map[legacy] = d
        company = comp_map.get(N.clean(r.get("id_azienda")))
        if company is not None:
            deal_company[d] = company
            out.link("deals", d, "companies", company, 341)
            out.link("deals", d, "companies", company, 5)
        for c in {contact_map[x.strip()] for x in re.split(r"[;,]", r.get("contatti") or "") if x.strip() in contact_map}:
            out.link("deals", d, "contacts", c, 3)
        for lp, prod, _ in line_props:
            li = out.add("line_items", lp)
            out.link("line_items", li, "deals", d, 20)
            if prod is not None:
                out.refs.append((li, "hs_product_id", prod))
        # R8 / R9 inputs
        if company is not None and stage in WON:
            if amount is not None and close is not None and close.year == 2025:
                revenue[company] += amount * FX.get(currency, Decimal(1))
            if amount is None or amount > 0:
                won_companies.add(company)
            if amount is not None and amount < 0:
                st["opportunita.refunds_won_stage"] += 1
        elif amount is not None and amount < 0:
            st["opportunita.refunds_other_stage"] += 1
    st["righe.dropped_deal_missing_or_deleted"] = sum(len(v) for k, v in lines_by_deal.items() if k not in deal_map)

    # ---------------- R5 tickets
    trows = [r for r in data.get("ticket", []) if not N.is_deleted(r.get("cancellato"))]
    for r in trows:
        opened = N.parse_local(r.get("aperto_il"))
        closed = N.parse_local(r.get("chiuso_il"))
        props = {
            "subject": N.clean(r.get("oggetto")),
            "content": N.clean(r.get("descrizione")),
            "hs_pipeline": assistenza["__pipeline__"],
            "hs_pipeline_stage": assistenza[N.ticket_state(r.get("stato"))],
            "hs_ticket_priority": N.ticket_priority(r.get("priorita")),
            "createdate": N.iso_utc(opened),
            "closed_date": N.iso_utc(closed),
            "assegnatario": users.follower(r.get("id_utente")),
            "id_legacy": N.clean(r.get("id_ticket")),
        }
        t = out.add("tickets", props, opened)
        contact = contact_map.get(N.clean(r.get("id_contatto")))
        if contact is None:
            m = re.match(r"\s*Da:\s*(\S+)", r.get("descrizione") or "")
            em = N.parse_email(m.group(1)) if m else None
            contact = email_index.get(em or "")
            if contact is not None:
                st["ticket.contact_from_da_email"] += 1
        if contact is not None:
            out.link("tickets", t, "contacts", contact, 16)
        company = comp_map.get(N.clean(r.get("id_azienda")))
        if company is not None:
            out.link("tickets", t, "companies", company, 339)

    # ---------------- R6 activities (+ R9 activity in 2025)
    active_2025: set[int] = set()
    contact_to_company = contact_company
    for r in data.get("attivita", []):
        if N.is_deleted(r.get("cancellato")):
            st["attivita.deleted"] += 1
            continue
        otype = N.activity_type(r.get("tipo"))
        when = N.parse_local(r.get("data"))
        uid = users.resolve(r.get("id_utente"))
        props = {
            "hs_timestamp": N.iso_utc(when),
            N.BODY_PROP[otype]: N.clean(r.get("testo")),
            "autore": users.email(uid),
            "id_legacy": N.clean(r.get("id_attivita")),
        }
        a = out.add(otype, props)
        contact = contact_map.get(N.clean(r.get("id_contatto")))
        deal = deal_map.get(N.clean(r.get("id_opportunita")))
        if contact is not None:
            out.link(otype, a, "contacts", contact, ACT_TO_CONTACT[otype])
        if deal is not None:
            out.link(otype, a, "deals", deal, ACT_TO_DEAL[otype])
        if when is not None and when.year == 2025:
            if contact is not None and contact in contact_to_company:
                active_2025.add(contact_to_company[contact])
            if deal is not None and deal in deal_company:
                active_2025.add(deal_company[deal])

    # ---------------- R8 revenue + class, R9 dormant
    for cid, _rs in comp_rows.items():
        total = revenue.get(cid, Decimal(0)).quantize(N.CENT, rounding="ROUND_HALF_UP")
        props = out.objects["companies"][cid][1]
        props["fatturato_2025"] = str(total)
        if total >= 100000:
            props["classe_cliente"] = "A"
        elif total >= 20000:
            props["classe_cliente"] = "B"
        elif total > 0:
            props["classe_cliente"] = "C"
        if "classe_cliente" in props:
            st[f"r8.class_{props['classe_cliente']}"] += 1
    dormant = sorted(won_companies - active_2025)
    st["r9.won_companies"] = len(won_companies)
    st["r9.dormant"] = len(dormant)
    st["assocs"] = len(out.assocs)
    return {"n": out.n, "objects": out.objects, "assocs": out.assocs, "uniques": out.uniques,
            "refs": out.refs, "dormant": dormant, "stats": dict(st)}
