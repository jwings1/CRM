"""CRM object endpoints, generic over every object type.
Mounted at /crm/objects/2026-09 and /crm/v3/objects (see main.py).

Scaffold: single-record CRUD + record associations.
Lane A adds: batch/read|create|update|upsert|archive, search, merge. Register the
literal paths (/batch/..., /search, /merge) BEFORE the /{objectType}/{objectId} routes.
"""
from __future__ import annotations

import orjson
from fastapi import APIRouter, Request, Response

from .. import db, store
from ..defaults import ASSOC_TYPES, INVERSE, OBJECT_TYPES
from ..errors import ApiError

router = APIRouter()


def qlist(request: Request, name: str) -> list[str] | None:
    vals = request.query_params.getlist(name)
    out = [x.strip() for v in vals for x in v.split(",") if x.strip()]
    return out or None


def qbool(request: Request, name: str) -> bool:
    return (request.query_params.get(name) or "").lower() == "true"


async def read_json(request: Request):
    raw = await request.body()
    if not raw:
        return {}
    try:
        return orjson.loads(raw)
    except orjson.JSONDecodeError:
        raise ApiError(400, "Invalid input JSON on line 1", "VALIDATION_ERROR")


async def render(conn, otype: str, row, request: Request) -> dict:
    assoc_types = qlist(request, "associations")
    assocs = await store.associations_v3(conn, otype, row["id"], assoc_types) if assoc_types else None
    return store.serialize(otype, row, qlist(request, "properties"), assocs)


# ------------------------------------------------------------------ Lane A: batch / search / merge go here


# ------------------------------------------------------------------ basic

@router.get("/{objectType}")
async def list_objects(objectType: str, request: Request):
    otype = store.resolve_type(objectType)
    async with db.pool.acquire() as conn:
        rows, nxt = await store.list_page(conn, otype, int(request.query_params.get("limit") or 10),
                                          request.query_params.get("after"), qbool(request, "archived"))
        results = [await render(conn, otype, r, request) for r in rows]
    body = {"results": results}
    if nxt:
        body["paging"] = {"next": {"after": nxt, "link": f"{request.url.path}?after={nxt}"}}
    return body


@router.post("/{objectType}", status_code=201)
async def create_object(objectType: str, request: Request):
    otype = store.resolve_type(objectType)
    body = await read_json(request)
    async with db.pool.acquire() as conn:
        row = await store.create(conn, otype, body.get("properties") or {}, body.get("associations") or None)
        return store.serialize(otype, row, list((body.get("properties") or {}).keys()) or None)


@router.get("/{objectType}/{objectId}")
async def get_object(objectType: str, objectId: str, request: Request):
    otype = store.resolve_type(objectType)
    async with db.pool.acquire() as conn:
        row = await store.get(conn, otype, objectId, request.query_params.get("idProperty"), qbool(request, "archived"))
        return await render(conn, otype, row, request)


@router.patch("/{objectType}/{objectId}")
async def update_object(objectType: str, objectId: str, request: Request):
    otype = store.resolve_type(objectType)
    body = await read_json(request)
    async with db.pool.acquire() as conn:
        row = await store.update(conn, otype, objectId, body.get("properties") or {},
                                 id_property=request.query_params.get("idProperty"))
        return store.serialize(otype, row, list((body.get("properties") or {}).keys()) or None)


@router.delete("/{objectType}/{objectId}", status_code=204)
async def archive_object(objectType: str, objectId: str):
    otype = store.resolve_type(objectType)
    async with db.pool.acquire() as conn:
        await store.archive(conn, otype, objectId)
    return Response(status_code=204)


# ------------------------------------------------------------------ record associations (2026-09 / v4 shapes)

def _labels(from_type: str, to_type: str, category: str, type_id: int) -> dict:
    label = next((a["label"] for a in ASSOC_TYPES if a["type_id"] == type_id), None) if category == "HUBSPOT_DEFINED" else None
    return {"category": category, "typeId": type_id, "label": label}


async def _ids(conn, objectType, objectId, toObjectType, toObjectId):
    ft, tt = store.resolve_type(objectType), store.resolve_type(toObjectType)
    try:
        return ft, int(objectId), tt, int(toObjectId)
    except ValueError:
        raise ApiError(400, "Object ids must be numeric")


