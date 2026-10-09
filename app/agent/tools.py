"""Request-local tool execution and verified actions through app.store."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .. import db, store
from ..defaults import ASSOC_TYPES
from ..errors import ApiError
from . import csv_import, kb, read


def definition(name: str, description: str, properties: dict, required: tuple = ()) -> dict:
    return {"type": "function", "function": {"name": name, "description": description,
            "parameters": {"type": "object", "properties": properties, "required": list(required), "additionalProperties": False}}}


S = {"type": "string"}
I = {"type": "integer"}
B = {"type": "boolean"}
O = {"type": "object", "additionalProperties": True}
REF = {"type": "object", "properties": {"object_type": S, "id": S}, "required": ["object_type", "id"], "additionalProperties": False}
FILTERS = {"type": "array", "items": {"type": "object", "properties": {
    "filters": {"type": "array", "items": O}}, "required": ["filters"]}}
SEARCH = {"object_type": S, "query": S, "filter_groups": FILTERS, "related_to": REF,
          "my_customers": B, "after": I, "limit": I,
          "sorts": {"type": "array", "items": S}}

TOOL_DEFINITIONS = [
    definition("list_kb_documents", "List current published knowledge documents and revisions.", {}),
    definition("search_knowledge_base", "Search live Postgres company documents. Use short Italian keywords, an R number, document ID or SKU. Empty results mean no document found.", {"query": S, "max_results": I}, ("query",)),
    definition("get_kb_document", "Read a full published document, optionally a specific revision.", {"doc_id": S, "revision": I}, ("doc_id",)),
    definition("get_related_knowledge", "Read an internal graph neighborhood and documents applicable to a CRM record. This graph is live; depth at most two.", {**REF["properties"], "depth": I}, ("object_type", "id")),
    definition("search_records", "Search live CRM records. filter_groups is OR of groups of AND filters: propertyName, operator, value/values/highValue. Supports associations.TYPE. For my customers set my_customers=true on companies. Multiple matches require clarification before writing.", SEARCH, ("object_type",)),
    definition("get_record", "Read current properties and association IDs. Use id_property=id_legacy/email/hs_sku for exact identity lookups.", {"object_type": S, "id": S, "id_property": S}, ("object_type", "id")),
    definition("get_related_records", "List records directly associated with a verified record, deduplicated; follow after for further pages.", {**REF["properties"], "target_type": S, "after": I, "limit": I}, ("object_type", "id")),
    definition("get_activity_history", "Read notes, calls, emails and meetings for a record. For a company includes history on its contacts and deals.", {**REF["properties"], "after": I, "limit": I}, ("object_type", "id")),
    definition("list_pipelines", "Read real pipeline/stage IDs and property definitions/options before creating or patching properties.", {"object_type": S}, ("object_type",)),
    definition("list_users", "Find imported employees by email, name or legacy ID and check whether they are active.", {"query": S, "active_only": B}),
    definition("aggregate_records", "Compute exact count or sum over ALL matching records in code. Monetary sums remain separated by currency. Missing values are disclosed. Never add numbers yourself.", {**SEARCH, "operation": {"type": "string", "enum": ["count", "sum"]}, "field": S, "group_by": S}, ("object_type", "operation")),
    definition("create_record", "Create ONLY a record requested by the user. Properties are validated; associations target previously verified records. Hooks fire and result is read back.", {"object_type": S, "properties": O, "associations": {"type": "array", "items": REF}}, ("object_type", "properties")),
    definition("update_record", "Patch ONLY requested fields on a previously resolved record. Never select an arbitrary match. Read-back and automation outcomes are returned.", {"object_type": S, "id": S, "properties": O}, ("object_type", "id", "properties")),
    definition("archive_record", "Archive a previously resolved record ONLY when explicitly requested by the user.", REF["properties"], ("object_type", "id")),
    definition("associate", "Associate two previously verified records when the user requests it. Optional association_type_id must match the object types.", {"from": REF, "to": REF, "association_type_id": I}, ("from", "to")),
    definition("preview_csv", "Read a supplied CSV attachment by index, columns, row count and first rows. Never invent attachment content.", {"attachment_index": I}, ("attachment_index",)),
    definition("apply_csv", "Atomically apply a supplied CSV attachment through the store. Specify object_type, create/update/upsert mode and identity property; ask if unclear. Any invalid row rolls back the whole batch.", {"attachment_index": I, "object_type": S, "mode": {"type": "string", "enum": ["create", "update", "upsert"]}, "id_property": S}, ("attachment_index", "object_type", "mode", "id_property")),
]
WRITE_TOOLS = {"create_record", "update_record", "archive_record", "associate", "apply_csv"}
_WRITE_INTENT = re.compile(r"\b(segn\w*|spost\w*|cre\w*|aggiorn\w*|modific\w*|assegn\w*|associ\w*|archivi\w*|elimin\w*|cancell\w*|import\w*|caric\w*|aggiung\w*|chiud\w*|vinta|persa|metti|porta|imposta|registra|collega|apri|inserisci|scrivi|mark|update|create|assign|archive|delete|associate|import|add|set|close)\b", re.I)


@dataclass
class RunState:
    user: str
    now: datetime | None
    user_text: str
    attachments: list[dict] = field(default_factory=list)
    allow_writes: bool = False
    sources: list[str] = field(default_factory=list)
    records: dict[tuple[str, str], dict] = field(default_factory=dict)
    ambiguous: set[tuple[str, str]] = field(default_factory=set)
    actions: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def remember_record(self, item: dict, ambiguous: bool = False) -> None:
        key = (item["object_type"], str(item["id"]))
        self.records[key] = item
        source = f"{key[0]}:{key[1]}"
        if source not in self.sources:
            self.sources.append(source)
        if ambiguous:
            self.ambiguous.add(key)

    def remember_document(self, document: dict) -> None:
        source = f"{document['doc_id']}@{document['revision']}"
        if source not in self.sources:
            self.sources.append(source)

    def require_record(self, object_type: str, identifier) -> None:
        key = (store.resolve_type(object_type), str(identifier))
        if key not in self.records or key in self.ambiguous:
            raise ApiError(400, "Resolve the exact record first; ambiguous targets require user clarification")

    def attachment(self, index: int) -> dict:
        if not isinstance(index, int) or index < 0 or index >= len(self.attachments):
            raise ApiError(400, "Attachment index not found")
        attachment = self.attachments[index]
        if attachment.get("content_type", "text/csv") != "text/csv" or not isinstance(attachment.get("content"), str):
            raise ApiError(400, "Only supplied text/csv attachments can be applied")
        return attachment


def write_intent(messages: list[dict]) -> bool:
    user_messages = [str(m.get("content") or "") for m in messages if m.get("role") == "user"]
    if not user_messages:
        return False
    latest = user_messages[-1]
    if _WRITE_INTENT.search(latest):
        return True
    # Permit a clarification reply only following an earlier action request.
    clarification = re.fullmatch(r"\s*(s[iì]|ok|conferm\w*|quell\w*|la\s+\w+|il\s+\w+|[\w.@+-]+)\s*[.!]?\s*", latest, re.I)
    return bool(clarification and any(_WRITE_INTENT.search(text) for text in user_messages[:-1]))


async def execute_tool(name: str, args: dict, state: RunState) -> Any:
    if name not in {t["function"]["name"] for t in TOOL_DEFINITIONS}:
        raise ApiError(400, f"Unknown tool {name}")
    if name == "preview_csv":
        attachment = state.attachment(args["attachment_index"])
        columns, rows = csv_import.parse(attachment["content"])
        return {"name": attachment.get("name"), "columns": columns, "total": len(rows), "preview": rows[:5]}
    if db.pool is None:
        raise ApiError(503, "CRM database unavailable")
    async with db.pool.acquire() as conn:
        if name in WRITE_TOOLS:
            if not state.allow_writes:
                raise ApiError(400, "The conversation does not authorize a CRM action")
            if not state.now:
                raise ApiError(400, "context.now is required for CRM actions")
            if not await conn.fetchval("SELECT EXISTS(SELECT 1 FROM agent_users WHERE lower(email)=lower($1) AND active)", state.user):
                raise ApiError(400, "context.user must be an imported active employee")
            return await _write(conn, name, args, state)
        if name == "list_kb_documents":
            return {"documents": await kb.list_documents(conn)}
        if name == "search_knowledge_base":
            docs = await kb.search_documents(conn, args["query"], args.get("max_results", 4))
            for doc in docs:
                state.remember_document(doc)
            return {"documents": docs}
        if name == "get_kb_document":
            doc = await kb.get_document(conn, args["doc_id"], args.get("revision"))
            state.remember_document(doc)
            return doc
        if name == "get_related_knowledge":
            result = await kb.related_knowledge(conn, args["object_type"], int(args["id"]), args.get("depth", 2))
            for doc in result["documents"]:
                state.remember_document(doc)
            # Graph identity does not authorize a write; use precise record tools.
            result["records"] = [{"id": r["id"], "object_type": r["object_type"],
                                  "label": r["properties"].get("name") or r["properties"].get("dealname") or r["properties"].get("subject"),
                                  "updated_at": r["updated_at"]} for r in result["records"]]
            return result
        if name == "search_records":
            result = await read.search_records(conn, args["object_type"], args, state.user)
            for row in result["records"]:
                state.remember_record(row, ambiguous=result["total"] > 1)
                if result["total"] == 1:
                    state.ambiguous.discard((row["object_type"], row["id"]))
            return result
        if name == "get_record":
            row = await read.get_record(conn, args["object_type"], args["id"], args.get("id_property"))
            state.remember_record(row)
            # An explicit identifier in the user's request disambiguates a target.
            if str(args["id"]).lower() in state.user_text.lower():
                state.ambiguous.discard((row["object_type"], row["id"]))
            return row
        if name in ("get_related_records", "get_activity_history"):
            result = await read.related_records(conn, args["object_type"], args["id"], args.get("target_type"),
                                                args.get("after", 0), args.get("limit", 50), name == "get_activity_history")
            for row in result["records"]:
                state.remember_record(row, ambiguous=result["total"] > 1)
            return result
        if name == "list_pipelines":
            return await read.metadata(conn, args["object_type"])
        if name == "list_users":
            return {"users": await read.list_users(conn, args.get("query", ""), args.get("active_only", False))}
        if name == "aggregate_records":
            result = await read.aggregate_records(conn, args["object_type"], args, state.user)
            state.sources.append(f"{store.resolve_type(args['object_type'])}:aggregate")
            return result
    raise ApiError(400, f"Unimplemented tool {name}")


async def _write(conn, name: str, args: dict, state: RunState) -> dict:
    action = {"operation": name}
    async with conn.transaction():
        if name == "apply_csv":
            attachment = state.attachment(args["attachment_index"])
            rows = await csv_import.apply(conn, args["object_type"], attachment["content"], args["mode"], args["id_property"], state.now)
            result = {"records": rows, "count": len(rows), "verified": True}
            action["count"] = len(rows)
        elif name == "associate":
            ft, tt = store.resolve_type(args["from"]["object_type"]), store.resolve_type(args["to"]["object_type"])
            fid, tid = int(args["from"]["id"]), int(args["to"]["id"])
            state.require_record(ft, fid)
            state.require_record(tt, tid)
            types = None
            if "association_type_id" in args:
                type_id = int(args["association_type_id"])
                if not any(t["from"] == ft and t["to"] == tt and t["type_id"] == type_id for t in ASSOC_TYPES):
                    raise ApiError(400, "Association type does not match these object types")
                types = [("HUBSPOT_DEFINED", type_id)]
            await store.associate(conn, ft, fid, tt, tid, types)
            row = await read.get_record(conn, ft, fid)
            result = {"record": row, "verified": any(r["to_id"] == tid for r in row["associations"])}
            action.update(object_type=ft, id=str(fid), changes={"associated_to": f"{tt}:{tid}"})
        else:
            object_type = store.resolve_type(args["object_type"])
            if name == "archive_record":
                state.require_record(object_type, args["id"])
                await store.archive(conn, object_type, args["id"])
                row = await store.get(conn, object_type, args["id"], archived=True)
                result = {"record": read.record(row), "verified": row["archived"]}
                action.update(object_type=object_type, id=str(row["id"]), changes={"archived": True})
            else:
                props = await csv_import.normalize_properties(conn, object_type, args["properties"])
                if name == "update_record":
                    state.require_record(object_type, args["id"])
                    row = await store.update(conn, object_type, args["id"], props, effective_now=state.now)
                else:
                    associations = []
                    for target in args.get("associations", []):
                        target_type = store.resolve_type(target["object_type"])
                        state.require_record(target_type, target["id"])
                        associations.append((target_type, int(target["id"]), None))
                    row = await store.create(conn, object_type, props, associations or None, effective_now=state.now)
                current = await read.get_record(conn, object_type, row["id"])
                result = {"record": current, "verified": True}
                if object_type == "deals":
                    result["automation_records"] = []
                    for target_type in ("tickets", "tasks"):
                        linked = await read.related_records(conn, object_type, row["id"], target_type)
                        result["automation_records"].extend(linked["records"])
                action.update(object_type=object_type, id=str(row["id"]),
                              changes={key: current["properties"].get(key) for key in props})
    # Record only committed actions; failed CSV batches never reach this line.
    state.actions.append(action)
    for row in result.get("records", []) + ([result["record"]] if "record" in result else []) + result.get("automation_records", []):
        state.remember_record(row)
    return result
