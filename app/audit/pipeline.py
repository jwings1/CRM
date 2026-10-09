"""Legacy audit inside POST /__migrate.

  1. rules      deterministic checks on the raw export (core.run): trails, findings, judgment cases
  2. decisions  gpt-6-luna on the judgment cases only, in parallel, under a hard deadline and a $ cap;
                company merges with confidence >= 0.9 are applied by the migration (transform company_links)
  3. record     every finding (rules + agent) into Postgres schema `audit` after the load

The review of every deal trail is NOT run here (25 min, ~$1.70): it changes no data. Run it offline with
`python -m audit.run --agent`.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path

from . import core, judge

log = logging.getLogger("crm")

# The LLM step gets whatever the 5-minute /__migrate window leaves: TOTAL_S minus the time already spent
# (download, read, rules) minus a reserve for transform + load + record (2x what they take locally).
TOTAL_S = float(os.environ.get("AUDIT_MIGRATE_BUDGET_S", "250"))
POST_RESERVE_S = float(os.environ.get("AUDIT_POST_LLM_RESERVE_S", "90"))
DEADLINE_MAX_S = float(os.environ.get("AUDIT_LLM_DEADLINE_S", "180"))


def llm_deadline(started: float | None) -> float:
    if started is None:
        return DEADLINE_MAX_S
    left = TOTAL_S - (time.monotonic() - started) - POST_RESERVE_S
    return max(15.0, min(DEADLINE_MAX_S, left))
BUDGET_USD = float(os.environ.get("AUDIT_LLM_BUDGET_USD", "0.50"))
WORKERS = int(os.environ.get("AUDIT_LLM_WORKERS", "24"))
MIN_CONF = 0.9
BATCH = 15


def run_rules(data: dict) -> dict:
    """Deterministic audit. Returns findings, judgment cases, run dir."""
    run_dir = Path(tempfile.mkdtemp(prefix="audit-"))
    res = core.run(data, run_dir, "manager")
    findings = [json.loads(l) for l in (run_dir / "findings.deterministic.jsonl").open()]
    return {"run_dir": run_dir, "findings": findings, "judgment": res["judgment"], "counts": dict(res["counts"]),
            "r8": res["r8"], "r9": res["r9"], "r12": res["counts"].get("CT-COMPANY-FROM-DOMAIN", 0)}


def cross_check(rules: dict, res: dict, company_links) -> dict:
    """R8 / R9 / R12 as the migration computed them vs. the audit's independent recomputation.
    Differences become findings; companies merged by the agent are marked (expected to differ)."""
    merged = {x for pair in (company_links or []) for x in pair}
    by_local = {i: p for i, p, _ in res["objects"].get("companies", [])}
    crm_r8 = {p.get("id_legacy"): (p.get("fatturato_2025"), p.get("classe_cliente")) for p in by_local.values()}
    crm_r9 = {by_local[i].get("id_legacy") for i in res.get("dormant", []) if i in by_local}
    out = {"r8_mismatch": 0, "r9_only_crm": 0, "r9_only_audit": 0, "explained_by_agent_merge": 0,
           "r12_crm": res["stats"].get("contatti.r12_associated"), "r12_audit": rules.get("r12")}
    for cid, (rev, cls) in crm_r8.items():
        mine = rules["r8"].get(cid)
        if mine and (mine[0] != (rev or "0.00") or mine[1] != cls):
            why = cid in merged
            out["explained_by_agent_merge"] += why
            out["r8_mismatch"] += 1
            rules["findings"].append({"source": "rule", "code": "AU-R8-MISMATCH", "entity": "companies", "id_legacy": cid,
                                      "severity": "info" if why else "high",
                                      "message": f"migration: {rev} / {cls}; audit: {mine[0]} / {mine[1]}"
                                                 + (" (company merged by the agent)" if why else "")})
    for cid, code, side in [(c, "AU-R9-ONLY-CRM", "r9_only_crm") for c in crm_r9 - rules["r9"]] + \
                           [(c, "AU-R9-ONLY-AUDIT", "r9_only_audit") for c in rules["r9"] - crm_r9]:
        why = cid in merged
        out[side] += 1
        out["explained_by_agent_merge"] += why
        rules["findings"].append({"source": "rule", "code": code, "entity": "companies", "id_legacy": cid,
                                  "severity": "info" if why else "high",
                                  "message": "dormant per " + ("the migration only" if side == "r9_only_crm" else "the audit only")
                                             + (" (company merged by the agent)" if why else "")})
    if out["r12_crm"] != out["r12_audit"]:
        rules["findings"].append({"source": "rule", "code": "AU-R12-MISMATCH", "entity": "contacts", "id_legacy": "*",
                                  "severity": "medium",
                                  "message": f"R12 links: migration {out['r12_crm']}, audit {out['r12_audit']}"})
    return out


def _batches(judgment: list[dict]) -> list[dict]:
    by_code: dict[str, list] = {}
    for j in judgment:
        by_code.setdefault(j["code"], []).append(j)
    out = []
    for code, items in sorted(by_code.items()):
        for i in range(0, len(items), BATCH):
            chunk = items[i:i + BATCH]
            lines = [json.dumps({"ref": f"{j['entity']}:{j['id_legacy']}", "code": j["code"], "message": j["message"],
                                 "evidence": j.get("evidence")}, ensure_ascii=False, default=str) for j in chunk]
            prompt = (f"Casi segnalati dal codice come da giudicare ({code}). Per ognuno decidi. "
                      "Per i possibili duplicati: se sono la stessa entita' usa fix_field='merge_into' e fix_value con l'id "
                      "da tenere (il piu' completo); se sono entita' diverse verdict='ok'. Per date invertite indica quale "
                      "campo correggere.\n" + "\n".join(lines))
            out.append({"id": f"J-{code}-{i // BATCH}-{hashlib.sha1(prompt.encode()).hexdigest()[:8]}",
                        "items": chunk, "prompt": prompt})
    return out


def run_decisions(judgment: list[dict], run_dir: Path, deadline_s: float | None = None) -> dict:
    """gpt-6-luna on the judgment cases. Never raises; what isn't back by the deadline stays as the rules left it."""
    key = os.environ.get("OPENROUTER_API_KEY")
    stats = {"batches": 0, "answered": 0, "late_or_failed": 0, "cost_usd": 0.0, "merges": 0}
    if not key or not judgment:
        stats["skipped"] = "no key" if not key else "nothing to judge"
        return {"verdicts": [], "company_links": [], "stats": stats}
    batches = _batches(judgment)
    stats["batches"] = len(batches)
    ledger = judge.Ledger(run_dir / "llm_ledger.json", BUDGET_USD)
    cache = run_dir / "cache"
    t0 = time.monotonic()
    ex = ThreadPoolExecutor(WORKERS)
    futs = {ex.submit(judge.call, key, ledger, cache, b["prompt"], 4000): b for b in batches}
    deadline_s = deadline_s or DEADLINE_MAX_S
    stats["deadline_s"] = round(deadline_s, 1)
    done, pending = wait(futs, timeout=deadline_s)
    ex.shutdown(wait=False, cancel_futures=True)
    verdicts, links = [], []
    for f in done:
        b = futs[f]
        try:
            parsed, meta = f.result()
        except Exception as e:  # noqa: BLE001
            stats["late_or_failed"] += 1
            log.warning("audit llm batch %s failed: %s", b["id"], e)
            continue
        stats["answered"] += 1
        stats["cost_usd"] += meta.get("cost", 0)
        refs = {f"{j['entity']}:{j['id_legacy']}": j for j in b["items"]}
        for r in parsed.get("results", []):
            j = refs.get(r.get("ref"))
            if not j:
                continue
            verdicts.append({"batch": b["id"], **r})
            for a in r.get("anomalies", []):
                if a.get("fix_field") == "merge_into" and (a.get("confidence") or 0) >= MIN_CONF \
                        and j["code"] == "CO-NAME-DUP-CANDIDATE":
                    group = [c["id_legacy"] for c in (j.get("evidence") or {}).get("candidates", [])]
                    tgt = (a.get("fix_value") or "").strip()
                    if tgt in group:
                        links += [(tgt, x) for x in group if x != tgt]
                        stats["merges"] += 1
                        a["applied"] = True
    stats["late_or_failed"] += len(pending)
    stats["seconds"] = round(time.monotonic() - t0, 1)
    stats["cost_usd"] = round(stats["cost_usd"], 4)
    return {"verdicts": verdicts, "company_links": links, "stats": stats}


