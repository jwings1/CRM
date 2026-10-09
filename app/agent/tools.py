"""Restricted CRM tools. All record mutations use the shared store and read back."""
from __future__ import annotations

import inspect
from datetime import datetime
from decimal import Decimal

from .. import db, search, store
from ..errors import ApiError


def tool(name, description, properties, required=()):
    return {"type": "function", "function": {"name": name, "description": description,
            "parameters": {"type": "object", "properties": properties, "required": list(required),
                           "additionalProperties": False}}}

S = {"type": "string"}
O = {"type": "object"}
T = {"type": "string", "description": "companies, contacts, deals, tickets, products, line_items, notes, calls, emails, meetings, tasks"}
TOOLS = [
    tool("search_records", "Search CRM. filterGroups use HubSpot operators; associations.companies EQ company ID finds its deals/contacts. Exact total and pagination. Never assume the first match is the intended record.",
         {"object_type": T, "query": S, "filterGroups": {"type": "array", "items": O}, "sorts": {"type": "array", "items": {}}, "limit": {"type": "integer"}, "after": S, "my_customers": {"type": "boolean"}}, ["object_type"]),
    tool("get_record", "Read all properties and associated records, using CRM ID or id_property=id_legacy/email. Required before an update.",
         {"object_type": T, "id": S, "id_property": S}, ["object_type", "id"]),
    tool("list_pipelines", "Get exact pipeline and stage IDs/labels. Never invent stage IDs.", {"object_type": T}, ["object_type"]),
    tool("list_properties", "Get writable property names, types and allowed enum values.", {"object_type": T}, ["object_type"]),
    tool("list_users", "Resolve employee names/emails and check active status before assignments.", {"query": S}),
    tool("create_record", "Create one explicitly requested record. Associations reference previously read IDs. Returns persisted record and automation results.",
         {"object_type": T, "properties": O, "associations": {"type": "array", "items": {"type": "object", "properties": {"object_type": T, "id": S}, "required": ["object_type", "id"]}}}, ["object_type", "properties"]),
    tool("update_record", "Patch only explicitly requested fields on a previously read, unambiguous record. Empty string clears a field. Runs all CRM rules and reads back.",
         {"object_type": T, "id": S, "properties": O}, ["object_type", "id", "properties"]),
    tool("associate", "Associate two previously read records using the default association. Does not replace the primary company.",
         {"from_type": T, "from_id": S, "to_type": T, "to_id": S}, ["from_type", "from_id", "to_type", "to_id"]),
    tool("company_revenue", "Exact won-deal revenue for a company/year, net of refunds. EUR; USD x0.92, GBP x1.17. For 2025 use authoritative fatturato_2025 when present.",
         {"company_id": S, "year": {"type": "integer"}}, ["company_id", "year"]),
]


