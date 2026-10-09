"""CRM object endpoints, generic over every object type.
Mounted at /crm/objects/2026-09 and /crm/v3/objects (see main.py).

Scaffold: single-record CRUD + record associations.
Lane A adds: batch/read|create|update|upsert|archive, search, merge. Register the
literal paths (/batch/..., /search, /merge) BEFORE the /{objectType}/{objectId} routes.
"""
from __future__ import annotations

import orjson
from fastapi import APIRouter, Request, Response
from fastapi.responses import ORJSONResponse

from .. import db, store
from .. import search as search_mod
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


# ------------------------------------------------------------------ search / batch / merge
# (literal paths registered BEFORE /{objectType}/{objectId})

MAX_BATCH = 100


def _inputs(body: dict) -> list:
    inputs = (body or {}).get("inputs")
    if not isinstance(inputs, list):
        raise ApiError(400, "inputs is required")
    if len(inputs) > MAX_BATCH:
        raise ApiError(400, f"Too many inputs: {len(inputs)} (max {MAX_BATCH})")
    return inputs


def _batch(results: list, errors: list | None = None, status: int = 200):
    now = store.now_iso()
    body = {"status": "COMPLETE", "results": results, "startedAt": now, "completedAt": now}
    if errors:
        body["numErrors"] = len(errors)
        body["errors"] = errors
        status = 207
    return ORJSONResponse(body, status_code=status)


def _missing(otype: str, ids: list) -> dict:
    return {"status": "error", "category": "OBJECT_NOT_FOUND",
            "message": f"Could not get some {otype} objects, they may be deleted or not exist. Check that ids are valid.",
            "context": {"ids": [str(i) for i in ids]}}


@router.post("/{objectType}/search")
async def search_objects(objectType: str, request: Request):
    otype = store.resolve_type(objectType)
    body = await read_json(request)
    async with db.pool.acquire() as conn:
        rows, total, nxt = await search_mod.search(conn, otype, body)
    props = body.get("properties") or None
    out = {"total": total, "results": [store.serialize(otype, r, props) for r in rows]}
    if nxt is not None:
        out["paging"] = {"next": {"after": str(nxt), "link": f"{request.url.path}?after={nxt}"}}
    return out


@router.post("/{objectType}/batch/read")
async def batch_read(objectType: str, request: Request):
    otype = store.resolve_type(objectType)
    body = await read_json(request)
    inputs = _inputs(body)
    id_prop = body.get("idProperty") or request.query_params.get("idProperty")
    archived = qbool(request, "archived")
    props = body.get("properties") or None
    results, missing = [], []
    async with db.pool.acquire() as conn:
        for inp in inputs:
            key = (inp or {}).get("id")
            row = await store.fetch_row(conn, otype, key, id_prop, archived)
            if row is None:
                missing.append(key)
            else:
                results.append(store.serialize(otype, row, props))
    return _batch(results, [_missing(otype, missing)] if missing else None)


@router.post("/{objectType}/batch/create")
async def batch_create(objectType: str, request: Request):
    otype = store.resolve_type(objectType)
    inputs = _inputs(await read_json(request))
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            rows = [await store.create(conn, otype, inp.get("properties") or {}, inp.get("associations") or None)
                    for inp in inputs]
    return _batch([store.serialize(otype, r, list((i.get("properties") or {}).keys()) or None)
                   for r, i in zip(rows, inputs)], status=201)


@router.post("/{objectType}/batch/update")
async def batch_update(objectType: str, request: Request):
    otype = store.resolve_type(objectType)
    body = await read_json(request)
    inputs = _inputs(body)
    results, missing = [], []
    async with db.pool.acquire() as conn:
        for inp in inputs:
            try:
                row = await store.update(conn, otype, inp.get("id"), inp.get("properties") or {},
                                         id_property=inp.get("idProperty") or body.get("idProperty"))
                results.append(store.serialize(otype, row, list((inp.get("properties") or {}).keys()) or None))
            except ApiError as e:
                if e.status != 404:
                    raise
                missing.append(inp.get("id"))
    return _batch(results, [_missing(otype, missing)] if missing else None)


