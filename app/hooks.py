"""CRM automations, fired synchronously by store.create/store.update (same txn).

R10  deal enters closedwon in the default (Vendite) pipeline -> ticket "Avvio fornitura - <dealname>"
R11  deal enters closedlost in the default pipeline          -> task "Richiamare: <dealname>" due +180 days
R12  contact with no company + email domain = an existing company's domain/additional domain -> associate

Not applied to the migrated history (the migration does not call the store).
"""
from __future__ import annotations

from . import store

SALES_PIPELINE = "default"


async def after_write(conn, otype: str, oid: int, before: dict | None, after: dict, *, created: bool,
                      effective_now=None) -> None:
    if otype == "deals":
        await _deal_rules(conn, oid, before, after, created, effective_now)
    elif otype == "contacts":
        await _r12(conn, oid, before, after, created)


def _entered(before: dict | None, after: dict, created: bool, stage: str) -> bool:
    if (after.get("pipeline") or SALES_PIPELINE) != SALES_PIPELINE or after.get("dealstage") != stage:
        return False
    if created or before is None:
        return True
    return before.get("dealstage") != stage or (before.get("pipeline") or SALES_PIPELINE) != SALES_PIPELINE


async def _once(conn, rule: str, oid: int) -> bool:
    return bool(await conn.fetchval(
        "INSERT INTO automation_log (rule, object_id) VALUES ($1, $2) ON CONFLICT DO NOTHING RETURNING 1", rule, oid))


async def _deal_rules(conn, oid, before, after, created, effective_now=None) -> None:
    if _entered(before, after, created, "closedwon") and await _once(conn, "R10", oid):
        await _r10(conn, oid, after)
    if _entered(before, after, created, "closedlost") and await _once(conn, "R11", oid):
        await _r11(conn, oid, after, effective_now)


async def _assistenza(conn) -> tuple[str, str]:
    """(pipeline id, 'Aperto' stage id) of the ticket pipeline created by the migration."""
    row = await conn.fetchrow(
        "SELECT p.id AS pid, s.id AS sid FROM pipelines p JOIN pipeline_stages s "
        "ON s.object_type = p.object_type AND s.pipeline_id = p.id "
        "WHERE p.object_type='tickets' AND p.label='Assistenza' AND NOT p.archived AND NOT s.archived "
        "ORDER BY (s.label = 'Aperto') DESC, s.display_order LIMIT 1")
    if row:
        return row["pid"], row["sid"]
    return "0", "1"


async def _r10(conn, oid: int, deal: dict) -> None:
    pid, sid = await _assistenza(conn)
    props = {
        "subject": f"Avvio fornitura - {deal.get('dealname') or ''}",
        "hs_pipeline": pid,
        "hs_pipeline_stage": sid,
    }
    if deal.get("commerciale"):
        props["assegnatario"] = deal["commerciale"]
    companies = await conn.fetch(
        "SELECT DISTINCT to_id FROM associations WHERE from_id=$1 AND to_type='companies'", oid)
    assocs = [("deals", oid, [("HUBSPOT_DEFINED", 28)])]
    assocs += [("companies", r["to_id"], [("HUBSPOT_DEFINED", 339)]) for r in companies]
    await store.create(conn, "tickets", props, assocs, validate=False, run_hooks=False)


async def _r11(conn, oid: int, deal: dict, effective_now=None) -> None:
    props = {
        "hs_task_subject": f"Richiamare: {deal.get('dealname') or ''}",
        "hs_timestamp": store.days_from(effective_now or store.utcnow(), 180),
        "hs_task_status": "NOT_STARTED",
        "hs_task_type": "CALL",
    }
    await store.create(conn, "tasks", props, [("deals", oid, [("HUBSPOT_DEFINED", 216)])],
                       validate=False, run_hooks=False)


async def _r12(conn, oid: int, before: dict | None, after: dict, created: bool) -> None:
    email = (after.get("email") or "").strip().lower()
    if "@" not in email:
        return
    if not created and (before or {}).get("email", "").strip().lower() == email:
        return
    if await conn.fetchval("SELECT 1 FROM associations WHERE from_id=$1 AND to_type='companies' LIMIT 1", oid):
        return
    domain = store.bare_domain(email.rsplit("@", 1)[1])
    cid = await conn.fetchval(
        "SELECT id FROM objects WHERE object_type='companies' AND NOT archived AND ("
        " regexp_replace(lower(coalesce(properties->>'domain','')), '^(https?://)?(www\\.)?', '') = $1"
        " OR $1 = ANY(string_to_array(regexp_replace(lower(coalesce(properties->>'hs_additional_domains','')),"
        "   '(https?://)?(www\\.)?', '', 'g'), ';'))"
        ") ORDER BY id LIMIT 1", domain)
    if cid:
        await store.associate(conn, "contacts", oid, "companies", cid, [("HUBSPOT_DEFINED", 1)], check=False)
