"""Small, atomic assistant imports. Every row goes through the normal store."""
from __future__ import annotations

import csv
import io

from .. import store
from ..errors import ApiError
from ..migrate import normalize as normal
from . import read

ALIASES = {
    "companies": {"ragione_sociale": "name", "sito_web": "domain", "citta": "city", "provincia": "state", "id_azienda": "id_legacy"},
    "contacts": {"nome": "firstname", "cognome": "lastname", "telefono": "phone", "tipo": "lifecyclestage", "id_contatto": "id_legacy"},
    "deals": {"titolo": "dealname", "importo": "amount", "valuta": "deal_currency_code", "fase": "dealstage", "data_chiusura": "closedate", "id_commerciale": "commerciale", "id_opportunita": "id_legacy"},
    "products": {"codice_articolo": "hs_sku", "descrizione": "name", "prezzo_listino": "price"},
    "line_items": {"descrizione": "name", "quantita": "quantity", "prezzo_unitario": "price", "sconto": "hs_discount_percentage", "id_riga": "id_legacy"},
    "tickets": {"oggetto": "subject", "descrizione": "content", "priorita": "hs_ticket_priority", "aperto_il": "createdate", "chiuso_il": "closed_date", "id_utente": "assegnatario", "id_ticket": "id_legacy", "stato": "hs_pipeline_stage"},
}
REFERENCES = {"id_azienda": "companies", "id_contatto": "contacts", "id_opportunita": "deals"}


def parse(content: str) -> tuple[list[str], list[dict]]:
    try:
        reader = csv.DictReader(io.StringIO(content.lstrip("\ufeff"), newline=""), delimiter=";", strict=True)
        headers = [header.strip().lower() for header in reader.fieldnames or []]
        if not headers or len(headers) != len(set(headers)) or any(not h for h in headers):
            raise ApiError(400, "CSV requires unique, non-empty column names")
        reader.fieldnames = headers
        rows = []
        for line, raw in enumerate(reader, 2):
            if None in raw or any(v is None for v in raw.values()):
                raise ApiError(400, f"CSV row {line} has a different number of columns")
            rows.append({k: v.strip() for k, v in raw.items()})
        return headers, rows
    except csv.Error as error:
        raise ApiError(400, f"Invalid CSV: {error}") from error


