"""Run the migration locally without HTTP:
    python -m app.migrate.cli starter/starter-v9/legacy/export.zip          # transform only
    python -m app.migrate.cli starter/starter-v9/legacy/export.zip --load   # reset + load into DATABASE_URL
"""
from __future__ import annotations

import asyncio
import sys
import time

from .. import db
from .csvio import read_export
from .run import run, transform


async def main(path: str, load: bool) -> None:
    raw = open(path, "rb").read()
    t0 = time.monotonic()
    if not load:
        data = read_export(raw)
        t1 = time.monotonic()
        res = transform(data)
        print(f"read {t1 - t0:.1f}s transform {time.monotonic() - t1:.1f}s", res.get("stats"))
        return
    await db.connect()
    await db.reset()
    stats = await run(db.pool, raw)
    print(f"migrated in {time.monotonic() - t0:.1f}s", stats)
    await db.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], "--load" in sys.argv))