class Session:
    def __init__(self, context):
        self.context = context
        self.seen = set()
        self.writes = []
        self.ambiguous = set()
        self.now = None
        if context.get("now"):
            self.now = datetime.fromisoformat(str(context["now"]).replace("Z", "+00:00"))
            if self.now.tzinfo is None:
                raise ApiError(400, "context.now deve includere il fuso orario")

    async def record(self, conn, otype, ident, id_property=None):
        row = await store.get(conn, otype, ident, id_property)
        oid = str(row["id"])
        self.seen.add((otype, oid))
        assocs = await store.assoc_rows(conn, int(oid))
        targets = sorted({(a["to_type"], a["to_id"]) for a in assocs})
        linked = await conn.fetch("SELECT * FROM objects WHERE id=ANY($1::bigint[]) AND NOT archived ORDER BY id LIMIT 100",
                                  list({i for _, i in targets})) if targets else []
        return {"id": oid, "object_type": otype, "properties": row["properties"],
                "associations": [{"object_type": t, "id": str(i)} for t, i in targets[:100]],
                "association_count": len(targets), "associated_records": [
                    {"id": str(r["id"]), "object_type": r["object_type"], "properties": r["properties"]} for r in linked]}

    def require_seen(self, otype, ident):
        if (otype, str(ident)) not in self.seen:
            raise ApiError(400, "Leggi prima il record con get_record; non inventare ID")

    async def users(self, conn, query=""):
        if not await conn.fetchval("SELECT to_regclass('public.agent_users')"):
            return []
        return [dict(r) for r in await conn.fetch(
            "SELECT legacy_id,email,name,active FROM agent_users WHERE $1='' OR name ILIKE '%'||$1||'%' "
            "OR email ILIKE '%'||$1||'%' OR legacy_id=$1 ORDER BY name LIMIT 100", query)]

    async def assignments(self, conn, props):
        for key in ("commerciale", "assegnatario", "autore"):
            if props.get(key):
                matches = await self.users(conn, str(props[key]))
                exact = [u for u in matches if str(props[key]).casefold() in
                         (u["email"].casefold(), u["name"].casefold(), u["legacy_id"].casefold())]
                if len(exact) != 1 or not exact[0]["active"]:
                    raise ApiError(400, f"{key}: utente non trovato, ambiguo o non più attivo. Nessuna modifica eseguita.")
                props[key] = exact[0]["email"]

    async def execute(self, name, args):
        async with db.pool.acquire() as conn:
            if name == "list_users":
                return {"users": await self.users(conn, args.get("query", ""))}
            if name == "associate":
                ft, tt = store.resolve_type(args["from_type"]), store.resolve_type(args["to_type"])
                self.require_seen(ft, args["from_id"]); self.require_seen(tt, args["to_id"])
                async with conn.transaction():
                    await store.associate(conn, ft, int(args["from_id"]), tt, int(args["to_id"]))
                    result = await self.record(conn, ft, args["from_id"])
                self.writes.append({"operation": name, "record": result})
                return result
            if name == "company_revenue":
                cid, year = str(args["company_id"]), int(args["year"])
                company = await self.record(conn, "companies", cid)
                if year == 2025 and company["properties"].get("fatturato_2025") is not None:
                    return {"company": company["properties"].get("name"), "year": year,
                            "revenue_eur": company["properties"]["fatturato_2025"], "source": "fatturato_2025"}
                rows = await conn.fetch(
                    "SELECT o.properties FROM objects o JOIN pipeline_stages s ON s.object_type='deals' "
                    "AND s.pipeline_id=o.properties->>'pipeline' AND s.id=o.properties->>'dealstage' "
                    "WHERE o.object_type='deals' AND NOT o.archived AND s.metadata->>'probability'='1.0' "
                    "AND substring(o.properties->>'closedate',1,4)=$2 AND EXISTS "
                    "(SELECT 1 FROM associations a WHERE a.from_id=o.id AND a.to_type='companies' AND a.to_id=$1)", int(cid), str(year))
                total = Decimal(0)
                for row in rows:
                    p = row["properties"]
                    amount = Decimal(p.get("amount") or "0")
                    if "storno" in p.get("dealname", "").casefold():
                        amount = -abs(amount)
                    total += amount * {"EUR": Decimal(1), "USD": Decimal("0.92"), "GBP": Decimal("1.17")}.get(p.get("deal_currency_code") or "EUR", Decimal(1))
                return {"year": year, "revenue_eur": str(total.quantize(Decimal("0.01"))), "deal_count": len(rows)}
            ot = store.resolve_type(args["object_type"])
            if name == "get_record":
                return await self.record(conn, ot, args["id"], args.get("id_property"))
            if name == "list_pipelines":
                pipelines = await conn.fetch("SELECT id,label FROM pipelines WHERE object_type=$1 AND NOT archived ORDER BY display_order", ot)
                return {"pipelines": [{**dict(p), "stages": [dict(s) for s in await conn.fetch(
                    "SELECT id,label,metadata FROM pipeline_stages WHERE object_type=$1 AND pipeline_id=$2 AND NOT archived ORDER BY display_order", ot, p["id"])]} for p in pipelines]}
            if name == "list_properties":
                return {"properties": [dict(r) for r in await conn.fetch(
                    "SELECT name,label,type,options,read_only FROM property_defs WHERE object_type=$1 AND NOT archived ORDER BY name", ot)]}
            if name == "search_records":
                body = {k: v for k, v in args.items() if k not in ("object_type", "my_customers")}
                body["limit"] = min(int(body.get("limit") or 20), 50)
                if args.get("my_customers"):
                    if ot != "companies" or not self.context.get("user"):
                        raise ApiError(400, "Per i miei clienti serve context.user e object_type companies")
                    ids = await conn.fetch(
                        "SELECT DISTINCT a.to_id FROM associations a JOIN objects o ON o.id=a.from_id "
                        "WHERE a.to_type='companies' AND NOT o.archived AND "
                        "((o.object_type='deals' AND lower(o.properties->>'commerciale')=lower($1)) OR "
                        "(o.object_type='tickets' AND lower(o.properties->>'assegnatario')=lower($1)))", self.context["user"])
                    f = {"propertyName": "hs_object_id", "operator": "IN", "values": [str(r["to_id"]) for r in ids]}
                    body["filterGroups"] = [{"filters": g.get("filters", [])+[f]} for g in body.get("filterGroups") or [{}]]
                rows, total, after = await search.search(conn, ot, body)
                results = [{"id": str(r["id"]), "properties": r["properties"]} for r in rows]
                # Names may match multiple records; the model must ask before choosing.
                if total > 1 and body.get("query"):
                    self.ambiguous.update((ot, r["id"]) for r in rows)
                return {"results": results, "total": total, "after": str(after) if after is not None else None}
            if name not in ("create_record", "update_record"):
                raise ApiError(400, "Strumento sconosciuto")
            props = dict(args["properties"])
            await self.assignments(conn, props)
            extra = {"effective_now": self.now} if "effective_now" in inspect.signature(store.create).parameters else {}
            async with conn.transaction():
                if name == "update_record":
                    self.require_seen(ot, args["id"])
                    before = await store.get(conn, ot, args["id"])
                    row = await store.update(conn, ot, args["id"], props, **extra)
                else:
                    before = None
                    assocs = []
                    for a in args.get("associations") or []:
                        tt = store.resolve_type(a["object_type"])
                        self.require_seen(tt, a["id"])
                        assocs.append((tt, int(a["id"]), None))
                    row = await store.create(conn, ot, props, assocs or None, **extra)
                result = await self.record(conn, ot, row["id"])
                result["changes"] = {k: {"before": before["properties"].get(k) if before else None,
                                         "after": result["properties"].get(k)} for k in props}
            self.writes.append({"operation": name, "record": result})
            return result
