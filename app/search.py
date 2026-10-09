"""HubSpot CRM search -> SQL over objects.properties (jsonb, string values).

filterGroups are OR'ed, filters inside a group AND'ed. Operators: EQ NEQ LT LTE GT GTE BETWEEN IN NOT_IN
HAS_PROPERTY NOT_HAS_PROPERTY CONTAINS_TOKEN NOT_CONTAINS_TOKEN. Comparison follows the property type
(number -> numeric, date/datetime -> timestamptz, else case-insensitive text).
Extras: propertyName "hs_object_id"/"id" hits the id column; "associations.<type>" filters by association.
Paging: `after` is an offset over a stable order (sorts + id), `total` is exact.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

from .defaults import OBJECT_TYPES, canon_type
from .errors import ApiError

MAX_LIMIT = 200

QUERY_PROPS = {
    "contacts": ["firstname", "lastname", "email", "phone", "company"],
    "companies": ["name", "domain", "website", "phone"],
    "deals": ["dealname"],
    "tickets": ["subject", "content"],
    "products": ["name", "hs_sku", "description"],
    "line_items": ["name"],
    "tasks": ["hs_task_subject", "hs_task_body"],
    "notes": ["hs_note_body"],
    "calls": ["hs_call_title", "hs_call_body"],
    "emails": ["hs_email_subject", "hs_email_text"],
    "meetings": ["hs_meeting_title", "hs_meeting_body"],
    "quotes": ["hs_title"],
}

_NUM_RX = r"^\s*-?[0-9]+(\.[0-9]+)?\s*$"
_TS_RX = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}"


class Q:
    def __init__(self):
        self.args: list = []

    def p(self, v) -> str:
        self.args.append(v)
        return f"${len(self.args)}"


def _to_iso(v) -> str:
    s = str(v).strip()
    if re.fullmatch(r"-?\d{9,}", s):
        return datetime.fromtimestamp(int(s) / 1000, tz=timezone.utc).isoformat()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s + "T00:00:00+00:00"
    return s.replace("Z", "+00:00")


def _expr(name: str, ptype: str) -> str:
    if name in ("hs_object_id", "id"):
        return "o.id"
    raw = f"(o.properties->>'{name}')"
    if ptype == "number":
        return f"(CASE WHEN {raw} ~ '{_NUM_RX}' THEN {raw}::numeric END)"
    if ptype in ("date", "datetime"):
        return f"(CASE WHEN {raw} ~ '{_TS_RX}' THEN {raw}::timestamptz END)"
    return f"lower({raw})"


def _val(q: Q, v, ptype: str, name: str) -> str:
    if name in ("hs_object_id", "id"):
        try:
            return q.p(int(str(v).strip())) + "::bigint"
        except ValueError:
            raise ApiError(400, f"{v} is not a valid id")
    if ptype == "number":
        try:
            return q.p(str(float(str(v).strip()))) + "::text::numeric"
        except ValueError:
            raise ApiError(400, f"{v} is not a valid number for {name}")
    if ptype in ("date", "datetime"):
        return q.p(_to_iso(v)) + "::text::timestamptz"
    return f"lower({q.p(str(v))})"


_SAFE = re.compile(r"^[A-Za-z0-9_.\-]+$")


def _filter(q: Q, otype: str, f: dict, types: dict[str, str]) -> str:
    name = f.get("propertyName") or ""
    op = (f.get("operator") or "EQ").upper()
    if not _SAFE.match(name):
        raise ApiError(400, f"Invalid propertyName {name!r}")
    if name.startswith("associations."):
        tt = canon_type(name.split(".", 1)[1])
        if not tt:
            raise ApiError(400, f"Unknown association type in {name}")
        vals = f.get("values") or ([f.get("value")] if f.get("value") is not None else [])
        ids = [int(v) for v in vals if str(v).strip().isdigit()]
        cond = (f"EXISTS (SELECT 1 FROM associations a WHERE a.from_id = o.id AND a.to_type = {q.p(tt)} "
                f"AND a.to_id = ANY({q.p(ids)}::bigint[]))")
        return f"NOT {cond}" if op in ("NEQ", "NOT_IN") else cond
    ptype = types.get(name, "string")
    raw = f"(o.properties->>'{name}')"
    has = f"coalesce({raw}, '') <> ''" if name not in ("hs_object_id", "id") else "true"
    if op == "HAS_PROPERTY":
        return has
    if op == "NOT_HAS_PROPERTY":
        return f"NOT ({has})"
    e = _expr(name, ptype)
    if op in ("EQ", "NEQ"):
        v = f.get("value")
        if v is None:
            raise ApiError(400, f"Filter {name} {op} requires value")
        if ptype == "enumeration" and types.get(f"__checkbox__{name}"):
            cond = f"{q.p(str(v).lower())} = ANY(string_to_array(lower({raw}), ';'))"
        else:
            cond = f"{e} = {_val(q, v, ptype, name)}"
        return cond if op == "EQ" else f"NOT coalesce({cond}, false)"
    if op in ("LT", "LTE", "GT", "GTE"):
        sym = {"LT": "<", "LTE": "<=", "GT": ">", "GTE": ">="}[op]
        return f"{e} {sym} {_val(q, f.get('value'), ptype, name)}"
    if op == "BETWEEN":
        lo, hi = f.get("value"), f.get("highValue")
        return f"{e} BETWEEN {_val(q, lo, ptype, name)} AND {_val(q, hi, ptype, name)}"
    if op in ("IN", "NOT_IN"):
        vals = f.get("values") or []
        if not vals:
            return "false" if op == "IN" else "true"
        items = ", ".join(_val(q, v, ptype, name) for v in vals)
        cond = f"{e} IN ({items})"
        return cond if op == "IN" else f"NOT coalesce({cond}, false)"
    if op in ("CONTAINS_TOKEN", "NOT_CONTAINS_TOKEN"):
        v = str(f.get("value") or "").lower()
        pat = v.replace("%", r"\%").replace("_", r"\_").replace("*", "%")
        if "%" not in pat:
            pat = f"%{pat}%"
        cond = f"lower(coalesce({raw}, '')) LIKE {q.p(pat)}"
        return cond if op == "CONTAINS_TOKEN" else f"NOT ({cond})"
    raise ApiError(400, f"Unsupported operator {op}")


async def search(conn, otype: str, body: dict) -> tuple[list, int, int | None]:
    """Returns (rows, total, next_offset)."""
    assert otype in OBJECT_TYPES
    body = body or {}
    limit = max(1, min(int(body.get("limit") or 10), MAX_LIMIT))
    try:
        offset = int(body.get("after") or 0)
    except ValueError:
        raise ApiError(400, f"Invalid after: {body.get('after')}")
    defs = await conn.fetch("SELECT name, type, field_type FROM property_defs WHERE object_type=$1", otype)
    types = {r["name"]: r["type"] for r in defs}
    for r in defs:
        if r["field_type"] == "checkbox":
            types[f"__checkbox__{r['name']}"] = "1"
    q = Q()
    where = [f"o.object_type = '{otype}'", "NOT o.archived"]  # literal: lets partial indexes apply
    groups = body.get("filterGroups") or []
    if len(groups) > 5:
        raise ApiError(400, "Too many filter groups (max 5)")
    ors = []
    for g in groups:
        filters = g.get("filters") or []
        if filters:
            ors.append("(" + " AND ".join(_filter(q, otype, f, types) for f in filters) + ")")
    if ors:
        where.append("(" + " OR ".join(ors) + ")")
    text = (body.get("query") or "").strip()
    if text:
        cols = " || ' ' || ".join(f"coalesce(o.properties->>'{c}', '')" for c in QUERY_PROPS.get(otype, ["name"]))
        where.append(f"lower({cols}) LIKE {q.p('%' + text.lower() + '%')}")
    order = []
    for s in body.get("sorts") or []:
        if isinstance(s, str):
            name, direction = s.lstrip("-"), "DESC" if s.startswith("-") else "ASC"
        else:
            name, direction = s.get("propertyName") or "", (s.get("direction") or "ASCENDING").upper()
            direction = "DESC" if direction.startswith("DESC") else "ASC"
        if not _SAFE.match(name) or name.startswith("associations."):
            raise ApiError(400, f"Invalid sort {name!r}")
        order.append(f"{_expr(name, types.get(name, 'string'))} {direction} NULLS LAST")
    order.append("o.id ASC")
    sql_where = " AND ".join(where)
    total = await conn.fetchval(f"SELECT count(*) FROM objects o WHERE {sql_where}", *q.args)
    rows = await conn.fetch(
        f"SELECT o.* FROM objects o WHERE {sql_where} ORDER BY {', '.join(order)} LIMIT {limit} OFFSET {offset}",
        *q.args)
    nxt = offset + limit if offset + limit < total else None
    return rows, total, nxt

