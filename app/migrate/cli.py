"""Run the migration locally without HTTP:
    python -m app.migrate.cli starter/starter-v9/legacy/export.zip          # transform only, print stats
    python -m app.migrate.cli starter/starter-v9/legacy/export.zip --load   # reset + full load into DATABASE_URL
"""
from __future__ import annotations

import asyncio
import json
import sys
import time

from .. import db
from .csvio import read_export
from .run import run
from .transform import transform

FAKE_IDS = {
    "rinnovi": {"__pipeline__": "1000", "Da rinnovare": "1001", "In trattativa": "1002", "Rinnovato": "1003", "Non rinnovato": "1004"},
    "assistenza": {"__pipeline__": "1005", "Aperto": "1006", "In lavorazione": "1007", "In attesa del cliente": "1008", "Chiuso": "1009"},
    "dormienti_list_id": 1,
}


async def main(path: str, load: bool) -> None:
    raw = open(path, "rb").read()
    t0 = time.monotonic()
    if not load:
        data = read_export(raw)
        t1 = time.monotonic()
        res = transform(data, FAKE_IDS)
        print(f"read {t1 - t0:.1f}s transform {time.monotonic() - t1:.1f}s")
        print(json.dumps(res["stats"], indent=1, sort_keys=True))
        return
    await db.connect()
    await db.reset()
    stats = await run(db.pool, raw)
    print(f"migrated in {time.monotonic() - t0:.1f}s")
    print(json.dumps(stats, indent=1, sort_keys=True))
    await db.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], "--load" in sys.argv))
