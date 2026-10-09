# PLAN — Zero to HubSpot (Brambilla CRM)

Freeze **15:30** (platform clock). Last push **15:20**. Choice sheet **15:00–15:25**.

## The math (read this first)

| Block | Pts | Gated by `/__migrate` 204? |
|---|---|---|
| R1–R9 data requests | 40 | yes |
| R10–R12 behaviour | 10 | R12 partly |
| Assistant R13 | 30 | yes (eval migrates a small clean export first) |
| Conformity (HubSpot API shape) | 10 | no |
| Durability | 10 | yes |

**~80/100 sit behind `/__migrate` returning 204.** UI = 0 test points (jury only, top 6, 20%).
In R1–R6 half the points are the *undescribed* dirty-data cases.

## Contracts (non-negotiable)

- Env: `CRM_TOKEN`, `DATABASE_URL`, `OPENROUTER_API_KEY`, `OPENROUTER_MODEL=openai/gpt-6-luna`, `OPENROUTER_BASE_URL`.
- Every call: `Authorization: Bearer $CRM_TOKEN` else **401**. Exempt: `GET /health`, export file links, UI pages.
- `GET /health` → `{"status":"ok","version":"2026-09","ui":{...}}`.
- `POST /__reset` → 204, **fast** (called hundreds of times): empty CRM + default props/pipelines/assoc types. Brambilla props/pipelines/list are created by the **migration**, not the reset.
- `POST /__migrate {"export_url"}` → download (http/https, query params, ignore filename) → migrate → **204 when done**. Hard limit 5 min, Railway can double → **target < 2 min on Railway**.
- `POST /__agente` → `{"reply": "<italiano>"}`, 60 s/turn, 4 concurrent, stateless.
- API paths are **date-versioned**: `/crm/objects/2026-09/{objectType}`, `/crm/associations/2026-09/...`, `/crm/properties/2026-09/...`, `/crm/pipelines/2026-09/...`, `/crm/lists/2026-09/...`, `/crm/imports/2026-09`, `/crm/exports/2026-09/...`. We also alias `/crm/v3/objects` and `/crm/v4`.
- Exact OpenAPI for every endpoint: `docs/hubspot/**.md` (offline mirror of the 2026-09 reference). **Grep it before guessing a shape.**
- Error JSON: `{"status":"error","message":...,"correlationId":uuid,"category":"VALIDATION_ERROR|OBJECT_NOT_FOUND|CONFLICT|INVALID_AUTHENTICATION"}`.
- Names from `starter/starter-v9/legacy/RICHIESTE.md` appendix are used **verbatim** by tests.

## Architecture (already scaffolded)