AUDIT_DDL = """
CREATE SCHEMA IF NOT EXISTS audit;
CREATE TABLE IF NOT EXISTS audit.runs (run_id text PRIMARY KEY, at timestamptz DEFAULT now(), stats jsonb);
CREATE TABLE IF NOT EXISTS audit.findings (
  run_id text, source text, code text, entity text, id_legacy text, severity text, message text,
  fix_field text, fix_old text, fix_new text, confidence text, applied boolean, evidence jsonb);
CREATE INDEX IF NOT EXISTS audit_findings_rec ON audit.findings (entity, id_legacy);
"""

_NOT_APPLIED = {"DL-STALE-OPEN", "TK-COMPANY-FROM-CONTACT"}


def finding_rows(run_id: str, rules: dict, decisions: dict) -> list[tuple]:
    rows = []
    for f in rules["findings"]:
        fx = f.get("fix") or {}
        rows.append((run_id, "rule", f["code"], f["entity"], f["id_legacy"], f["severity"], f["message"],
                     fx.get("field"), None if fx.get("old") is None else str(fx.get("old")),
                     None if fx.get("new") is None else str(fx.get("new")), fx.get("confidence"),
                     bool(fx) and f["code"] not in _NOT_APPLIED,
                     json.loads(json.dumps(f["evidence"], default=str)) if f.get("evidence") else None))
    for v in decisions["verdicts"]:
        if v.get("verdict") == "ok":
            continue
        ent, _, idl = v["ref"].rpartition(":")
        for a in v.get("anomalies") or []:
            rows.append((run_id, "agent", "AG-" + a.get("code", "UNSURE"), ent, idl, a.get("severity"),
                         a.get("explanation"), a.get("fix_field"), None, a.get("fix_value"), str(a.get("confidence")),
                         bool(a.get("applied")), {"verdict": v["verdict"]}))
    return rows


async def record(conn, run_id: str, rules: dict, decisions: dict, stats: dict) -> int:
    await conn.execute(AUDIT_DDL)
    await conn.execute("TRUNCATE audit.findings")       # one migration = one audited dataset
    rows = finding_rows(run_id, rules, decisions)
    await conn.copy_records_to_table(
        "findings", schema_name="audit", records=rows,
        columns=["run_id", "source", "code", "entity", "id_legacy", "severity", "message", "fix_field", "fix_old",
                 "fix_new", "confidence", "applied", "evidence"])
    await conn.execute("INSERT INTO audit.runs (run_id, stats) VALUES ($1, $2::jsonb) ON CONFLICT (run_id) DO UPDATE "
                       "SET stats = EXCLUDED.stats", run_id, json.loads(json.dumps(stats, default=str)))
    return len(rows)
