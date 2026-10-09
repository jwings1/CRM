"""App entry: uvicorn app.main:app"""
from __future__ import annotations

import hmac
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import config, db
from .errors import ApiError, error_body, error_response
from .routes import associations, crm_meta, lists, objects, system
from .ui import pages

log = logging.getLogger("crm")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.warning("boot: CRM_TOKEN %s, OPENROUTER_API_KEY %s, DATABASE_URL host %s",
                "set" if config.CRM_TOKEN else "MISSING", "set" if config.OPENROUTER_API_KEY else "MISSING",
                config.DATABASE_URL.split("@")[-1].split("/")[0])
    await db.connect()
    yield
    await db.close()


app = FastAPI(title="Brambilla CRM", lifespan=lifespan, default_response_class=ORJSONResponse,
              docs_url=None, redoc_url=None, openapi_url=None)

# ---------------------------------------------------------------- auth (pure ASGI, cheap)
_UI_PREFIXES = tuple(config.UI_ROUTES.values())
_TOKEN = config.CRM_TOKEN.encode()


def _public(method: str, path: str) -> bool:
    if path == "/health" or path.startswith("/exports/files/"):
        return True
    if path.startswith("/ui-api/"):  # read-only proxy for the UI; enforces its own allowlist
        return True
    if method in ("GET", "HEAD") and (path == "/" or path.startswith("/static/")
                                      or any(path == p or path.startswith(p + "/") for p in _UI_PREFIXES)):
        return True
    return False


class BearerAuth:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or _public(scope["method"], scope["path"]):
            return await self.app(scope, receive, send)
        auth = b""
        for k, v in scope["headers"]:
            if k == b"authorization":
                auth = v
                break
        ok = bool(_TOKEN) and auth[:7].lower() == b"bearer " and hmac.compare_digest(auth[7:].strip(), _TOKEN)
        if not ok:
            resp = ORJSONResponse(error_body(401, "Authentication credentials not found.", "INVALID_AUTHENTICATION"),
                                  status_code=401)
            return await resp(scope, receive, send)
        return await self.app(scope, receive, send)


app.add_middleware(BearerAuth)


# ---------------------------------------------------------------- errors -> HubSpot shape
@app.exception_handler(ApiError)
async def _api_error(request: Request, exc: ApiError):
    return error_response(exc.status, exc.message, category=exc.category, errors=exc.errors,
                          context=exc.context, sub_category=exc.sub_category)


@app.exception_handler(RequestValidationError)
async def _validation(request: Request, exc: RequestValidationError):
    return error_response(400, "Invalid input: " + "; ".join(str(e.get("msg")) for e in exc.errors()))


@app.exception_handler(StarletteHTTPException)
async def _http(request: Request, exc: StarletteHTTPException):
    return error_response(exc.status_code, str(exc.detail))


@app.exception_handler(Exception)
async def _boom(request: Request, exc: Exception):
    log.exception("unhandled error on %s %s", request.method, request.url.path)
    return error_response(500, f"Internal error: {type(exc).__name__}", category="INTERNAL_ERROR")


# ---------------------------------------------------------------- routes
app.include_router(system.router)
for prefix in (f"/crm/objects/{config.API_VERSION}", "/crm/v3/objects"):
    app.include_router(objects.router, prefix=prefix)
for prefix in (f"/crm/properties/{config.API_VERSION}", "/crm/v3/properties"):
    app.include_router(crm_meta.properties_router, prefix=prefix)
for prefix in (f"/crm/pipelines/{config.API_VERSION}", "/crm/v3/pipelines"):
    app.include_router(crm_meta.pipelines_router, prefix=prefix)
for prefix in (f"/crm/associations/{config.API_VERSION}", "/crm/v4/associations"):
    app.include_router(associations.router, prefix=prefix)
for prefix in (f"/crm/lists/{config.API_VERSION}", "/crm/v3/lists"):
    app.include_router(lists.router, prefix=prefix)
app.include_router(pages.router)
