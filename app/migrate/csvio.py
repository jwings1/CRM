"""Read the Sinergia export: zip of `;`-separated CSVs in Windows-1252."""
from __future__ import annotations

import csv
import io
import posixpath
import zipfile

FILES = ("aziende", "contatti", "opportunita", "righe_offerta", "listino", "ticket", "attivita", "utenti",
         "storico_fasi")


def _decode(raw: bytes) -> str:
    try:
        text = raw.decode("cp1252")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    return text.lstrip("﻿")


def read_export(zip_bytes: bytes) -> dict[str, list[dict[str, str]]]:
    """Return {'aziende': [row, ...], ...}. Keys are lowercase file stems; folder prefixes ignored.
    Values are raw strings (NOT stripped: normalizers decide)."""
    out: dict[str, list[dict[str, str]]] = {}
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".csv") or posixpath.basename(name).startswith("."):
                continue
            stem = posixpath.basename(name)[:-4].lower()
            reader = csv.DictReader(io.StringIO(_decode(zf.read(name)), newline=""), delimiter=";")
            reader.fieldnames = [f.strip().lower() for f in reader.fieldnames or []]
            out[stem] = [{k: (v if v is not None else "") for k, v in r.items() if k is not None} for r in reader]
    return out
