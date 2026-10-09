"""Service layer. EVERY write to CRM records goes through here (REST API, batch,
assistant), so validation, uniqueness (R7) and automations (R10/R11/R12) apply
everywhere. Only the bulk migration bypasses it.

Conventions
- property values are stored as strings (None/"" on update = clear the property)
- ids are global BIGINTs from object_id_seq, exposed as strings
- updates merge in SQL under SELECT ... FOR UPDATE: no lost values under concurrency
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

import asyncpg

from .defaults import (DEFAULT_ASSOC, DEFAULT_RETURNED, INVERSE, OBJECT_TYPES, PRIMARY_ASSOC,
                       canon_type, lastmod_prop)
from .errors import ApiError, not_found

# ---------------------------------------------------------------- time / values

def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def now_iso() -> str:
    return iso(utcnow())


def to_str(v: Any) -> str | None:
    if v is None:
        return None
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else repr(v)
    if isinstance(v, (list, tuple)):
        return ";".join(str(x) for x in v)
    return str(v)


_DATE_ONLY = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def norm_datetime(v: str) -> str:
    """Accept epoch ms or ISO; store ISO-8601 UTC with ms and Z."""
    s = v.strip()
    if re.fullmatch(r"-?\d{9,}", s):
        return iso(datetime.fromtimestamp(int(s) / 1000, tz=timezone.utc))
    if _DATE_ONLY.match(s):
        return f"{s}T00:00:00.000Z"
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return iso(dt)
    except ValueError:
        raise ApiError(400, f"{v} is not a valid datetime", errors=[{"message": f"{v} was not a valid datetime", "code": "INVALID_DATE"}])


def norm_piva(v: str) -> str:
    s = re.sub(r"[\s.\-]", "", v).upper()
    if s.startswith("IT"):
        s = s[2:]
    return s if re.fullmatch(r"\d{11}", s) else v.strip()


def bare_domain(v: str) -> str:
    s = v.strip().lower()
    s = re.sub(r"^[a-z]+://", "", s)
    s = s.split("/")[0].split("?")[0]
    return s[4:] if s.startswith("www.") else s


# Brambilla-specific write normalizers (property -> fn). Keep tiny.
NORMALIZERS: dict[str, dict[str, Any]] = {
    "companies": {"partita_iva": norm_piva},
}


def resolve_type(name: str) -> str:
    t = canon_type(name)
    if not t:
        raise ApiError(400, f"Unable to infer object type from: {name}", "VALIDATION_ERROR")
    return t


# ---------------------------------------------------------------- validation

def _invalid(errors: list[dict]) -> ApiError:
    detail = ", ".join(e["message"] for e in errors)
    return ApiError(400, f"Property values were not valid: {detail}", "VALIDATION_ERROR", errors=errors)


async def prepare(conn, otype: str, properties: dict | None, *, validate: bool = True) -> tuple[dict, set[str]]:
    """Stringify, validate and normalize input properties.
    Returns (props, unique_prop_names). Values None/"" mean 'clear'."""
    raw = properties or {}
    if not isinstance(raw, dict):
        raise ApiError(400, "properties must be an object")
    lm = lastmod_prop(otype)
    props = {k: to_str(v) for k, v in raw.items() if k not in ("hs_object_id", lm)}
    if not props:
        return props, set()
    defs = {r["name"]: r for r in await conn.fetch(
        "SELECT name, type, field_type, options, has_unique_value FROM property_defs "
        "WHERE object_type = $1 AND name = ANY($2::text[]) AND NOT archived", otype, list(props))}
    errors = []
    uniques = set()
    norm = NORMALIZERS.get(otype, {})
    for k, v in list(props.items()):
        d = defs.get(k)
        if d is None:
            if validate:
                errors.append({"message": f'Property "{k}" does not exist', "code": "PROPERTY_DOESNT_EXIST",
                               "context": {"propertyName": [k]}})
            continue
        if d["has_unique_value"]:
            uniques.add(k)
        if v is None or v == "":
            continue
        if k in norm:
            v = props[k] = norm[k](v)
        t = d["type"]
        if t == "number":
            try:
                float(v)
            except ValueError:
                if validate:
                    errors.append({"message": f"{v} was not a valid number", "code": "INVALID_FLOAT",
                                   "context": {"propertyName": [k]}})
        elif t in ("datetime", "date"):
            try:
                props[k] = norm_datetime(v)
            except ApiError:
                if validate:
                    errors.append({"message": f"{v} was not a valid date", "code": "INVALID_DATE",
                                   "context": {"propertyName": [k]}})
        elif t == "enumeration" and d["options"] and validate:
            allowed = {o["value"] for o in d["options"]}
            parts = v.split(";") if d["field_type"] == "checkbox" else [v]
            bad = [p for p in parts if p not in allowed]
            if bad:
                errors.append({"message": f'{bad[0]} was not one of the allowed options: {sorted(allowed)}',
                               "code": "INVALID_OPTION", "context": {"propertyName": [k]}})
        elif t == "bool":
            props[k] = "true" if v.lower() in ("true", "1", "yes") else "false"
    if errors:
        raise _invalid(errors)
    return props, uniques


async def _claim_uniques(conn, otype: str, oid: int, props: dict, uniques: Iterable[str]) -> None:
    for k in uniques:
        v = props.get(k)
        await conn.execute("DELETE FROM unique_values WHERE object_id = $1 AND property = $2", oid, k)
        if v in (None, ""):
            continue
        try:
            async with conn.transaction():
                await conn.execute(
                    "INSERT INTO unique_values (object_type, property, value, object_id) VALUES ($1,$2,$3,$4)",
                    otype, k, v, oid)
        except asyncpg.UniqueViolationError:
            other = await conn.fetchval(
                "SELECT object_id FROM unique_values WHERE object_type=$1 AND property=$2 AND value=$3", otype, k, v)
            raise ApiError(409, f'A {OBJECT_TYPES[otype][1]} with {k}={v} already exists. Existing ID: {other}',
                           "CONFLICT", context={"propertyName": [k], "existingId": [str(other)]})


async def _apply_type_defaults(conn, otype: str, props: dict, existing: dict | None = None) -> None:
    cur = {**(existing or {}), **{k: v for k, v in props.items() if v not in (None, "")}}
    if otype == "deals" and cur.get("dealstage") and not cur.get("pipeline"):
        props["pipeline"] = "default"
    if otype == "tickets" and existing is None:
        pipe = cur.get("hs_pipeline") or "0"
        props.setdefault("hs_pipeline", pipe)
        if not cur.get("hs_pipeline_stage"):
            first = await conn.fetchval(
                "SELECT id FROM pipeline_stages WHERE object_type='tickets' AND pipeline_id=$1 AND NOT archived "
                "ORDER BY display_order LIMIT 1", pipe)
            if first:
                props["hs_pipeline_stage"] = first


# ---------------------------------------------------------------- reads

async def fetch_row(conn, otype: str, id_value: str | int, id_property: str | None = None,
                    archived: bool = False, for_update: bool = False):
    lock = " FOR UPDATE" if for_update else ""
    if id_property and id_property not in ("hs_object_id", "id"):
        if id_property == "email" and otype == "contacts":
            return await conn.fetchrow(
                "SELECT * FROM objects WHERE object_type='contacts' AND archived=$2 "
                f"AND lower(properties->>'email') = lower($1) ORDER BY id LIMIT 1{lock}", str(id_value), archived)
        return await conn.fetchrow(
            f"SELECT * FROM objects WHERE object_type=$1 AND archived=$3 AND properties->>$2 = $4 "
            f"ORDER BY id LIMIT 1{lock}", otype, id_property, archived, str(id_value))
    try:
        oid = int(id_value)
    except (TypeError, ValueError):
        return None
    return await conn.fetchrow(
        f"SELECT * FROM objects WHERE id=$1 AND object_type=$2 AND archived=$3{lock}", oid, otype, archived)


async def get(conn, otype: str, id_value, id_property: str | None = None, archived: bool = False):
    row = await fetch_row(conn, otype, id_value, id_property, archived)
    if row is None:
        raise not_found(otype, id_value)
    return row


async def list_page(conn, otype: str, limit: int = 10, after: str | None = None, archived: bool = False):
    limit = max(1, min(int(limit or 10), 100))
    try:
        after_id = int(after) if after else 0
    except ValueError:
        raise ApiError(400, f"Invalid after: {after}")
    rows = await conn.fetch(
        "SELECT * FROM objects WHERE object_type=$1 AND archived=$2 AND id > $3 ORDER BY id LIMIT $4",
        otype, archived, after_id, limit + 1)
    more = len(rows) > limit
    rows = rows[:limit]
    return rows, (str(rows[-1]["id"]) if more and rows else None)


def serialize(otype: str, row, properties: list[str] | None = None,
              associations: dict[str, list] | None = None) -> dict:
    p = row["properties"]
    names = properties or DEFAULT_RETURNED[otype]
    out = {n: p.get(n) for n in names}
    for sys_prop in ("hs_object_id", "createdate" if otype in ("contacts", "companies", "deals", "tickets", "products", "line_items") else "hs_createdate", lastmod_prop(otype)):
        out.setdefault(sys_prop, p.get(sys_prop))
    out["hs_object_id"] = str(row["id"])
    res = {
        "id": str(row["id"]),
        "properties": out,
        "createdAt": iso(row["created_at"]),
        "updatedAt": iso(row["updated_at"]),
        "archived": row["archived"],
    }
    if row["archived"]:
        res["archivedAt"] = iso(row["archived_at"])
    if associations:
        res["associations"] = associations
    return res


# ---------------------------------------------------------------- associations

async def assoc_rows(conn, oid: int, to_type: str | None = None):
    if to_type:
        return await conn.fetch(
            "SELECT to_type, to_id, category, type_id FROM associations WHERE from_id=$1 AND to_type=$2 "
            "ORDER BY to_id", oid, to_type)
    return await conn.fetch(
        "SELECT to_type, to_id, category, type_id FROM associations WHERE from_id=$1 ORDER BY to_type, to_id", oid)


def _assoc_name(from_type: str, to_type: str, type_id: int) -> str:
    base = f"{OBJECT_TYPES[from_type][1]}_to_{OBJECT_TYPES[to_type][1]}"
    if (from_type, to_type) in PRIMARY_ASSOC and type_id == DEFAULT_ASSOC.get((from_type, to_type)):
        return base + "_unlabeled"
    return base


async def associations_v3(conn, otype: str, oid: int, to_types: list[str]) -> dict:
    out = {}
    for t in to_types:
        tt = canon_type(t)
        if not tt:
            continue
        rows = await assoc_rows(conn, oid, tt)
        if rows:
            out[tt] = {"results": [{"id": str(r["to_id"]), "type": _assoc_name(otype, tt, r["type_id"])}
                                   for r in rows]}
    return out


async def associate(conn, from_type: str, from_id: int, to_type: str, to_id: int,
                    types: list[tuple[str, int]] | None = None, *, check: bool = True) -> list[tuple[str, int]]:
    """Create association(s) in both directions. types=[(category, typeId)], None = default."""
    if check:
        n = await conn.fetchval(
            "SELECT count(*) FROM objects WHERE NOT archived AND ((id=$1 AND object_type=$2) OR (id=$3 AND object_type=$4))",
            from_id, from_type, to_id, to_type)
        if n != (1 if from_id == to_id else 2):
            raise ApiError(404, f"One or more objects not found: {from_type} {from_id}, {to_type} {to_id}", "OBJECT_NOT_FOUND")
    if not types:
        d = DEFAULT_ASSOC.get((from_type, to_type))
        if d is None:
            raise ApiError(400, f"No default association type from {from_type} to {to_type}")
        types = [("HUBSPOT_DEFINED", d)]
    rows = []
    for cat, tid in types:
        tid = int(tid)
        if cat == "HUBSPOT_DEFINED":
            inv = INVERSE.get(tid)
            if inv is None:
                raise ApiError(400, f"Unknown association type {tid} from {from_type} to {to_type}")
            prim = PRIMARY_ASSOC.get((from_type, to_type))
            if prim == tid or PRIMARY_ASSOC.get((to_type, from_type)) == inv:
                # one primary company per contact/deal/ticket: drop the old one
                child, child_type = (from_id, from_type) if from_type != "companies" else (to_id, to_type)
                ctid = PRIMARY_ASSOC.get((child_type, "companies"))
                if ctid is not None:
                    olds = await conn.fetch(
                        "DELETE FROM associations WHERE from_id=$1 AND to_type='companies' AND type_id=$2 RETURNING to_id",
                        child, ctid)
                    for o in olds:
                        await conn.execute(
                            "DELETE FROM associations WHERE from_id=$1 AND to_id=$2 AND type_id=$3",
                            o["to_id"], child, INVERSE[ctid])
                # HubSpot pairs a primary with the unlabeled default
                d = DEFAULT_ASSOC[(from_type, to_type)]
                rows.append((from_type, from_id, to_type, to_id, cat, d))
                rows.append((to_type, to_id, from_type, from_id, cat, INVERSE[d]))
        else:
            inv = tid  # USER_DEFINED labels: same id both ways unless Lane A adds a labels table
        rows.append((from_type, from_id, to_type, to_id, cat, tid))
        rows.append((to_type, to_id, from_type, from_id, cat, inv))
    await conn.executemany(
        "INSERT INTO associations (from_type, from_id, to_type, to_id, category, type_id) "
        "VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT DO NOTHING", rows)
    return types


async def unassociate(conn, from_id: int, to_id: int, type_ids: list[int] | None = None) -> None:
    if type_ids:
        inv = [INVERSE.get(t, t) for t in type_ids]
        await conn.execute("DELETE FROM associations WHERE from_id=$1 AND to_id=$2 AND type_id = ANY($3::int[])",
                           from_id, to_id, type_ids)
        await conn.execute("DELETE FROM associations WHERE from_id=$1 AND to_id=$2 AND type_id = ANY($3::int[])",
                           to_id, from_id, inv)
    else:
        await conn.execute("DELETE FROM associations WHERE (from_id=$1 AND to_id=$2) OR (from_id=$2 AND to_id=$1)",
                           from_id, to_id)


def parse_assoc_input(otype: str, items: list | None) -> list[tuple[str, int, list[tuple[str, int]]]]:
    """HubSpot create body: associations=[{to:{id}, types:[{associationCategory, associationTypeId}]}]
    Target type is inferred from the typeId."""
    from .defaults import ASSOC_TYPES
    out = []
    for a in items or []:
        to_id = int((a.get("to") or {}).get("id"))
        types = [(t.get("associationCategory", "HUBSPOT_DEFINED"), int(t["associationTypeId"]))
                 for t in a.get("types") or []]
        to_type = None
        for cat, tid in types:
            if cat == "HUBSPOT_DEFINED":
                for d in ASSOC_TYPES:
                    if d["type_id"] == tid and d["from"] == otype:
                        to_type = d["to"]
        out.append((to_type, to_id, types))
    return out


# ---------------------------------------------------------------- writes

async def create(conn, otype: str, properties: dict | None, associations: list | None = None, *,
                 validate: bool = True, run_hooks: bool = True):
    """associations: HubSpot body format, or [(to_type, to_id, [(cat, typeId)])]."""
    from . import hooks
    props, uniques = await prepare(conn, otype, properties, validate=validate)
    props = {k: v for k, v in props.items() if v not in (None, "")}
    async with conn.transaction():
        await _apply_type_defaults(conn, otype, props)
        oid = await conn.fetchval("SELECT nextval('object_id_seq')")
        now = utcnow()
        ck = "createdate" if otype in ("contacts", "companies", "deals", "tickets", "products", "line_items") else "hs_createdate"
        props.setdefault(ck, iso(now))
        props[lastmod_prop(otype)] = iso(now)
        props["hs_object_id"] = str(oid)
        if otype == "companies" and props.get("domain"):
            pass  # Lane A/B: decide whether to store bare_domain(props["domain"])
        await _claim_uniques(conn, otype, oid, props, uniques)
        try:
            async with conn.transaction():
                row = await conn.fetchrow(
                    "INSERT INTO objects (id, object_type, properties, created_at, updated_at) "
                    "VALUES ($1,$2,$3,$4,$4) RETURNING *", oid, otype, props, now)
        except asyncpg.UniqueViolationError:
            other = await conn.fetchval(
                "SELECT id FROM objects WHERE object_type='contacts' AND NOT archived AND lower(properties->>'email')=lower($1)",
                props.get("email", ""))
            raise ApiError(409, f"Contact already exists. Existing ID: {other}", "CONFLICT")
        if associations:
            items = associations
            if isinstance(items[0], dict):
                items = parse_assoc_input(otype, items)
            for to_type, to_id, types in items:
                if to_type is None:
                    raise ApiError(400, "Invalid association type for " + otype)
                await associate(conn, otype, oid, to_type, int(to_id), types or None)
        if run_hooks:
            await hooks.after_write(conn, otype, oid, None, row["properties"], created=True)
            if otype in ("deals", "contacts"):
                row = await conn.fetchrow("SELECT * FROM objects WHERE id=$1", oid)
    return row


async def update(conn, otype: str, id_value, properties: dict | None, *, id_property: str | None = None,
                 validate: bool = True, run_hooks: bool = True):
    from . import hooks
    props, uniques = await prepare(conn, otype, properties, validate=validate)
    async with conn.transaction():
        cur = await fetch_row(conn, otype, id_value, id_property, for_update=True)
        if cur is None:
            raise not_found(otype, id_value)
        oid = cur["id"]
        before = cur["properties"]
        await _apply_type_defaults(conn, otype, props, existing=before)
        set_props = {k: v for k, v in props.items() if v not in (None, "")}
        unset = [k for k, v in props.items() if v in (None, "")]
        set_props[lastmod_prop(otype)] = now_iso()
        await _claim_uniques(conn, otype, oid, {**before, **props}, [u for u in uniques if u in props])
        try:
            async with conn.transaction():
                row = await conn.fetchrow(
                    "UPDATE objects SET properties = (properties || $2::jsonb) - $3::text[], updated_at = now() "
                    "WHERE id=$1 RETURNING *", oid, set_props, unset)
        except asyncpg.UniqueViolationError:
            raise ApiError(409, "Contact already exists with this email", "CONFLICT")
        if run_hooks:
            await hooks.after_write(conn, otype, oid, before, row["properties"], created=False)
            if otype in ("deals", "contacts"):
                row = await conn.fetchrow("SELECT * FROM objects WHERE id=$1", oid)
    return row


async def archive(conn, otype: str, id_value) -> None:
    try:
        oid = int(id_value)
    except (TypeError, ValueError):
        return
    async with conn.transaction():
        done = await conn.fetchval(
            "UPDATE objects SET archived=true, archived_at=now(), updated_at=now() "
            "WHERE id=$1 AND object_type=$2 AND NOT archived RETURNING id", oid, otype)
        if done:
            await conn.execute("DELETE FROM unique_values WHERE object_id=$1", oid)
            await conn.execute("DELETE FROM associations WHERE from_id=$1 OR to_id=$1", oid)


# ---------------------------------------------------------------- bulk helpers (migration)

async def reserve_ids(conn, n: int) -> range:
    """Reserve n consecutive object ids. Use from the migration before COPY."""
    if n <= 0:
        return range(0)
    last = await conn.fetchval("SELECT setval('object_id_seq', nextval('object_id_seq') + $1 - 1)", n)
    return range(last - n + 1, last + 1)


def days_from(dt: datetime, days: int) -> str:
    return iso(dt + timedelta(days=days))
