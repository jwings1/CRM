"""POST /__migrate entry point.

  1. read_export (thread)               raw rows per file
  2. setup.ensure (db)                  Brambilla properties, pipelines, list  -> ids
  3. transform (thread, pure Python)    normalized + merged records, associations, R8/R9/R12
  4. load                               COPY objects / unique_values / list members (one txn)
                                        + associations COPY'd in parallel on other pool connections

No hooks here: R10/R11 don't apply to history; R12 is computed in transform.
"""
from __future__ import annotations

import asyncio
import logging
import time

from .. import store
from ..defaults import lastmod_prop
from . import setup
from .csvio import read_export
from .transform import transform

log = logging.getLogger("crm")

_CREATED_PROP = {"contacts": "createdate", "companies": "createdate", "deals": "createdate", "tickets": "createdate",
                 "products": "createdate", "line_items": "createdate"}
_ASSOC_COLS = ["from_type", "from_id", "to_type", "to_id", "category", "type_id"]
ASSOC_WORKERS = 3


async def load_objects(conn, res: dict, base: int) -> None:
    now = store.utcnow()
    now_iso = store.iso(now)
    by_local: dict[int, dict] = {}
    records = []
    for otype, items in res["objects"].items():
        ck = _CREATED_PROP.get(otype, "hs_createdate")
        lm = lastmod_prop(otype)
        for local, props, created in items:
            oid = base + local
            props["hs_object_id"] = str(oid)
            props.setdefault(ck, store.iso(created) if created else now_iso)
            props[lm] = now_iso
            by_local[local] = props
            records.append((oid, otype, props, created or now, now))
    for local, prop, target in res["refs"]:
        by_local[local][prop] = str(base + target)
    await conn.copy_records_to_table(
        "objects", records=records, columns=["id", "object_type", "properties", "created_at", "updated_at"])
    if res["uniques"]:
        await conn.copy_records_to_table(
            "unique_values", records=[(t, p, v, base + i) for t, p, v, i in res["uniques"]],
            columns=["object_type", "property", "value", "object_id"])
    if res["dormant"]:
        await conn.copy_records_to_table(
            "list_memberships", records=[(res["ids"]["dormienti_list_id"], base + c, now) for c in res["dormant"]],
            columns=["list_id", "record_id", "added_at"])


async def _copy_assocs(pool, rows: list) -> None:
    async with pool.acquire() as conn:
        await conn.copy_records_to_table("associations", records=rows, columns=_ASSOC_COLS)


async def run(pool, zip_bytes: bytes) -> dict:
    t0 = time.monotonic()
    data = await asyncio.to_thread(read_export, zip_bytes)
    t1 = time.monotonic()
    async with pool.acquire() as conn:
        async with conn.transaction():
            ids = await setup.ensure(conn)
        res = await asyncio.to_thread(transform, data, ids)
        del data
        res["ids"] = ids
        t2 = time.monotonic()
        base = (await store.reserve_ids(conn, res["n"])).start
        rows = [(ft, base + fi, tt, base + ti, "HUBSPOT_DEFINED", tid) for ft, fi, tt, ti, tid in res["assocs"]]
        res["assocs"] = None
        chunks = [rows[i::ASSOC_WORKERS] for i in range(ASSOC_WORKERS)]
        del rows

        async def objects_txn():
            async with conn.transaction():
                await load_objects(conn, res, base)

        await asyncio.gather(objects_txn(), *[_copy_assocs(pool, c) for c in chunks])
        t3 = time.monotonic()
        await conn.execute("ANALYZE objects; ANALYZE associations")
    t4 = time.monotonic()
    stats = res["stats"]
    stats["time"] = {"read": round(t1 - t0, 1), "transform": round(t2 - t1, 1), "load": round(t3 - t2, 1),
                     "analyze": round(t4 - t3, 1)}
    log.warning("migration stats: %s", stats)
    return stats
