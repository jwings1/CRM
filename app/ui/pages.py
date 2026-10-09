"""Jury UI (English, server-rendered, no auth: a browser can't send the bearer token).
Lane D owns this. Pages the jury opens: company page (fatturato_2025, classe_cliente,
contacts, deals, history), deals board by stage, dormant customers list, tickets.
No HubSpot name or logo anywhere."""
from __future__ import annotations

import html

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from .. import config

router = APIRouter()

CSS = """
:root{--bg:#f7f7f5;--fg:#1b1b1b;--mut:#6b6b6b;--card:#fff;--line:#e4e4e0;--acc:#0b6e4f}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--fg:#ececec;--mut:#9a9a9a;--card:#1d1d1d;--line:#2c2c2c;--acc:#4fd1a5}}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,sans-serif;background:var(--bg);color:var(--fg)}
nav{display:flex;gap:16px;padding:14px 20px;border-bottom:1px solid var(--line);background:var(--card)}
nav a{color:var(--fg);text-decoration:none}nav b{color:var(--acc);margin-right:12px}
main{padding:20px;max-width:1200px;margin:0 auto}.mut{color:var(--mut)}
"""


def layout(title: str, body: str) -> HTMLResponse:
    links = "".join(f'<a href="{r}">{html.escape(k.title())}</a>' for k, r in config.UI_ROUTES.items())
    return HTMLResponse(
        f"<!doctype html><html lang=en><head><meta charset=utf-8>"
        f"<meta name=viewport content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title>"
        f"<style>{CSS}</style></head><body><nav><b>Brambilla CRM</b>{links}</nav><main>{body}</main></body></html>")


def _placeholder(module: str):
    async def page():
        return layout(module.title(), f"<h1>{html.escape(module.title())}</h1><p class=mut>Coming soon.</p>")
    return page


for _module, _route in config.UI_ROUTES.items():
    router.add_api_route(_route, _placeholder(_module), methods=["GET"], response_class=HTMLResponse)


@router.get("/", response_class=HTMLResponse)
async def home():
    return layout("Brambilla CRM", "<h1>Brambilla CRM</h1><p class=mut>Pick a module above.</p>")
