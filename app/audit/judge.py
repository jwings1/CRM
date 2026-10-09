"""The agent layer: openai/gpt-6-luna on OpenRouter, only for what code can't decide.

- Hard budget: a persistent ledger (llm_ledger.json) of real cost from OpenRouter's `usage.cost`;
  no call starts if spent + reserve would pass the cap.
- Saved as it runs: every batch result is appended to findings.agent.jsonl the moment it returns;
  batches already done are skipped on resume; raw responses are cached by input hash.
- Strict JSON output (json_schema); malformed answers are retried once, then logged as errors.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-6-luna")
URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1") + "/chat/completions"
PRICE_IN, PRICE_OUT = 0.10 / 1e6, 0.50 / 1e6          # USD per token, openai/gpt-6-luna (OpenRouter, Oct 2026)

SYSTEM = """Sei un revisore dei dati del CRM legacy "Sinergia 4" di Brambilla Forniture S.p.A., distributore di
forniture industriali. L'export sta per essere migrato a un nuovo CRM. Il tuo compito: trovare anomalie che il codice
non sa giudicare, e proporre correzioni prudenti. Rispondi SOLO con il JSON richiesto. Spiegazioni in italiano, brevi.

Il processo corretto di Brambilla (modello di riferimento):
- Pipeline Vendite: V01 Contatto > V02 Qualifica > V03 Presentazione > V04 Decisione > V05 Contratto > V06 Vinta | V07 Persa.
  Pipeline Rinnovi: R1 Da rinnovare > R2 In trattativa > R3 Rinnovato | R4 Non rinnovato. I rinnovi sono annuali.
- Ogni trattativa nasce in V01/R1; le fasi non tornano indietro; nulla si muove dopo la chiusura; saltare fasi in
  avanti e' normale; tra due cambi di fase passano 2-89 giorni. La data di chiusura di una trattativa chiusa e' il giorno
  del cambio di fase che la chiude. Le note di credito/storni ("Storno", "NC", "Nota di credito") hanno importo negativo
  e riducono il fatturato dell'anno.
- Le trattative e i ticket li segue solo chi lavora oggi in azienda (utenti attivi).
- Un'azienda esiste una volta sola (stesso sito = stessa azienda; stessa partita IVA = stessa azienda).
  Una persona esiste una volta sola (stessa email = stessa persona).
- Un ticket si apre prima di chiudersi.
Gia' verificato dal codice (NON ripeterlo): formati di date/importi/valute, record cancellati, duplicati per sito/email/
P.IVA, riferimenti a record cancellati, importi mensili (x12), date di chiusura mancanti, utenti non piu' attivi.

