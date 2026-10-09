"""Brambilla's schema, created by the migration (NOT by /__reset): appendix of RICHIESTE.md.
Idempotent: safe to run twice."""
from __future__ import annotations

from ..defaults import OBJECT_TYPES

ENGAGEMENTS = ["notes", "calls", "emails", "meetings"]

# (object types, name, label, type, fieldType, hasUniqueValue)
PROPERTIES = [
    (["companies", "contacts", "deals", "line_items", "tickets", *ENGAGEMENTS], "id_legacy", "ID Sinergia", "string", "text", False),
    (["deals"], "commerciale", "Commerciale", "string", "text", False),
    (["tickets"], "assegnatario", "Assegnatario", "string", "text", False),
    (ENGAGEMENTS, "autore", "Autore", "string", "text", False),
    (["companies"], "partita_iva", "Partita IVA", "string", "text", True),
    (["companies"], "fatturato_2025", "Fatturato 2025", "number", "number", False),
    (["companies"], "classe_cliente", "Classe cliente", "string", "text", False),
]

VENDITE_STAGES = {  # default deal pipeline = Sinergia "Vendite"
    "appointmentscheduled": "Contatto",
    "qualifiedtobuy": "Qualifica",
    "presentationscheduled": "Presentazione",
    "decisionmakerboughtin": "Decisione",
    "contractsent": "Contratto",
    "closedwon": "Vinta",
    "closedlost": "Persa",
}

RINNOVI = [  # (label, metadata)
    ("Da rinnovare", {"isClosed": "false", "probability": "0.2"}),
    ("In trattativa", {"isClosed": "false", "probability": "0.6"}),
    ("Rinnovato", {"isClosed": "true", "probability": "1.0"}),
    ("Non rinnovato", {"isClosed": "true", "probability": "0.0"}),
]

ASSISTENZA = [
    ("Aperto", {"ticketState": "OPEN", "isClosed": "false"}),
    ("In lavorazione", {"ticketState": "OPEN", "isClosed": "false"}),
    ("In attesa del cliente", {"ticketState": "OPEN", "isClosed": "false"}),
    ("Chiuso", {"ticketState": "CLOSED", "isClosed": "true"}),
]

DORMIENTI = "Clienti dormienti"


async def _pipeline(conn, otype: str, label: str, stages: list[tuple[str, dict]]) -> dict[str, str]:
    """Create pipeline if missing. Returns {stage label: stage id}."""
    pid = await conn.fetchval("SELECT id FROM pipelines WHERE object_type=$1 AND label=$2 AND NOT archived", otype, label)
    if pid is None:
        pid = str(await conn.fetchval("SELECT nextval('pipeline_id_seq')"))
        order = await conn.fetchval("SELECT coalesce(max(display_order), 0) + 1 FROM pipelines WHERE object_type=$1", otype)
        await conn.execute("INSERT INTO pipelines (object_type, id, label, display_order) VALUES ($1,$2,$3,$4)",
                           otype, pid, label, order)
        for i, (slabel, meta) in enumerate(stages):
            sid = str(await conn.fetchval("SELECT nextval('pipeline_id_seq')"))
            await conn.execute(
                "INSERT INTO pipeline_stages (object_type, pipeline_id, id, label, display_order, metadata) "
                "VALUES ($1,$2,$3,$4,$5,$6)", otype, pid, sid, slabel, i, meta)
    rows = await conn.fetch("SELECT id, label FROM pipeline_stages WHERE object_type=$1 AND pipeline_id=$2", otype, pid)
    return {"__pipeline__": pid, **{r["label"]: r["id"] for r in rows}}


async def ensure(conn) -> dict:
    """Create properties, pipelines and the dormant list. Returns ids the loader needs:
    {'rinnovi': {...}, 'assistenza': {...}, 'dormienti_list_id': int}"""
    rows = []
    for types, name, label, ptype, field, unique in PROPERTIES:
        for t in types:
            rows.append((t, name, label, ptype, field, f"{OBJECT_TYPES[t][1]}information", unique))
    await conn.executemany(
        "INSERT INTO property_defs (object_type, name, label, type, field_type, group_name, has_unique_value) "
        "VALUES ($1,$2,$3,$4,$5,$6,$7) ON CONFLICT (object_type, name) DO UPDATE SET "
        "label=EXCLUDED.label, type=EXCLUDED.type, field_type=EXCLUDED.field_type, "
        "has_unique_value=EXCLUDED.has_unique_value, archived=false, updated_at=now()", rows)

    await conn.execute("UPDATE pipelines SET label='Vendite', updated_at=now() WHERE object_type='deals' AND id='default'")
    for sid, label in VENDITE_STAGES.items():
        await conn.execute("UPDATE pipeline_stages SET label=$2, updated_at=now() "
                           "WHERE object_type='deals' AND pipeline_id='default' AND id=$1", sid, label)

    rinnovi = await _pipeline(conn, "deals", "Rinnovi", RINNOVI)
    assistenza = await _pipeline(conn, "tickets", "Assistenza", ASSISTENZA)

    list_id = await conn.fetchval("SELECT list_id FROM lists WHERE name=$1 AND NOT archived", DORMIENTI)
    if list_id is None:
        list_id = await conn.fetchval(
            "INSERT INTO lists (name, object_type_id, processing_type) VALUES ($1, '0-2', 'MANUAL') RETURNING list_id",
            DORMIENTI)
    return {"rinnovi": rinnovi, "assistenza": assistenza, "dormienti_list_id": list_id}