@router.post("/{objectType}/batch/upsert")
async def batch_upsert(objectType: str, request: Request):
    """Create-or-update by a unique property (email, partita_iva, ...). Each key is serialized with a
    transaction-scoped advisory lock, so parallel upserts on the same key never duplicate or lose values."""
    otype = store.resolve_type(objectType)
    body = await read_json(request)
    inputs = _inputs(body)
    results = []
    async with db.pool.acquire() as conn:
        for inp in inputs:
            id_prop = inp.get("idProperty") or body.get("idProperty")
            key = inp.get("id")
            if not id_prop or key in (None, ""):
                raise ApiError(400, "Each upsert input needs id and idProperty")
            props = dict(inp.get("properties") or {})
            async with conn.transaction():
                await conn.execute("SELECT pg_advisory_xact_lock(hashtext($1))", f"{otype}|{id_prop}|{str(key).lower()}")
                row = await store.fetch_row(conn, otype, key, id_prop)
                if row is not None:
                    row = await store.update(conn, otype, row["id"], props)
                    is_new = False
                else:
                    if id_prop not in ("hs_object_id", "id"):
                        props.setdefault(id_prop, str(key))
                    row = await store.create(conn, otype, props)
                    is_new = True
            res = store.serialize(otype, row, list(props.keys()) or None)
            res["new"] = is_new
            results.append(res)
    return _batch(results)


@router.post("/{objectType}/batch/archive", status_code=204)
async def batch_archive(objectType: str, request: Request):
    otype = store.resolve_type(objectType)
    inputs = _inputs(await read_json(request))
    async with db.pool.acquire() as conn:
        for inp in inputs:
            await store.archive(conn, otype, (inp or {}).get("id"))
    return Response(status_code=204)


@router.post("/{objectType}/merge")
async def merge_objects(objectType: str, request: Request):
    """Primary keeps its values (fills its empty ones from the merged record), takes over the merged
    record's associations; the merged record is archived. Companies also keep the merged domains."""
    otype = store.resolve_type(objectType)
    body = await read_json(request)
    try:
        pid, mid = int(body.get("primaryObjectId")), int(body.get("objectIdToMerge"))
    except (TypeError, ValueError):
        raise ApiError(400, "primaryObjectId and objectIdToMerge are required")
    if pid == mid:
        raise ApiError(400, "Cannot merge a record with itself")
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            prim = await store.fetch_row(conn, otype, pid, for_update=True)
            other = await store.fetch_row(conn, otype, mid, for_update=True)
            if prim is None or other is None:
                raise ApiError(404, "One of the records to merge was not found", "OBJECT_NOT_FOUND")
            pp, op_ = prim["properties"], other["properties"]
            fill = {k: v for k, v in op_.items() if v not in (None, "") and not pp.get(k)
                    and k not in ("hs_object_id", "createdate", "hs_createdate", "lastmodifieddate", "hs_lastmodifieddate", "email", "partita_iva")}
            if otype == "companies":
                doms = [d for d in (pp.get("hs_additional_domains") or "").split(";") if d]
                for d in [op_.get("domain"), *(op_.get("hs_additional_domains") or "").split(";")]:
                    if d and d != pp.get("domain") and d not in doms:
                        doms.append(d)
                if doms:
                    fill["hs_additional_domains"] = ";".join(doms)
            if otype == "contacts" and op_.get("email") and op_.get("email") != pp.get("email"):
                extra = [e for e in (pp.get("hs_additional_emails") or "").split(";") if e]
                fill["hs_additional_emails"] = ";".join([*extra, op_["email"]])
            moved = await conn.fetch("SELECT to_type, to_id, category, type_id FROM associations WHERE from_id=$1", mid)
            await store.archive(conn, otype, mid)
            for a in moved:
                if a["to_id"] != pid:
                    await store.associate(conn, otype, pid, a["to_type"], a["to_id"], [(a["category"], a["type_id"])], check=False)
            row = await store.update(conn, otype, pid, fill, validate=False, run_hooks=False) if fill else prim
    return store.serialize(otype, row)



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
