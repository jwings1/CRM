"""Lists API (2026-09). Mounted at /crm/lists/2026-09 and /crm/v3/lists.
MANUAL/SNAPSHOT lists store members in list_memberships. DYNAMIC lists: Lane A can evaluate
filter_branch with the search engine; until then they behave like static lists."""
from __future__ import annotations

from fastapi import APIRouter, Request, Response

from .. import db, store
from ..defaults import OBJECT_TYPES, canon_type
from ..errors import ApiError
from .objects import read_json

router = APIRouter()
_TYPE_IDS = {tid for tid, _ in OBJECT_TYPES.values()}


def _type_id(raw: str) -> str:
    t = canon_type(raw)
    if not t:
        raise ApiError(400, f"Unknown objectTypeId {raw}")
    return OBJECT_TYPES[t][0]


async def _list_json(conn, r, include_filters: bool = False) -> dict:
    size = await conn.fetchval("SELECT count(*) FROM list_memberships WHERE list_id=$1", r["list_id"])
    out = {
        "listId": str(r["list_id"]), "listVersion": 1, "name": r["name"], "objectTypeId": r["object_type_id"],
        "processingType": r["processing_type"], "processingStatus": "COMPLETE",
        "createdAt": store.iso(r["created_at"]), "updatedAt": store.iso(r["updated_at"]),
        "filtersUpdatedAt": store.iso(r["updated_at"]), "size": size,
        "additionalProperties": {"hs_list_size": str(size)},
    }
    if include_filters and r["filter_branch"] is not None:
        out["filterBranch"] = r["filter_branch"]
    return out


async def _get(conn, list_id: str):
    try:
        lid = int(list_id)
    except ValueError:
        raise ApiError(404, f"List {list_id} not found", "OBJECT_NOT_FOUND")
    r = await conn.fetchrow("SELECT * FROM lists WHERE list_id=$1 AND NOT archived", lid)
    if not r:
        raise ApiError(404, f"List {list_id} not found", "OBJECT_NOT_FOUND")
    return r


@router.post("")
async def create_list(request: Request):
    body = await read_json(request)
    name, otid = (body.get("name") or "").strip(), body.get("objectTypeId")
    ptype = body.get("processingType") or "MANUAL"
    if not name or not otid:
        raise ApiError(400, "name, objectTypeId and processingType are required")
    otid = _type_id(otid)
    async with db.pool.acquire() as conn:
        if await conn.fetchval("SELECT 1 FROM lists WHERE lower(name)=lower($1) AND NOT archived", name):
            raise ApiError(409, f"A list named {name} already exists", "CONFLICT")
        r = await conn.fetchrow(
            "INSERT INTO lists (name, object_type_id, processing_type, filter_branch) VALUES ($1,$2,$3,$4) RETURNING *",
            name, otid, ptype, body.get("filterBranch"))
        return {"list": await _list_json(conn, r, True)}


@router.get("")
async def get_lists(request: Request):
    ids = [int(x) for v in request.query_params.getlist("listIds") for x in v.split(",") if x.strip().isdigit()]
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM lists WHERE list_id = ANY($1::bigint[]) AND NOT archived ORDER BY list_id", ids)
        return {"lists": [await _list_json(conn, r) for r in rows]}


@router.post("/search")
async def search_lists(request: Request):
    body = await read_json(request)
    q = (body.get("query") or "").strip()
    offset, count = int(body.get("offset") or 0), int(body.get("count") or 20)
    ids = [int(x) for x in body.get("listIds") or [] if str(x).isdigit()]
    ptypes = body.get("processingTypes") or []
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM lists WHERE NOT archived AND ($1 = '' OR name ILIKE '%' || $1 || '%') "
            "AND (cardinality($2::bigint[]) = 0 OR list_id = ANY($2)) "
            "AND (cardinality($3::text[]) = 0 OR processing_type = ANY($3)) ORDER BY list_id", q, ids, ptypes)
        page = rows[offset:offset + count]
        return {"lists": [await _list_json(conn, r) for r in page], "hasMore": offset + count < len(rows),
                "offset": offset + len(page), "total": len(rows)}


@router.get("/object-type-id/{objectTypeId}/name/{listName}")
async def get_by_name(objectTypeId: str, listName: str):
    otid = _type_id(objectTypeId)
    async with db.pool.acquire() as conn:
        r = await conn.fetchrow("SELECT * FROM lists WHERE object_type_id=$1 AND lower(name)=lower($2) AND NOT archived",
                                otid, listName)
        if not r:
            raise ApiError(404, f"List {listName} not found", "OBJECT_NOT_FOUND")
        return {"list": await _list_json(conn, r)}


