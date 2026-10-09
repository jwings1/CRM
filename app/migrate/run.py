"""POST /__migrate entry point. Lane B owns this package.

Pipeline (target < 60 s locally, < 2 min on Railway):
  1. read_export (thread)            -> raw rows per file
  2. transform (thread, pure Python)  -> normalized, deduplicated records + associations + derived R8/R9/R12
  3. load (one connection, one txn)   -> property defs, pipelines, list, then COPY objects/associations/unique_values

Rules: see PLAN.md "Lane B details" and "Data quirks". No hooks here (R10/R11 don't apply to history).
"""
from __future__ import annotations

import asyncio

from . import setup
from .csvio import read_export


def transform(data: dict[str, list[dict]]) -> dict:
    """Pure function: raw CSV rows -> records to load. TODO Lane B."""
    return {"stats": {k: len(v) for k, v in data.items()}}


async def load(conn, result: dict) -> None:
    """COPY everything in. TODO Lane B.
    Use store.reserve_ids(conn, n) for ids and
    conn.copy_records_to_table('objects', records=[(id, type, props_dict, created_at, updated_at)],
                               columns=['id','object_type','properties','created_at','updated_at'])."""
    return None


async def run(pool, zip_bytes: bytes) -> dict:
    data = await asyncio.to_thread(read_export, zip_bytes)
    result = await asyncio.to_thread(transform, data)
    async with pool.acquire() as conn:
        async with conn.transaction():
            result["ids"] = await setup.ensure(conn)   # properties, pipelines, list (appendix)
            await load(conn, result)
    return result.get("stats", {})
