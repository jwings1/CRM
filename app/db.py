"""Postgres pool, schema bootstrap, defaults seeding and the fast reset."""
from __future__ import annotations

import pathlib

import asyncpg
import orjson

from . import config
from .defaults import DEFAULT_PIPELINES, OBJECT_TYPES, property_rows

pool: asyncpg.Pool | None = None

SCHEMA = (pathlib.Path(__file__).parent / "schema.sql").read_text()
KB_SCHEMA = (pathlib.Path(__file__).parent / "agent" / "kb_schema.sql").read_text()

TABLES = (
    "objects, associations, unique_values, property_groups, property_defs, pipelines, "
    "pipeline_stages, lists, list_memberships, automation_log, exports, kb_document_links, agent_users"
)


def _jsonb_enc(v) -> bytes:
    # binary jsonb wire format = version byte 1 + JSON text. Binary is required by COPY.
    return b"\x01" + orjson.dumps(v)


def _jsonb_dec(b: bytes):
    return orjson.loads(b[1:])


async def _init_conn(conn: asyncpg.Connection) -> None:
    # Pass Python dicts/lists for jsonb params, never pre-encoded JSON strings.
    await conn.set_type_codec("jsonb", encoder=_jsonb_enc, decoder=_jsonb_dec, schema="pg_catalog", format="binary")
    await conn.set_type_codec("json", encoder=orjson.dumps, decoder=orjson.loads, schema="pg_catalog", format="binary")


async def connect() -> asyncpg.Pool:
    global pool
    import asyncio
    import logging
    log = logging.getLogger("crm")
    host = config.DATABASE_URL.split("@")[-1].split("/")[0]
    for attempt in range(30):  # Railway private network / Postgres may need a few seconds at boot
        try:
            pool = await asyncpg.create_pool(
                config.DATABASE_URL, min_size=config.DB_POOL_MIN, max_size=config.DB_POOL_MAX,
                init=_init_conn, command_timeout=300,
            )
            break
        except (OSError, asyncpg.PostgresError) as e:
            log.warning("db connect to %s failed (attempt %d): %r", host, attempt + 1, e)
            if attempt == 29:
                raise
            await asyncio.sleep(2)
    async with pool.acquire() as conn:
        # one boot at a time when several workers start together
        await conn.execute("SELECT pg_advisory_lock(424242)")
        try:
            await conn.execute(SCHEMA)
            await conn.execute(KB_SCHEMA)
            if not await conn.fetchval("SELECT EXISTS (SELECT 1 FROM property_defs)"):
                async with conn.transaction():
                    await seed(conn)
            from .agent.kb import seed_documents
            await seed_documents(conn)
        finally:
            await conn.execute("SELECT pg_advisory_unlock(424242)")
    return pool


async def close() -> None:
    if pool is not None:
        await pool.close()


# ---- seed records (built once) ------------------------------------------------
_GROUP_COLS = ["object_type", "name", "label", "display_order"]
_PROP_COLS = ["object_type", "name", "label", "type", "field_type", "group_name", "options",
              "display_order", "has_unique_value", "calculated", "read_only", "hubspot_defined"]
_PIPE_COLS = ["object_type", "id", "label", "display_order"]
_STAGE_COLS = ["object_type", "pipeline_id", "id", "label", "display_order", "metadata"]

_GROUPS = [(t, f"{s}information", f"{s.replace('_', ' ').title()} information", 0) for t, (_, s) in OBJECT_TYPES.items()]
_PROPS = [tuple(r[c] for c in _PROP_COLS) for t in OBJECT_TYPES for r in property_rows(t)]
_PIPES = [(p["object_type"], p["id"], p["label"], p["display_order"]) for p in DEFAULT_PIPELINES]
_STAGES = [
    (p["object_type"], p["id"], sid, label, i, meta)
    for p in DEFAULT_PIPELINES for i, (sid, label, meta) in enumerate(p["stages"])
]


async def seed(conn: asyncpg.Connection) -> None:
    await conn.copy_records_to_table("property_groups", records=_GROUPS, columns=_GROUP_COLS)
    await conn.copy_records_to_table("property_defs", records=_PROPS, columns=_PROP_COLS)
    await conn.copy_records_to_table("pipelines", records=_PIPES, columns=_PIPE_COLS)
    await conn.copy_records_to_table("pipeline_stages", records=_STAGES, columns=_STAGE_COLS)


async def reset() -> None:
    """Fresh HubSpot account. Called hundreds of times by the tests: keep it fast."""
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                f"TRUNCATE {TABLES};"
                " ALTER SEQUENCE object_id_seq RESTART;"
                " ALTER SEQUENCE list_id_seq RESTART;"
                " ALTER SEQUENCE pipeline_id_seq RESTART;"
            )
            await seed(conn)