Per ogni elemento ricevuto restituisci un risultato con lo stesso "ref". verdict: "ok" se non c'e' nulla da segnalare,
"anomaly" se trovi un problema reale, "unsure" se servono informazioni che non hai. Non inventare fatti: basati solo sui
dati forniti. proposed_fix solo se sei sicuro; confidence tra 0 e 1."""

SCHEMA = {
    "name": "audit_verdicts",
    "strict": True,
    "schema": {
        "type": "object", "additionalProperties": False, "required": ["results"],
        "properties": {"results": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["ref", "verdict", "anomalies"],
            "properties": {
                "ref": {"type": "string"},
                "verdict": {"type": "string", "enum": ["ok", "anomaly", "unsure"]},
                "anomalies": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["code", "severity", "explanation", "fix_field", "fix_value", "confidence"],
                    "properties": {
                        "code": {"type": "string", "description": "SHORT-UPPER-CASE-CODE"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                        "explanation": {"type": "string"},
                        "fix_field": {"type": ["string", "null"]},
                        "fix_value": {"type": ["string", "null"]},
                        "confidence": {"type": "number"}}}}}}}}},
}


class BudgetExceeded(Exception):
    pass


class Ledger:
    def __init__(self, path: Path, cap_usd: float):
        self.path, self.cap = path, cap_usd
        self.lock = threading.Lock()
        self.data = json.loads(path.read_text()) if path.exists() else {"spent_usd": 0.0, "calls": 0,
                                                                          "tokens_in": 0, "tokens_out": 0}
        self.reserved = 0.0

    def reserve(self, est: float):
        with self.lock:
            if self.data["spent_usd"] + self.reserved + est > self.cap:
                raise BudgetExceeded(f"spent ${self.data['spent_usd']:.4f}, cap ${self.cap:.2f}")
            self.reserved += est

    def settle(self, est: float, cost: float, tin: int, tout: int):
        with self.lock:
            self.reserved -= est
            d = self.data
            d["spent_usd"] += cost
            d["calls"] += 1
            d["tokens_in"] += tin
            d["tokens_out"] += tout
            self.path.write_text(json.dumps(d, indent=1))

    @property
    def spent(self):
        return self.data["spent_usd"]


def _post(key: str, body: dict, timeout=90) -> dict:
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://brambilla-crm.local", "X-Title": "Sinergia audit"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def call(key: str, ledger: Ledger, cache_dir: Path, user: str, max_out=6000) -> tuple[dict, dict]:
    """One request. Returns (parsed json, meta). Cached by input hash: a re-run costs nothing."""
    body = {"model": MODEL, "temperature": 0, "max_tokens": max_out,
            "reasoning": {"effort": "low"}, "usage": {"include": True},
            "response_format": {"type": "json_schema", "json_schema": SCHEMA},
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
    h = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:24]
    cp = cache_dir / f"{h}.json"
    if cp.exists():
        resp = json.loads(cp.read_text())
        return json.loads(resp["choices"][0]["message"]["content"]), {"cached": True, "cost": 0.0, "hash": h}
    est = (len(SYSTEM) + len(user)) / 3.2 * PRICE_IN + max_out * PRICE_OUT
    ledger.reserve(est)
    cost, tin, tout = 0.0, 0, 0
    try:
        for attempt in range(3):
            try:
                resp = _post(key, body)
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503) and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError(f"HTTP {e.code}: {e.read()[:300]!r}")
        u = resp.get("usage") or {}
        tin, tout = u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        cost = float(u.get("cost") or (tin * PRICE_IN + tout * PRICE_OUT))
        content = resp["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(resp, ensure_ascii=False))
        return parsed, {"cached": False, "cost": cost, "hash": h, "tokens_in": tin, "tokens_out": tout}
    finally:
        ledger.settle(est, cost, tin, tout)


def run_batches(batches: list[dict], run_dir: Path, key: str, cap_usd: float, workers: int = 8,
                log=print) -> dict:
    """batches: [{"id": str, "kind": str, "items": [{"ref":..., ...}], "prompt": str}]"""
    out_path = run_dir / "findings.agent.jsonl"
    done = set()
    if out_path.exists():
        for line in out_path.open():
            try:
                done.add(json.loads(line)["batch"])
            except Exception:
                pass
    todo = [b for b in batches if b["id"] not in done]
    ledger = Ledger(run_dir / "llm_ledger.json", cap_usd)
    cache = run_dir / "cache" / "llm"
    lock = threading.Lock()
    stats = {"batches_total": len(batches), "skipped_done": len(batches) - len(todo), "ok": 0, "errors": 0,
             "stopped_by_budget": False}
    f = out_path.open("a", encoding="utf-8")

    def work(b):
        parsed, meta = call(key, ledger, cache, b["prompt"])
        return b, parsed, meta

    stop = threading.Event()
    with ThreadPoolExecutor(workers) as ex:
        futs = {}
        it = iter(todo)

        def submit_next():
            if stop.is_set():
                return
            b = next(it, None)
            if b is not None:
                futs[ex.submit(work, b)] = b

        for _ in range(workers * 2):
            submit_next()
        while futs:
            for fut in as_completed(list(futs)):
                b = futs.pop(fut)
                try:
                    b, parsed, meta = fut.result()
                    refs = {i["ref"] for i in b["items"]}
                    with lock:
                        for r in parsed.get("results", []):
                            if r.get("ref") not in refs:
                                continue
                            f.write(json.dumps({"batch": b["id"], "kind": b["kind"], **r}, ensure_ascii=False) + "\n")
                        # batch marker, so resume knows it is done even if every verdict was "ok"
                        f.write(json.dumps({"batch": b["id"], "kind": b["kind"], "ref": "__batch__",
                                            "cost": meta["cost"], "cached": meta["cached"],
                                            "answered": len(parsed.get("results", [])), "asked": len(refs)}) + "\n")
                        f.flush()
                    stats["ok"] += 1
                except BudgetExceeded as e:
                    stats["stopped_by_budget"] = True
                    stop.set()
                    log(f"budget cap reached: {e}")
                except Exception as e:  # noqa: BLE001 - logged, run continues
                    stats["errors"] += 1
                    with lock:
                        (run_dir / "agent_errors.log").open("a").write(f"{b['id']}: {e}\n")
                submit_next()
                if stats["ok"] and (stats["ok"] + stats["errors"]) % 25 == 0:
                    log(f"agent: {stats['ok']} batches, ${ledger.spent:.4f} spent")
                break
    f.close()
    stats["spent_usd"] = round(ledger.spent, 4)
    stats["ledger"] = ledger.data
    return stats


# ---------------------------------------------------------------- what the agent gets
def deal_line(t: dict) -> str:
    ev = " > ".join(f"{(e['ts'] or '?')[:10]} {e['to']} {e['by']}" for e in t["events"])
    a = t["activities"]
    return (f"[{t['id_legacy']}] \"{t['title']}\" | {t['pipeline']} | fase {t['stage']} | "
            f"commerciale {t['owner'] or '-'}{'' if t['owner_active'] else ' (non attivo)'} | "
            f"importo {t['amount'] or '-'} {t['currency'] or ''} (grezzo: {t['raw_amount']!r}) | "
            f"chiusura {t['close_date'] or '-'} | creata {(t['created'] or '-')[:10]} | ultima modifica {(t['last_modified'] or '-')[:10]} | "
            f"righe {t['lines']} tot {t['lines_total'] or '-'} | attivita {a['n']} ({(a['first'] or '-')[:10]}..{(a['last'] or '-')[:10]}) | "
            f"storico: {ev} | segnalazioni codice: {', '.join(t['flags']) or 'nessuna'}")


def build_batches(run_dir: Path, judgment: list[dict], deal_batch=40, judg_batch=15) -> list[dict]:
    batches = []
    # 1) cases the rules handed over, grouped by kind
    by_code: dict[str, list] = {}
    for j in judgment:
        by_code.setdefault(j["code"], []).append(j)
    for code, items in sorted(by_code.items()):
        for i in range(0, len(items), judg_batch):
            chunk = items[i:i + judg_batch]
            lines = [json.dumps({"ref": f"{j['entity']}:{j['id_legacy']}", "code": j["code"], "message": j["message"],
                                 "evidence": j.get("evidence")}, ensure_ascii=False) for j in chunk]
            prompt = (f"Casi segnalati dal codice come da giudicare ({code}). Per ognuno decidi. "
                      "Per i possibili duplicati: se sono la stessa entita' usa fix_field='merge_into' e fix_value con l'id "
                      "da tenere (il piu' completo); se sono entita' diverse verdict='ok'. Per date invertite indica quale "
                      "campo correggere.\n" + "\n".join(lines))
            batches.append({"id": f"J-{code}-{i // judg_batch}-{hashlib.sha1(prompt.encode()).hexdigest()[:8]}",
                            "kind": "judgment",
                            "items": [{"ref": f"{j['entity']}:{j['id_legacy']}"} for j in chunk], "prompt": prompt})
    # 2) every deal trail, flagged ones first
    trails = [json.loads(l) for l in (run_dir / "trails" / "deals.jsonl").open()]
    trails.sort(key=lambda t: (not t["flags"], t["id_legacy"]))
    for i in range(0, len(trails), deal_batch):
        chunk = trails[i:i + deal_batch]
        prompt = ("Storia di ogni trattativa dalla creazione a oggi (export del 1/12/2026). Cerca incoerenze che il "
                  "codice non ha gia' segnalato, per esempio: nota di credito/storno in una fase che non ha senso o con "
                  "importo implausibile, importo implausibile rispetto alle righe o al tipo di documento, trattativa "
                  "aperta e ferma da anni, data di chiusura prevista gia' passata da anni su una trattativa aperta, "
                  "commerciale diverso da chi ha mosso le fasi, valuta incoerente col titolo. "
                  "NON sono anomalie (verificato su tutto l'export): il tipo di titolo ('Rinnovo', 'Offerta', "
                  "'Fornitura') e' indipendente dalla pipeline; attivita' precedenti alla creazione della trattativa; "
                  "fasi saltate in avanti. Restituisci SOLO le trattative con verdict 'anomaly' o 'unsure' "
                  "(ref = id tra parentesi quadre).\n" + "\n".join(deal_line(t) for t in chunk))
        batches.append({"id": f"D-{i // deal_batch:05d}-{hashlib.sha1(prompt.encode()).hexdigest()[:8]}",
                        "kind": "deal_trail",
                        "items": [{"ref": t["id_legacy"]} for t in chunk], "prompt": prompt})
    return batches
