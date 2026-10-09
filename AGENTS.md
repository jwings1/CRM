# AGENTS.md — rules for every coding agent in this repo

Read `PLAN.md` first (scoring, contracts, lanes, data quirks). The brief is `starter/starter-v9/BRIEF.md`,
Brambilla's requests `starter/starter-v9/legacy/RICHIESTE.md` (names in its appendix are used verbatim by tests).

## Hard rules
1. **All record writes go through `app/store.py`** (`create`, `update`, `archive`, `associate`). Never write
   `objects`/`associations` with raw SQL outside `store.py`, except the bulk migration in `app/migrate/`.
   This is what makes R7/R10/R11/R12 fire for the API *and* the assistant.
2. Property values are **strings** in `objects.properties`. Pass Python dicts for jsonb params (binary codec in `db.py`).
3. Updates merge in SQL (`properties || $patch`) under `FOR UPDATE`. No read-modify-write in Python.
4. API paths are date-versioned: `/crm/objects/2026-09/...`, `/crm/associations/2026-09/...`,
   `/crm/properties/2026-09/...`, `/crm/pipelines/2026-09/...`, `/crm/lists/2026-09/...`.
   Before implementing an endpoint, **grep its OpenAPI in `docs/hubspot/`** (e.g. `docs/hubspot/crm/objects/contacts/search/`).
5. Errors: raise `ApiError(status, message, category)` from `app/errors.py` → HubSpot error JSON.
6. Stay in your lane's files (table in PLAN.md). Shared files: small additive edits only.
7. Never commit `.env`, tokens or keys. Never call the OpenRouter model in loops ($10 for the whole day).
8. No HubSpot name or logo in the UI.

## Run
```bash
docker compose up -d db
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/crm CRM_TOKEN=dev
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
BASE_URL=http://localhost:8000 CRM_TOKEN=dev python tests/smoke.py   # must stay green
DATABASE_URL=... python tests/bench.py                                  # concurrency + load + COPY speed
python -m app.migrate.cli starter/starter-v9/legacy/export.zip [--load]
```

## Measured on the scaffold (local)
- `/__reset`: ~40 ms (60 ms after 600k rows). 20 parallel clients GET-by-id: p95 ~90 ms.
- `copy_records_to_table` 600k objects ≈ 10 s, 600k association rows ≈ 4.5 s → the migration budget is in Python
  parsing/normalizing, not in Postgres.

## Log findings
Every dirty-data case you handle goes in `NOTES.md` (file, column, example row, count, rule applied).
It becomes the choice sheet at 15:00.
