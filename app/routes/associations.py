"""Associations API (2026-09 / v4 shapes). Mounted at /crm/associations/2026-09 and /crm/v4/associations."""
from __future__ import annotations

from fastapi import APIRouter, Request, Response
from fastapi.responses import ORJSONResponse

from .. import db, store
from ..defaults import ASSOC_TYPES, DEFAULT_ASSOC, INVERSE, OBJECT_TYPES
from ..errors import ApiError
from .objects import read_json

router = APIRouter()


def _types(ft: str, tt: str):
    return [a for a in ASSOC_TYPES if a["from"] == ft and a["to"] == tt]


def _label(type_id: int, category: str):
    if category != "HUBSPOT_DEFINED":
        return None
    return next((a["label"] for a in ASSOC_TYPES if a["type_id"] == type_id), None)


def _batch(results, errors=None, status=200):
    now = store.now_iso()
    body = {"status": "COMPLETE", "results": results, "startedAt": now, "completedAt": now}
    if errors:
        body["numErrors"], body["errors"] = len(errors), errors
        status = 207
    return ORJSONResponse(body, status_code=status)


def _ids(inp, key):
    v = (inp or {}).get(key)
    if isinstance(v, dict):
        v = v.get("id")
    try:
        return int(v)
    except (TypeError, ValueError):
        raise ApiError(400, f"Invalid {key} id: {v}")


@router.get("/{fromObjectType}/{toObjectType}/labels")
async def labels(fromObjectType: str, toObjectType: str):
    ft, tt = store.resolve_type(fromObjectType), store.resolve_type(toObjectType)
    return {"results": [{"category": a["category"], "typeId": a["type_id"], "label": a["label"]} for a in _types(ft, tt)]}


@router.post("/{fromObjectType}/{toObjectType}/batch/read")
async def batch_read(fromObjectType: str, toObjectType: str, request: Request):
    ft, tt = store.resolve_type(fromObjectType), store.resolve_type(toObjectType)
    body = await read_json(request)
    results, missing = [], []
    async with db.pool.acquire() as conn:
        for inp in body.get("inputs") or []:
            fid = _ids(inp, "id")
            rows = await store.assoc_rows(conn, fid, tt)
            if not rows:
                exists = await conn.fetchval("SELECT 1 FROM objects WHERE id=$1 AND object_type=$2 AND NOT archived", fid, ft)
                if not exists:
                    missing.append(str(fid))
                continue
            grouped: dict[int, list] = {}
            for r in rows:
                grouped.setdefault(r["to_id"], []).append(
                    {"category": r["category"], "typeId": r["type_id"], "label": _label(r["type_id"], r["category"])})
            results.append({"from": {"id": str(fid)},
                            "to": [{"toObjectId": k, "associationTypes": v} for k, v in grouped.items()]})
    errors = [{"status": "error", "category": "OBJECT_NOT_FOUND", "message": "No associations found",
               "context": {"fromObjectId": missing}}] if missing else None
    return _batch(results, errors)


@router.post("/{fromObjectType}/{toObjectType}/batch/create")
async def batch_create(fromObjectType: str, toObjectType: str, request: Request):
    ft, tt = store.resolve_type(fromObjectType), store.resolve_type(toObjectType)
    body = await read_json(request)
    results = []
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            for inp in body.get("inputs") or []:
                fid, tid = _ids(inp, "from"), _ids(inp, "to")
                types = [(t.get("associationCategory", "HUBSPOT_DEFINED"), int(t["associationTypeId"]))
                         for t in inp.get("types") or []] or None
                await store.associate(conn, ft, fid, tt, tid, types)
                rows = await conn.fetch("SELECT category, type_id FROM associations WHERE from_id=$1 AND to_id=$2", fid, tid)
                results.append({"fromObjectTypeId": OBJECT_TYPES[ft][0], "fromObjectId": fid,
                                "toObjectTypeId": OBJECT_TYPES[tt][0], "toObjectId": tid,
                                "labels": [l for l in (_label(r["type_id"], r["category"]) for r in rows) if l]})
    return _batch(results, status=201)


@router.post("/{fromObjectType}/{toObjectType}/batch/associate/default")
async def batch_default(fromObjectType: str, toObjectType: str, request: Request):
    ft, tt = store.resolve_type(fromObjectType), store.resolve_type(toObjectType)
    body = await read_json(request)
    if (ft, tt) not in DEFAULT_ASSOC:
        raise ApiError(400, f"No default association from {ft} to {tt}")
    d = DEFAULT_ASSOC[(ft, tt)]
    results = []
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            for inp in body.get("inputs") or []:
                fid, tid = _ids(inp, "from"), _ids(inp, "to")
                await store.associate(conn, ft, fid, tt, tid, None)
                results.append({"from": {"id": str(fid)}, "to": {"id": str(tid)},
                                "associationSpec": {"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": d}})
                results.append({"from": {"id": str(tid)}, "to": {"id": str(fid)},
                                "associationSpec": {"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": INVERSE[d]}})
    return _batch(results)


@router.post("/{fromObjectType}/{toObjectType}/batch/archive", status_code=204)
async def batch_archive(fromObjectType: str, toObjectType: str, request: Request):
    body = await read_json(request)
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            for inp in body.get("inputs") or []:
                fid = _ids(inp, "from")
                tos = inp.get("to") or []
                for t in tos if isinstance(tos, list) else [tos]:
                    await store.unassociate(conn, fid, _ids({"to": t}, "to"))
    return Response(status_code=204)


@router.post("/{fromObjectType}/{toObjectType}/batch/labels/archive", status_code=204)
async def batch_archive_labels(fromObjectType: str, toObjectType: str, request: Request):
    body = await read_json(request)
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            for inp in body.get("inputs") or []:
                fid, tid = _ids(inp, "from"), _ids(inp, "to")
                type_ids = [int(t["associationTypeId"]) for t in inp.get("types") or []]
                await store.unassociate(conn, fid, tid, type_ids or None)
    return Response(status_code=204)