- FastAPI + asyncpg + Postgres. One generic store for all 12 object types.
- `objects(id, object_type, properties jsonb, created_at, updated_at, archived)` — property values stored as **strings**.
- `associations` stores **both directions** with HubSpot typeIds (`app/defaults.py`).
- `unique_values` enforces `hasUniqueValue` props (R7 `partita_iva` → 409). Contact email unique via partial index.
- `automation_log(rule, object_id)` PK → R10/R11 fire **once per deal**, atomically.
- **RULE: every write goes through `app/store.py`** (API, batch, assistant). Hooks R10/R11/R12 live in `app/hooks.py` and fire from there. The migration is the only exception (bulk COPY, no hooks — R10/R11 don't apply to history; R12 is computed in the migration).
- Updates merge in SQL: `properties = properties || $patch` under `SELECT … FOR UPDATE`. Never read-modify-write in Python.

## MoSCoW

### Must
1. Skeleton deployed + form check green on health/auth/reset. ✅ scaffold
2. Object engine, all types: CRUD ✅ scaffold · batch read/create/update/upsert/archive · **search** (filterGroups, operators EQ/NEQ/LT/LTE/GT/GTE/BETWEEN/IN/NOT_IN/HAS_PROPERTY/NOT_HAS_PROPERTY/CONTAINS_TOKEN, sorts, `after`, exact `total`, `query`) · associations (2026-09 PUT/DELETE + batch read/create/archive) · properties CRUD (`hasUniqueValue`) · pipelines CRUD · lists (+ memberships).
3. `/__migrate` < 2 min: parse cp1252 `;` → normalize → drop deleted → merge duplicates (latest `ultima_modifica` keeps the code; each field = latest non-empty) → `id_legacy` everywhere → bulk COPY.
4. Normalizers (see Data quirks). Half of R1–R6.
5. R8 `fatturato_2025` + `classe_cliente`, R9 list `Clienti dormienti` — computed in the migration.
6. R7 409 · R10 · R11 · R12 in the write path.
7. Concurrency-safe writes (atomic merge, unique email, upsert on conflict).
8. Assistant: tool loop on gpt-6-luna over `app/store.py`; Italian; `context.now`/`context.user`; ask when ambiguous; refuse rule violations; read back after writes; ≤ 8 steps, ~45 s.

### Should
- Dirty-case hunt for the other half of R1–R6 → log each case in `NOTES.md` (choice-sheet seed).
- Durability proof: restart + recount, 20-client GET-by-id load (p95 < 1 s), parallel upserts same email, paging exactly-once.
- UI (English, server-rendered, 4 pages): company page (fatturato, classe, contacts, deals, history), deals board, dormant list, tickets.
- Choice sheet 15:00–15:25.

### Could
- Exports API (async task + tokenless file link), imports API, merge endpoints, rate-limit headers, quotes.

### Won't
- Login/users UI, anything outside the brief's module links, a 2nd AI feature (banned), HubSpot name/logo (banned), burning the $10 key in dev loops.

## Lanes (parallel agents) — file ownership

| Lane | Owns | Done when |
|---|---|---|
| **A — Engine** | `app/routes/objects.py`, `app/routes/crm_meta.py`, `app/search.py`, `app/store.py`, `app/hooks.py` | batch + search + assoc + props + pipelines + lists conform to `docs/hubspot`; R7/R10/R11/R12 pass `tests/smoke.py` |
| **B — Migration** | `app/migrate/*` | `python -m app.migrate.cli starter/starter-v9/legacy/export.zip` loads the full export < 60 s locally; counts logged; `NOTES.md` cases |
| **C — Assistant** | `app/agent/*` | both examples in `starter/starter-v9/assistant/examples.md` work on a migrated DB, < 45 s, correct Italian reply |
| **D — UI** (last) | `app/ui/*` | 4 pages render on the migrated data |

Shared files (`app/main.py`, `app/db.py`, `app/schema.sql`, `app/defaults.py`): small additive edits only, tell the others.

## Lane B details — migration

Output per record: `properties.id_legacy` = Sinergia code of the surviving row.

| Sinergia | → | HubSpot |
|---|---|---|
| `aziende.csv` | companies | `name`, `domain` (bare domain), `city`, `state` (provincia), `partita_iva`, `hs_additional_domains` (merged sites, `;`-separated), `fatturato_2025`, `classe_cliente` |
| `contatti.csv` | contacts | `firstname`, `lastname`, `email` (valid only), `phone` (as is), `lifecyclestage` (Lead→`lead`, Prospect→`opportunity`, Cliente→`customer`, Ex cliente→`other`) + company assoc (279 + primary 1) |
| `opportunita.csv` | deals | `dealname`, `amount`, `deal_currency_code` (EUR default; no amount → no amount, no currency), `pipeline`, `dealstage`, `closedate`, `commerciale` (active users only) + assoc company (341+5) and contacts (3), each once |
| `righe_offerta.csv` | line_items | `name` (fallback product), `quantity`, `price`, `hs_discount_percentage` (0 default), `hs_product_id`; assoc deal (20). Deal with lines: `amount` = Σ round(qty·price·(1−disc/100), 2) |
| `listino.csv` | products | `hs_sku` `BF-01234`, `name`, `price`; same SKU = same product, latest price |
| `ticket.csv` | tickets | pipeline `Assistenza`, `subject`, `content`, `hs_ticket_priority`, `createdate`, `closed_date`, `assegnatario` + assoc contact (16) & company (339) |
| `attivita.csv` | notes/calls/emails/meetings | `hs_timestamp`, body prop, `autore`; assoc contact & deal |
| `storico_fasi.csv` | (input) | stage history — renewals are annual; may inform stages/dates |
| `utenti.csv` | (input) | `attivo` → who can follow deals/tickets |

Migration also creates: properties from the appendix, pipeline `Rinnovi` (4 stages w/ probabilities), ticket pipeline `Assistenza` (Aperto, In lavorazione, In attesa del cliente, Chiuso), relabels default deal pipeline (Vendite), list `Clienti dormienti` (companies, MANUAL/static is fine).

Speed: do everything in Python dicts, then `copy_records_to_table`. Pre-allocate ids with `store.reserve_ids`. Build heavy indexes after COPY if needed.

## Data quirks (measured on the export we got)

- `cancellato`: kept = `''`, `0`, `N`, `NO`; deleted = `S`, `s`, `SI`, `Sì`, `1`.
- Amounts mix IT and US formats: `€ -5.131,24`, `€24,376.08`, `EUR 223.370,86`, `1027956.14`, `488210,35`. Rule: last separator followed by exactly 2 digits = decimal.
- Dates: `18/01/2015`, `2018-05-17`, `20-04-2017`, `16/03/2014 00:00:00`, `13/01/2018 17:02`, blanks. Timezone = Europe/Rome.
- Currency: `EUR/Euro/€/eur/''` → EUR, `$/USD/usd` → USD, `£/GBP/gbp` → GBP.
- Pipeline: `vendite `, `VENDITE`, `Rinnovi`, `''` (→ Vendite).
- Stage: `06`, `06 VINTA`, `06 - Vinta`, ` vinta`, `Vinta`, `07 PERSA`, ` qualifica`, `01 - Contatto`… (also in `storico_fasi`).
- Contact `tipo`: 14 spellings (`Cliente`, ` Cliente `, `prospect `, `EX CLIENTE`, `Ex-cliente`…).
- Ticket priority: `1 - Bassa/BASSA/bassa`, `2 - Media/MEDIA/Normale`, `3 - Alta/ALTA`, `4 - Urgente`, `''` (→ none). Ticket stato: `RISOLTO/Chiuso/CHIUSO` → Chiuso, `Nuovo/Aperto` → Aperto, `Lavorazione/IN LAVORAZIONE` → In lavorazione, `Attesa cliente/IN ATTESA` → In attesa del cliente.
- Activity `tipo`: `NOTA/Appunto/nota` → note, `CHIAMATA/Telefonata/Tel.` → call, `E-mail/email/Mail` → email, `Incontro/Meeting` → meeting.
- SKU `BF38295` → `BF-38295`; qty `1 pz`; discount `15,0` vs `10%`; `unita` noise.
- P.IVA lives in `aziende.note` (~8.6k rows): `partita iva 84874 281912`, `P. IVA: IT 40969350707`, `p.iva IT11476373136` → 11 digits.
- Sites: `http://www.x.it/`, `www.x.eu`, `x.com` → bare domain; same domain = same company.
- Emails: uppercase, invalid strings → absent.
- Deal `contatti` is a `;` list inside the field: `"4675114;9275880"`.
- Refunds (storni): 831 negative-amount deals, only 331 titled "Storno…". **Decide** which defines a refund for R8 → NOTES.md.
- Users: `attivo` `s/SI/S` vs `N/NO/n`. Departed users follow nothing (R3/R5).
- Ticket `descrizione` sometimes starts `Da: someone@domain` (possible contact hint when `id_contatto` is missing).

## Lane C details — assistant

- Model `openai/gpt-6-luna` only, via OpenRouter, key `OPENROUTER_API_KEY`. **$10 for the whole day incl. evaluation.** No dev loops; every form check spends a call.
- Tools call `app/store.py` directly (so R7/R10/R11/R12 fire): `search_records`, `get_record` (with associations), `create_record`, `update_record`, `associate`, `list_pipelines`.
- System prompt: Italian, `context.now` is "today", `context.user` is the writer; "my customers" = companies on deals where `commerciale` = user or tickets where `assegnatario` = user. Multiple matches → ask. Violates a rule (dup P.IVA, inactive user, missing record) → don't act, explain. After a write, read back and state exactly what changed. Never touch other records.
- Attachments: CSV text with `;` separator in `messages[].attachments[].content`.
- Caps: ≤ 8 tool steps, abort and answer at ~45 s.

## Clock

| Time | Work |
|---|---|
| 10:55–11:30 | Scaffold, Railway deploy, first form check |
| 11:30–12:45 | A: batch/search/props/pipelines/lists · B: migration offline on export.zip |
| 12:45–13:15 | Merge, migrate on Railway, time it |
| 12:45–14:15 | C: assistant |
| 13:15–13:45 | A: R7, R10–R12 hardening · B: dirty cases → NOTES.md |
| 14:15–14:45 | Durability tests |
| 14:45–15:15 | D: UI pages · choice sheet from NOTES.md |
| 15:20 | Last push, final form check, hands off |

## Commands

```bash
# local Postgres
docker compose up -d db
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/crm CRM_TOKEN=dev
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
BASE_URL=http://localhost:8000 CRM_TOKEN=dev python tests/smoke.py

# local migration (serve the zip, then call the endpoint)
python -m http.server 9999 --directory starter/starter-v9/legacy &
curl -X POST localhost:8000/__migrate -H "Authorization: Bearer dev" -H 'content-type: application/json' \
  -d '{"export_url":"http://localhost:9999/export.zip"}'
```

Railway: service from this repo (Dockerfile), add a Postgres service, set `DATABASE_URL=${{Postgres.DATABASE_URL}}`, `CRM_TOKEN`, `OPENROUTER_API_KEY`; region EU West; generate a domain; register it on the platform.
