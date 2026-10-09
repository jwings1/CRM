"""Reviewed Markdown -> production Postgres. Run with the intended DATABASE_URL.

python -m app.agent.kb_cli import DIRECTORY
python -m app.agent.kb_cli link DOC_ID OBJECT_ID --revision N [--relation mentions]
python -m app.agent.kb_cli archive DOC_ID --revision N
python -m app.agent.kb_cli list
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from .. import db, store
from ..errors import ApiError
from .kb import list_documents, load_documents


async def run(args) -> None:
    await db.connect()
    try:
        async with db.pool.acquire() as conn:
            if args.command == "list":
                print(json.dumps(await list_documents(conn), ensure_ascii=False, indent=2))
                return
            async with conn.transaction():
                if args.command == "import":
                    documents = load_documents(Path(args.directory))
                    result = []
                    for document in documents:
                        observed = await conn.fetchval("SELECT revision FROM kb_documents WHERE doc_id=$1", document["doc_id"])
                        expected = document.pop("expected_revision", observed or 0)
                        row = await store.publish_kb_document(conn, document, expected_revision=expected)
                        result.append({"doc_id": row["doc_id"], "revision": row["revision"]})
                else:
                    options = {"expected_revision": args.revision}
                    if args.command == "archive":
                        options["archived"] = True
                    else:
                        options["link"] = {"object_id": args.object_id, "relation": args.relation}
                    row = await store.change_kb_document(conn, args.doc_id, **options)
                    result = [{"doc_id": row["doc_id"], "revision": row["revision"]}]
            print(json.dumps(result, ensure_ascii=False))
    finally:
        await db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    commands.add_parser("import").add_argument("directory")
    for command in ("link", "archive"):
        sub = commands.add_parser(command)
        sub.add_argument("doc_id")
        if command == "link":
            sub.add_argument("object_id", type=int)
            sub.add_argument("--relation", default="mentions")
        sub.add_argument("--revision", type=int, required=True)
    try:
        asyncio.run(run(parser.parse_args()))
    except ApiError as error:
        parser.exit(1, f"{error.category}: {error.message}\n")


if __name__ == "__main__":
    main()
