# Company Brain and assistant

The assistant uses the application's production `DATABASE_URL` and asyncpg pool.
Startup creates the additive KB tables and inserts missing seed documents: one
document per R1–R13, general rules with the appendix, and assistant context.
Existing published content is preserved. CRM migration also persists the employee
roster; live CRM changes and KB publications are visible on subsequent requests.

Configure `CRM_TOKEN`, `DATABASE_URL`, `OPENROUTER_API_KEY`, and
`OPENROUTER_MODEL=openai/gpt-6-luna`. Test through the UI or authenticated
`POST /__agente`, supplying `context.user`, an ISO timestamp in `context.now`,
and conversation `messages`. Model calls are bounded to eight tool executions
and a 45-second turn. Writes use the store and return verified record changes.

## Publish reviewed knowledge

Use a directory containing Markdown files and a `manifest.json` with a
`documents` array. See `data/kb/manifest.json` for the format. Each entry includes
`doc_id`, `title`, `category`, `source`, `file`, and optional `metadata`, `links`,
and `expected_revision`. Use `expected_revision: 0` for a new document and the
observed current revision when editing an existing document.

```bash
python -m app.agent.kb_cli list
python -m app.agent.kb_cli import /path/to/reviewed-kb
python -m app.agent.kb_cli link BKB-R11 123 --revision 1 --relation governs
python -m app.agent.kb_cli archive BKB-R11 --revision 2
```

Run against the intended `DATABASE_URL`. An import publishes all documents in
one transaction; identical content is a no-op and stale revisions fail with a
conflict. Content, metadata, links, immutable revision snapshots, and weighted
Italian search indexes update together. No worker restart is required.
Reset preserves documents and revisions while clearing CRM links and employees.

## Validation

Integration tests require an isolated Postgres database whose name includes
`kb_test`; they reset its CRM data. They mock model completion and cover live
publication, revisions, search, graph links, migration, assignment checks,
automations, CSV rollback, exact aggregates, concurrent conversations, and
deadlines.

```bash
KB_TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/kb_test \
  CRM_TOKEN=dev python -m unittest discover -s tests -p test_company_brain.py -v
```
