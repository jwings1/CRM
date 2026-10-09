"""Whole-document retrieval from the production CRM Postgres database."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .. import store
from ..errors import ApiError

SEED_DIR = Path(__file__).parent / "data" / "kb"
_SYNONYMS = {"perdo": "persa", "perso": "persa", "vinto": "vinta", "ricavi": "fatturato",
             "piva": "partita iva", "customer": "cliente", "revenue": "fatturato",
             "price": "prezzo", "discount": "sconto", "dormant": "dormienti"}


def load_documents(directory: Path = SEED_DIR) -> list[dict]:
    directory = directory.resolve()
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    documents, seen = [], set()
    for entry in manifest["documents"]:
        entry = dict(entry)
        doc_id = str(entry["doc_id"]).upper()
        if doc_id in seen:
            raise ApiError(400, f"Duplicate document ID {doc_id}")
        seen.add(doc_id)
        path = (directory / entry.pop("file")).resolve()
        if not path.is_relative_to(directory) or path.suffix != ".md":
            raise ApiError(400, "Document files must be Markdown inside the import directory")
        entry["doc_id"] = doc_id
        entry["content"] = path.read_text(encoding="utf-8")
        documents.append(entry)
    return documents


async def seed_documents(conn) -> None:
    for document in load_documents():
        await store.publish_kb_document(conn, document, only_if_missing=True)


def document_result(row) -> dict:
    return {key: row[key] for key in ("doc_id", "title", "category", "content", "source", "metadata", "revision", "content_hash")}


async def list_documents(conn) -> list[dict]:
    return [dict(row) for row in await conn.fetch(
        "SELECT doc_id,title,category,source,metadata,revision FROM kb_documents WHERE NOT archived ORDER BY doc_id")]


async def get_document(conn, doc_id: str, revision: int | None = None) -> dict:
    if revision is None:
        row = await conn.fetchrow("SELECT * FROM kb_documents WHERE doc_id=$1 AND NOT archived", doc_id.upper())
    else:
        row = await conn.fetchrow(
            "SELECT v.* FROM kb_document_versions v JOIN kb_documents d USING (doc_id) "
            "WHERE v.doc_id=$1 AND v.revision=$2 AND NOT v.archived AND NOT d.archived", doc_id.upper(), revision)
    if row is None:
        raise ApiError(404, f"Knowledge document {doc_id} not found", "OBJECT_NOT_FOUND")
    return document_result(row)


async def search_documents(conn, query: str, max_results: int = 4) -> list[dict]:
    limit = max(1, min(int(max_results), 4))
    query = str(query).strip()
    if not query:
        return []
    identifiers = re.findall(r"\b(?:BKB-[A-Z0-9_.-]+|DOC-\d+|R\d{1,2})\b", query.upper())
    ids = [f"BKB-R{int(v[1:]):02d}" if re.fullmatch(r"R\d+", v) else v for v in identifiers]
    exact = await conn.fetch("SELECT * FROM kb_documents WHERE doc_id=ANY($1::text[]) AND NOT archived ORDER BY doc_id LIMIT $2",
                             ids, limit) if ids else []
    if exact:
        return [document_result(row) for row in exact]
    # A SKU is an exact entity discriminator, not an approximate text token.
    skus = re.findall(r"\bBF[- .]?(\d{1,5})\b", query, re.I)
    if skus:
        normalized = [f"BF-{int(s):05d}" for s in skus]
        rows = await conn.fetch(
            "SELECT DISTINCT d.* FROM kb_documents d LEFT JOIN kb_document_links l USING (doc_id) "
            "LEFT JOIN objects o ON o.id=l.object_id AND NOT o.archived "
            "WHERE NOT d.archived AND (d.metadata->'skus' ?| $1::text[] OR "
            "(o.object_type='products' AND o.properties->>'hs_sku'=ANY($1::text[]))) ORDER BY d.doc_id LIMIT $2",
            normalized, limit)
        return [document_result(row) for row in rows]
    words = re.findall(r"[\w]+", query.lower())
    normalized = " ".join(_SYNONYMS.get(word, word) for word in words)
    rows = await conn.fetch(
        "SELECT d.* FROM kb_documents d, plainto_tsquery('italian', $1) q "
        "WHERE NOT d.archived AND d.search_vector @@ q "
        "ORDER BY ts_rank_cd(d.search_vector,q) DESC,d.doc_id LIMIT $2", normalized, limit)
    return [document_result(row) for row in rows]


async def related_knowledge(conn, object_type: str, object_id: int, depth: int = 2) -> dict:
    await store.get(conn, store.resolve_type(object_type), object_id)
    # Recursive UNION deduplicates labeled/primary variants and cycles. Cap depth.
    rows = await conn.fetch(
        "WITH RECURSIVE neighborhood(id,depth) AS (SELECT $1::bigint,0 UNION "
        "SELECT a.to_id,n.depth+1 FROM neighborhood n JOIN associations a ON a.from_id=n.id "
        "JOIN objects o ON o.id=a.to_id AND NOT o.archived WHERE n.depth<$2) "
        "SELECT DISTINCT o.* FROM neighborhood n JOIN objects o USING (id) WHERE NOT o.archived ORDER BY o.id LIMIT 201",
        object_id, max(0, min(int(depth), 2)))
    truncated = len(rows) > 200
    nodes = rows[:200]
    ids = [row["id"] for row in nodes]
    types = sorted({row["object_type"] for row in nodes})
    edges = await conn.fetch(
        "SELECT DISTINCT from_id,to_id,from_type,to_type FROM associations "
        "WHERE from_id=ANY($1::bigint[]) AND to_id=ANY($1::bigint[]) AND from_id<to_id ORDER BY from_id,to_id", ids)
    docs = await conn.fetch(
        "SELECT DISTINCT d.* FROM kb_documents d LEFT JOIN kb_document_links l USING (doc_id) "
        "WHERE NOT d.archived AND (l.object_id=ANY($1::bigint[]) OR d.metadata->'object_types' ?| $2::text[]) "
        "ORDER BY d.doc_id LIMIT 20", ids, types)
    links = await conn.fetch(
        "SELECT l.doc_id,l.object_id,l.relation FROM kb_document_links l JOIN kb_documents d USING (doc_id) "
        "WHERE l.object_id=ANY($1::bigint[]) AND NOT d.archived ORDER BY l.doc_id,l.object_id", ids)
    return {"records": [{"id": str(r["id"]), "object_type": r["object_type"],
                         "properties": r["properties"], "updated_at": store.iso(r["updated_at"])} for r in nodes],
            "edges": [dict(r) for r in edges], "document_links": [dict(r) for r in links],
            "documents": [document_result(r) for r in docs], "truncated": truncated}