@router.put("/{objectType}/{objectId}/associations/default/{toObjectType}/{toObjectId}")
async def associate_default(objectType: str, objectId: str, toObjectType: str, toObjectId: str):
    async with db.pool.acquire() as conn:
        ft, fid, tt, tid = await _ids(conn, objectType, objectId, toObjectType, toObjectId)
        async with conn.transaction():
            types = await store.associate(conn, ft, fid, tt, tid, None)
    cat, typ = types[0]
    now = store.now_iso()
    return {"status": "COMPLETE", "results": [
        {"from": {"id": str(fid)}, "to": {"id": str(tid)},
         "associationSpec": {"associationCategory": cat, "associationTypeId": typ}},
        {"from": {"id": str(tid)}, "to": {"id": str(fid)},
         "associationSpec": {"associationCategory": cat, "associationTypeId": INVERSE.get(typ, typ)}},
    ], "startedAt": now, "completedAt": now}


@router.put("/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}")
async def associate_labeled(objectType: str, objectId: str, toObjectType: str, toObjectId: str, request: Request):
    body = await read_json(request)
    if not isinstance(body, list) or not body:
        raise ApiError(400, "Body must be a non-empty array of {associationCategory, associationTypeId}")
    types = [(b.get("associationCategory", "HUBSPOT_DEFINED"), int(b["associationTypeId"])) for b in body]
    async with db.pool.acquire() as conn:
        ft, fid, tt, tid = await _ids(conn, objectType, objectId, toObjectType, toObjectId)
        async with conn.transaction():
            await store.associate(conn, ft, fid, tt, tid, types)
            rows = await conn.fetch("SELECT category, type_id FROM associations WHERE from_id=$1 AND to_id=$2", fid, tid)
    return {"fromObjectTypeId": OBJECT_TYPES[ft][0], "fromObjectId": fid,
            "toObjectTypeId": OBJECT_TYPES[tt][0], "toObjectId": tid,
            "labels": [l for l in (_labels(ft, tt, r["category"], r["type_id"])["label"] for r in rows) if l]}


@router.put("/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}")
async def associate_v3(objectType: str, objectId: str, toObjectType: str, toObjectId: str, associationTypeId: int):
    async with db.pool.acquire() as conn:
        ft, fid, tt, tid = await _ids(conn, objectType, objectId, toObjectType, toObjectId)
        async with conn.transaction():
            await store.associate(conn, ft, fid, tt, tid, [("HUBSPOT_DEFINED", associationTypeId)])
            row = await store.get(conn, ft, fid)
            assocs = await store.associations_v3(conn, ft, fid, [tt])
    return store.serialize(ft, row, None, assocs)


@router.delete("/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}", status_code=204)
async def unassociate(objectType: str, objectId: str, toObjectType: str, toObjectId: str):
    async with db.pool.acquire() as conn:
        _, fid, _, tid = await _ids(conn, objectType, objectId, toObjectType, toObjectId)
        await store.unassociate(conn, fid, tid)
    return Response(status_code=204)


@router.delete("/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}", status_code=204)
async def unassociate_type(objectType: str, objectId: str, toObjectType: str, toObjectId: str, associationTypeId: int):
    async with db.pool.acquire() as conn:
        _, fid, _, tid = await _ids(conn, objectType, objectId, toObjectType, toObjectId)
        await store.unassociate(conn, fid, tid, [associationTypeId])
    return Response(status_code=204)


@router.get("/{objectType}/{objectId}/associations/{toObjectType}")
async def list_associations(objectType: str, objectId: str, toObjectType: str):
    ft, tt = store.resolve_type(objectType), store.resolve_type(toObjectType)
    async with db.pool.acquire() as conn:
        rows = await store.assoc_rows(conn, int(objectId), tt)
    grouped: dict[int, list] = {}
    for r in rows:
        grouped.setdefault(r["to_id"], []).append(_labels(ft, tt, r["category"], r["type_id"]))
    return {"results": [{"toObjectId": k, "associationTypes": v} for k, v in grouped.items()]}
