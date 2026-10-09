"""Properties and pipelines (read side in the scaffold).
Mounted at /crm/properties/2026-09 + /crm/v3/properties and /crm/pipelines/2026-09 + /crm/v3/pipelines.
Lane A: POST/PATCH/DELETE properties (hasUniqueValue!), groups, batch; pipeline + stage CRUD."""
from __future__ import annotations

from fastapi import APIRouter

from .. import db, store
from ..errors import ApiError

properties_router = APIRouter()
pipelines_router = APIRouter()


def prop_json(r) -> dict:
    return {
        "name": r["name"], "label": r["label"], "type": r["type"], "fieldType": r["field_type"],
        "groupName": r["group_name"], "description": r["description"], "options": r["options"],
        "displayOrder": r["display_order"], "hasUniqueValue": r["has_unique_value"], "hidden": r["hidden"],
        "formField": r["form_field"], "calculated": r["calculated"], "externalOptions": False,
        "archived": r["archived"],
        "modificationMetadata": {"archivable": not r["hubspot_defined"], "readOnlyDefinition": r["hubspot_defined"],
                                 "readOnlyValue": r["read_only"]},
        "createdAt": store.iso(r["created_at"]), "updatedAt": store.iso(r["updated_at"]),
        **({"hubspotDefined": True} if r["hubspot_defined"] else {}),
    }


@properties_router.get("/{objectType}")
async def list_properties(objectType: str, archived: bool = False):
    otype = store.resolve_type(objectType)
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM property_defs WHERE object_type=$1 AND archived=$2 ORDER BY display_order, name",
                                otype, archived)
    return {"results": [prop_json(r) for r in rows]}


@properties_router.get("/{objectType}/{propertyName}")
async def get_property(objectType: str, propertyName: str):
    otype = store.resolve_type(objectType)
    async with db.pool.acquire() as conn:
        r = await conn.fetchrow("SELECT * FROM property_defs WHERE object_type=$1 AND name=$2 AND NOT archived",
                                otype, propertyName)
    if not r:
        raise ApiError(404, f"Unable to find property {propertyName} on {otype}", "OBJECT_NOT_FOUND")
    return prop_json(r)


async def pipeline_json(conn, p) -> dict:
    stages = await conn.fetch(
        "SELECT * FROM pipeline_stages WHERE object_type=$1 AND pipeline_id=$2 AND NOT archived ORDER BY display_order",
        p["object_type"], p["id"])
    return {
        "id": p["id"], "label": p["label"], "displayOrder": p["display_order"], "archived": p["archived"],
        "createdAt": store.iso(p["created_at"]), "updatedAt": store.iso(p["updated_at"]),
        "stages": [{
            "id": s["id"], "label": s["label"], "displayOrder": s["display_order"], "metadata": s["metadata"],
            "archived": s["archived"], "createdAt": store.iso(s["created_at"]), "updatedAt": store.iso(s["updated_at"]),
            "writePermissions": "CRM_PERMISSIONS_ENFORCEMENT",
        } for s in stages],
    }


@pipelines_router.get("/{objectType}")
async def list_pipelines(objectType: str):
    otype = store.resolve_type(objectType)
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM pipelines WHERE object_type=$1 AND NOT archived ORDER BY display_order, id", otype)
        return {"results": [await pipeline_json(conn, p) for p in rows]}


@pipelines_router.get("/{objectType}/{pipelineId}")
async def get_pipeline(objectType: str, pipelineId: str):
    otype = store.resolve_type(objectType)
    async with db.pool.acquire() as conn:
        p = await conn.fetchrow("SELECT * FROM pipelines WHERE object_type=$1 AND id=$2 AND NOT archived", otype, pipelineId)
        if not p:
            raise ApiError(404, f"Unable to find pipeline {pipelineId}", "OBJECT_NOT_FOUND")
        return await pipeline_json(conn, p)
