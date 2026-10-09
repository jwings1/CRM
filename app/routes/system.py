"""Race contract endpoints: /health, /__reset, /__migrate, /__agente."""
from __future__ import annotations

import logging
import time

import httpx
from fastapi import APIRouter, Request, Response

from .. import config, db
from ..agent import run as agent
from ..errors import ApiError
from ..migrate import run as migrate
from .objects import read_json

log = logging.getLogger("crm")
router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "version": config.API_VERSION, "ui": config.UI_ROUTES}


@router.post("/__reset", status_code=204)
async def reset():
    await db.reset()
    return Response(status_code=204)


async def download(url: str) -> bytes:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=httpx.Timeout(120, connect=15)) as client:
            r = await client.get(url)
    except httpx.HTTPError as e:
        raise ApiError(400, f"could not download export_url: {type(e).__name__}: {e}")
    if r.status_code >= 400:
        raise ApiError(400, f"export_url returned HTTP {r.status_code}")
    return r.content


@router.post("/__migrate", status_code=204)
async def do_migrate(request: Request):
    body = await read_json(request)
    url = (body or {}).get("export_url")
    if not url:
        raise ApiError(400, "export_url is required")
    t0 = time.monotonic()
    data = await download(url)
    t1 = time.monotonic()
    stats = await migrate.run(db.pool, data, started=t0)
    log.warning("migrate: download %.1fs, migrate %.1fs, stats=%s", t1 - t0, time.monotonic() - t1, stats)
    return Response(status_code=204)


@router.post("/__agente")
async def agente(request: Request):
    body = await read_json(request)
    if not isinstance(body, dict) or not isinstance(body.get("messages"), list):
        raise ApiError(400, "messages is required")
    return {"reply": await agent.reply(body)}