async def normalize_properties(conn, object_type: str, props: dict) -> dict:
    props = dict(props)
    # Only repair formats already covered by migration's measured normalizers.
    for key in ("amount", "price", "quantity"):
        if key in props and props[key] not in (None, ""):
            value = str(props[key])
            if key == "amount":
                amount, currency, monthly = normal.parse_amount(value)
                if monthly:
                    raise ApiError(400, "Specify the annual renewal amount explicitly")
                if currency and object_type == "deals":
                    props.setdefault("deal_currency_code", currency)
            else:
                amount = normal.plain_number(value)
            if amount is None:
                raise ApiError(400, f"Invalid {key}: {value}")
            props[key] = normal.num_str(amount)
    for key in ("commerciale", "assegnatario"):
        if props.get(key):
            value = str(props[key]).strip()
            rows = await read.list_users(conn, value)
            exact = [r for r in rows if value.lower() in (r["email"].lower(), r["legacy_id"].lower(), r["name"].lower())]
            rows = exact or rows
            if len(rows) != 1:
                raise ApiError(400, f"Assignee '{value}' is missing or ambiguous; ask the user")
            if not rows[0]["active"] or not rows[0]["email"]:
                raise ApiError(400, f"Assignee '{value}' is inactive or has no email")
            props[key] = rows[0]["email"]
    if props.get("email"):
        email = normal.parse_email(str(props["email"]))
        if email is None:
            raise ApiError(400, "Invalid contact email")
        props["email"] = email
    if props.get("domain"):
        props["domain"] = store.bare_domain(str(props["domain"]))
    if props.get("hs_sku"):
        sku = normal.parse_sku(str(props["hs_sku"]))
        if sku is None:
            raise ApiError(400, "Invalid product SKU")
        props["hs_sku"] = sku
    if props.get("lifecyclestage"):
        stages = {"lead": "lead", "prospect": "opportunity", "cliente": "customer", "ex cliente": "other"}
        props["lifecyclestage"] = stages.get(normal.fold(str(props["lifecyclestage"])), props["lifecyclestage"])
    if "hs_discount_percentage" in props:
        props["hs_discount_percentage"] = normal.num_str(normal.parse_discount(str(props["hs_discount_percentage"])))
    for key in ("closedate", "createdate", "closed_date", "hs_timestamp"):
        value = props.get(key)
        if value and not str(value).isdigit():
            try:
                props[key] = store.norm_datetime(str(value))
            except ApiError:
                parsed = normal.parse_local(str(value))
                if parsed is None:
                    raise
                props[key] = store.iso(parsed)
    if object_type == "deals":
        if props.get("deal_currency_code"):
            currency = normal.currency_of(str(props["deal_currency_code"]))
            if currency:
                props["deal_currency_code"] = currency
        if props.get("pipeline"):
            pipeline = await conn.fetchval("SELECT id FROM pipelines WHERE object_type='deals' AND NOT archived "
                                           "AND (id=$1 OR lower(label)=lower($1))", str(props["pipeline"]).strip())
            if pipeline is None:
                raise ApiError(400, "Unknown deal pipeline")
            props["pipeline"] = pipeline
    stage_key = "dealstage" if object_type == "deals" else "hs_pipeline_stage" if object_type == "tickets" else None
    if stage_key and props.get(stage_key):
        stage = str(props[stage_key]).strip()
        if object_type == "deals":
            parsed = normal.parse_stage(stage)
            if parsed:
                family, code = parsed
                if family == "vendite":
                    stage = {"1": "appointmentscheduled", "2": "qualifiedtobuy", "3": "presentationscheduled",
                             "4": "decisionmakerboughtin", "5": "contractsent", "6": "closedwon", "7": "closedlost"}.get(str(code), stage)
                else:
                    stage = {1: "Da rinnovare", 2: "In trattativa", 3: "Rinnovato", 4: "Non rinnovato"}.get(code, stage)
        pipe_key = "pipeline" if object_type == "deals" else "hs_pipeline"
        candidates = await conn.fetch(
            "SELECT s.id,s.pipeline_id FROM pipeline_stages s JOIN pipelines p "
            "ON p.object_type=s.object_type AND p.id=s.pipeline_id WHERE s.object_type=$1 AND NOT s.archived AND NOT p.archived "
            "AND (s.id=$2 OR lower(s.label)=lower($2)) AND ($3::text IS NULL OR s.pipeline_id=$3)",
            object_type, stage, props.get(pipe_key))
        if len(candidates) != 1:
            raise ApiError(400, "Pipeline stage is missing or ambiguous; read pipeline metadata")
        props[stage_key] = candidates[0]["id"]
        props[pipe_key] = candidates[0]["pipeline_id"]
    protected = {"hs_object_id", "hs_lastmodifieddate", "lastmodifieddate", "fatturato_2025", "classe_cliente"}
    if protected & props.keys():
        raise ApiError(400, "System and calculated properties cannot be patched by the assistant")
    return props


async def apply(conn, object_type: str, content: str, mode: str, id_property: str, effective_now) -> list[dict]:
    object_type = store.resolve_type(object_type)
    if mode not in ("create", "update", "upsert"):
        raise ApiError(400, "CSV mode must be create, update or upsert")
    if id_property not in ("id", "id_legacy", "email", "hs_sku"):
        raise ApiError(400, "Unsupported CSV identity property")
    _, rows = parse(content)
    results = []
    async with conn.transaction():
        for number, raw in enumerate(rows, 2):
            if raw.get("cancellato") and normal.is_deleted(raw["cancellato"]):
                continue
            props, associations = {}, []
            for column, value in raw.items():
                if column in ("cancellato", "ultima_modifica"):
                    continue
                mapped = ALIASES.get(object_type, {}).get(column, column)
                if column in REFERENCES and mapped != "id_legacy":
                    if value:
                        target = await store.get(conn, REFERENCES[column], value, "id_legacy")
                        associations.append((REFERENCES[column], target["id"], None))
                else:
                    props[mapped] = value
            props = await normalize_properties(conn, object_type, props)
            identifier = props.pop("id", None) if id_property == "id" else props.get(id_property)
            if mode != "create" and not identifier:
                raise ApiError(400, f"CSV row {number} requires {id_property}")
            current = await store.fetch_row(conn, object_type, identifier, id_property) if mode != "create" else None
            if mode == "update" and current is None:
                raise ApiError(404, f"CSV row {number}: record not found", "OBJECT_NOT_FOUND")
            if current:
                row = await store.update(conn, object_type, current["id"], props, effective_now=effective_now)
                for target_type, target_id, types in associations:
                    await store.associate(conn, object_type, row["id"], target_type, target_id, types)
            else:
                row = await store.create(conn, object_type, props, associations or None, effective_now=effective_now)
            results.append(await read.get_record(conn, object_type, row["id"]))
    return results
