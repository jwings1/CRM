"""Live CRM evidence; no model SQL and no caches between requests."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from .. import search, store
from ..errors import ApiError


def record(row) -> dict:
    return {"id": str(row["id"]), "object_type": row["object_type"],
            "properties": row["properties"], "updated_at": store.iso(row["updated_at"]),
            "archived": row["archived"]}


async def scoped_body(conn, object_type: str, args: dict, user: str) -> dict:
    body = {key: args[key] for key in ("query", "sorts", "after", "limit") if key in args}
    groups = args.get("filter_groups") or []
    extra = []
    related = args.get("related_to")
    if related:
        target_type = store.resolve_type(related["object_type"])
        target = await store.get(conn, target_type, related["id"])
        extra.append({"propertyName": f"associations.{target_type}", "operator": "EQ", "value": str(target["id"])})
    if args.get("my_customers"):
        if object_type != "companies":
            raise ApiError(400, "my_customers applies to companies")
        ids = await conn.fetch(
            "SELECT DISTINCT a.to_id FROM objects o JOIN associations a ON a.from_id=o.id AND a.to_type='companies' "
            "JOIN objects c ON c.id=a.to_id AND NOT c.archived WHERE NOT o.archived AND "
            "((o.object_type='deals' AND lower(o.properties->>'commerciale')=lower($1)) OR "
            "(o.object_type='tickets' AND lower(o.properties->>'assegnatario')=lower($1)))", user)
        extra.append({"propertyName": "id", "operator": "IN", "values": [str(r["to_id"]) for r in ids]})
    body["filterGroups"] = [{"filters": list(g.get("filters", [])) + extra} for g in groups] if groups else [{"filters": extra}]
    return body


async def search_records(conn, object_type: str, args: dict, user: str) -> dict:
    object_type = store.resolve_type(object_type)
    body = await scoped_body(conn, object_type, args, user)
    rows, total, after = await search.search(conn, object_type, body)
    return {"records": [record(r) for r in rows], "total": total, "after": after}


async def get_record(conn, object_type: str, identifier, id_property: str | None = None) -> dict:
    row = await store.get(conn, store.resolve_type(object_type), identifier, id_property)
    result = record(row)
    result["associations"] = [dict(r) for r in await conn.fetch(
        "SELECT DISTINCT a.to_type,a.to_id FROM associations a JOIN objects o ON o.id=a.to_id "
        "WHERE a.from_id=$1 AND NOT o.archived ORDER BY a.to_type,a.to_id", row["id"])]
    return result


async def related_records(conn, object_type: str, identifier, target_type: str | None = None,
                           after: int = 0, limit: int = 50, activities: bool = False) -> dict:
    root = await store.get(conn, store.resolve_type(object_type), identifier)
    roots = [root["id"]]
    if activities and root["object_type"] == "companies":
        roots += [r["to_id"] for r in await conn.fetch(
            "SELECT DISTINCT a.to_id FROM associations a JOIN objects o ON o.id=a.to_id "
            "WHERE a.from_id=$1 AND a.to_type IN ('contacts','deals') AND NOT o.archived", root["id"])]
    target_types = (["notes", "calls", "emails", "meetings"] if activities else
                    [store.resolve_type(target_type)] if target_type else [])
    condition = ("NOT o.archived AND ($2::text[]='{}' OR o.object_type=ANY($2)) AND "
                 "EXISTS (SELECT 1 FROM associations a WHERE a.to_id=o.id AND a.from_id=ANY($1::bigint[]))")
    total = await conn.fetchval("SELECT count(*) FROM objects o WHERE " + condition, roots, target_types)
    rows = await conn.fetch("SELECT o.* FROM objects o WHERE " + condition +
                            " AND o.id>$3 ORDER BY o.id LIMIT $4", roots, target_types, int(after), max(1, min(int(limit), 200)) + 1)
    bound = max(1, min(int(limit), 200))
    more = len(rows) > bound
    rows = rows[:bound]
    return {"records": [record(r) for r in rows], "total": total,
            "after": str(rows[-1]["id"]) if rows and more else None}


async def aggregate_records(conn, object_type: str, args: dict, user: str) -> dict:
    object_type = store.resolve_type(object_type)
    operation = args.get("operation", "count")
    field, group_by = args.get("field"), args.get("group_by")
    if operation not in ("count", "sum"):
        raise ApiError(400, "Aggregate operation must be count or sum")
    if operation == "sum":
        definition = await conn.fetchrow(
            "SELECT type FROM property_defs WHERE object_type=$1 AND name=$2 AND NOT archived", object_type, field)
        if not definition or definition["type"] != "number":
            raise ApiError(400, f"{field} is not a numeric property")
    monetary = field in ("amount", "price", "fatturato_2025")
    buckets, excluded, count = {}, 0, 0
    async with conn.transaction(isolation="repeatable_read", readonly=True):
        body = await scoped_body(conn, object_type, args, user)
        body.update(limit=200, after=0)
        while True:
            rows, total, after = await search.search(conn, object_type, body)
            if operation == "count" and not group_by:
                return {"count": total, "complete": True}
            for row in rows:
                count += 1
                props = row["properties"]
                currency = props.get("deal_currency_code", "EUR") if monetary else None
                key = (props.get(group_by) if group_by else None, currency)
                bucket = buckets.setdefault(key, {"group": key[0], "currency": currency, "count": 0,
                                                   "sum": Decimal(0), "valued_count": 0})
                bucket["count"] += 1
                if operation == "sum":
                    try:
                        value = Decimal(props.get(field, ""))
                        if not value.is_finite():
                            raise InvalidOperation
                    except InvalidOperation:
                        excluded += 1
                        continue
                    bucket["sum"] += value
                    bucket["valued_count"] += 1
            if after is None:
                break
            body["after"] = after
    for bucket in buckets.values():
        bucket["sum"] = str(bucket["sum"]) if bucket["valued_count"] else None
        if operation == "count":
            bucket.pop("sum")
    return {"count": count, "groups": list(buckets.values()), "excluded_values": excluded, "complete": True}


async def list_users(conn, query: str = "", active_only: bool = False) -> list[dict]:
    return [dict(r) for r in await conn.fetch(
        "SELECT legacy_id,email,name,active FROM agent_users WHERE (NOT $2 OR active) AND "
        "($1='' OR lower(name) LIKE '%'||lower($1)||'%' OR lower(email)=lower($1) OR lower(legacy_id)=lower($1)) "
        "ORDER BY name,legacy_id", query.strip(), active_only)]


async def metadata(conn, object_type: str) -> dict:
    object_type = store.resolve_type(object_type)
    props = await conn.fetch(
        "SELECT name,label,type,options,read_only,calculated FROM property_defs WHERE object_type=$1 AND NOT archived ORDER BY name",
        object_type)
    stages = await conn.fetch(
        "SELECT p.id AS pipeline_id,p.label AS pipeline_label,s.id AS stage_id,s.label AS stage_label,s.metadata "
        "FROM pipelines p JOIN pipeline_stages s ON s.object_type=p.object_type AND s.pipeline_id=p.id "
        "WHERE p.object_type=$1 AND NOT p.archived AND NOT s.archived ORDER BY p.display_order,s.display_order", object_type)
    return {"properties": [dict(r) for r in props], "pipeline_stages": [dict(r) for r in stages]}
