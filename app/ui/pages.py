"""Interface (English). A static single-page app in app/ui/static/, served on the public UI routes.

The UI uses /ui-api/* to forward reads and assistant requests with the configured
server token. Other writes still require a bearer token. No HubSpot name or logo anywhere."""
from __future__ import annotations

import re
from pathlib import Path

import httpx
from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse, RedirectResponse

from .. import config

router = APIRouter()
STATIC = Path(__file__).parent / "static"
_TYPES = "(companies|contacts|deals|tickets|notes|calls|emails|meetings|tasks|products|line_items)"
_READ_POST = re.compile(
    rf"^/crm/v3/objects/{_TYPES}/(search|batch/read)$|^/crm/v4/associations/{_TYPES}/{_TYPES}/batch/read$|^/crm/v3/lists/search$")
_READ_GET = re.compile(r"^/crm/v3/(objects|pipelines|lists)/")


def _index() -> FileResponse:
    return FileResponse(STATIC / "index.html", media_type="text/html", headers={"Cache-Control": "no-cache"})


def _page():
    async def page():
        return _index()
    return page


for _route in config.UI_ROUTES.values():
    router.add_api_route(_route, _page(), methods=["GET"])
    router.add_api_route(_route + "/{rest:path}", _page(), methods=["GET"])


@router.get("/")
async def home():
    return RedirectResponse("/companies")


@router.get("/static/ui/{name}")
async def asset(name: str):
    f = (STATIC / name).resolve()
    if STATIC.resolve() not in f.parents or not f.is_file():
        return Response(status_code=404)
    return FileResponse(f, headers={"Cache-Control": "no-cache"})


@router.api_route("/ui-api/{path:path}", methods=["GET", "POST"])
async def read_proxy(path: str, request: Request):
    p = "/" + path
    assistant = request.method == "POST" and p == "/__agente"
    if assistant:
        origin = request.headers.get("origin")
        expected_origin = f"{request.url.scheme}://{request.url.netloc}"
        if (origin and origin != expected_origin) or request.headers.get("sec-fetch-site") == "cross-site":
            return Response(status_code=403)
        if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
            return Response(status_code=415)
    ok = assistant or (request.method == "GET" and _READ_GET.match(p)) or (request.method == "POST" and _READ_POST.match(p))
    if not ok:
        return Response('{"status":"error","message":"Read-only endpoint","category":"INVALID_AUTHENTICATION"}',
                        status_code=401, media_type="application/json")
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=request.app), base_url="http://crm",
                                 headers={"Authorization": f"Bearer {config.CRM_TOKEN}"}) as c:
        r = await c.request(request.method, p, params=request.query_params, content=await request.body(),
                            headers={"content-type": "application/json"})
    return Response(r.content, status_code=r.status_code, media_type="application/json")