@router.get("/records/{objectTypeId}/{recordId}/memberships")
async def record_memberships(objectTypeId: str, recordId: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT list_id, added_at FROM list_memberships WHERE record_id=$1 ORDER BY list_id", recordId)
    return {"results": [{"listId": str(r["list_id"]), "listVersion": 1, "isPublicList": True,
                         "firstAddedTimestamp": store.iso(r["added_at"]), "lastAddedTimestamp": store.iso(r["added_at"])}
                        for r in rows], "total": len(rows)}


@router.get("/{listId}")
async def get_list(listId: str, includeFilters: bool = False):
    async with db.pool.acquire() as conn:
        return {"list": await _list_json(conn, await _get(conn, listId), includeFilters)}


@router.delete("/{listId}", status_code=204)
async def delete_list(listId: str):
    async with db.pool.acquire() as conn:
        r = await _get(conn, listId)
        await conn.execute("UPDATE lists SET archived=true WHERE list_id=$1", r["list_id"])
    return Response(status_code=204)


async def _members(listId: str, request: Request, order: str):
    limit = max(1, min(int(request.query_params.get("limit") or 100), 250))
    after = request.query_params.get("after")
    async with db.pool.acquire() as conn:
        r = await _get(conn, listId)
        total = await conn.fetchval("SELECT count(*) FROM list_memberships WHERE list_id=$1", r["list_id"])
        rows = await conn.fetch(
            "SELECT record_id, added_at FROM list_memberships WHERE list_id=$1 AND record_id > $2 "
            "ORDER BY record_id LIMIT $3", r["list_id"], int(after or 0), limit + 1)
    more = len(rows) > limit
    rows = rows[:limit]
    body = {"results": [{"recordId": str(x["record_id"]), "membershipTimestamp": store.iso(x["added_at"])} for x in rows],
            "total": total}
    if more:
        body["paging"] = {"next": {"after": str(rows[-1]["record_id"])}}
    return body


@router.get("/{listId}/memberships")
async def memberships(listId: str, request: Request):
    return await _members(listId, request, "record")


@router.get("/{listId}/memberships/join-order")
async def memberships_join(listId: str, request: Request):
    return await _members(listId, request, "join")


async def _change(listId: str, add: list, remove: list) -> dict:
    async with db.pool.acquire() as conn:
        r = await _get(conn, listId)
        otype = next(t for t, (tid, _) in OBJECT_TYPES.items() if tid == r["object_type_id"])
        wanted = [int(x) for x in [*add, *remove] if str(x).isdigit()]
        existing = {x["id"] for x in await conn.fetch(
            "SELECT id FROM objects WHERE id = ANY($1::bigint[]) AND object_type=$2 AND NOT archived", wanted, otype)}
        added = [int(x) for x in add if str(x).isdigit() and int(x) in existing]
        removed = [int(x) for x in remove if str(x).isdigit()]
        async with conn.transaction():
            if added:
                await conn.executemany("INSERT INTO list_memberships (list_id, record_id) VALUES ($1,$2) ON CONFLICT DO NOTHING",
                                       [(r["list_id"], a) for a in added])
            if removed:
                await conn.execute("DELETE FROM list_memberships WHERE list_id=$1 AND record_id = ANY($2::bigint[])",
                                   r["list_id"], removed)
            await conn.execute("UPDATE lists SET updated_at=now() WHERE list_id=$1", r["list_id"])
    missing = [str(x) for x in add if not (str(x).isdigit() and int(x) in existing)]
    return {"recordsIdsAdded": [str(a) for a in added], "recordIdsRemoved": [str(x) for x in removed],
            "recordIdsMissing": missing}


@router.put("/{listId}/memberships/add")
async def add_members(listId: str, request: Request):
    return await _change(listId, await read_json(request) or [], [])


@router.put("/{listId}/memberships/remove")
async def remove_members(listId: str, request: Request):
    return await _change(listId, [], await read_json(request) or [])


@router.put("/{listId}/memberships/add-and-remove")
async def add_remove_members(listId: str, request: Request):
    body = await read_json(request) or {}
    return await _change(listId, body.get("recordIdsToAdd") or [], body.get("recordIdsToRemove") or [])


@router.delete("/{listId}/memberships", status_code=204)
async def clear_members(listId: str):
    async with db.pool.acquire() as conn:
        r = await _get(conn, listId)
        await conn.execute("DELETE FROM list_memberships WHERE list_id=$1", r["list_id"])
    return Response(status_code=204)
