"""Parsers for the shapes Sinergia data is written in. Pure functions, no I/O.
Every rule here is backed by a count in NOTES.md."""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache
from datetime import date, datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from zoneinfo import ZoneInfo

ROME = ZoneInfo("Europe/Rome")
CENT = Decimal("0.01")

# ---------------------------------------------------------------- generic

_DELETED = {"S", "SI", "SÌ", "1", "Y", "YES", "TRUE", "X"}


def is_deleted(v: str | None) -> bool:
    return (v or "").strip().upper() in _DELETED


_MOJIBAKE = re.compile("[ÃÂ][\u0080-\u00ff\u2018-\u203a\u20ac\u0152\u0153\u0160\u0161\u017d\u017e\u0178\u0192\u02c6\u02dc]|â€")


def clean(v: str | None) -> str:
    """Text as people wrote it, without extra spaces around. Repairs UTF-8 text that Sinergia stored
    as Windows-1252 ('SocietÃ\xa0' -> 'Società', 'NiccolÃ²' -> 'Niccolò'): ~4,200 rows in the export."""
    if not v:
        return ""
    if _MOJIBAKE.search(v):
        for enc in ("cp1252", "latin-1"):
            try:
                v = v.encode(enc).decode("utf-8")
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
    return v.strip()


def is_active(v: str | None) -> bool:
    return (v or "").strip().upper() in {"S", "SI", "SÌ", "1", "Y", "YES", "TRUE"}


@lru_cache(maxsize=8192)
def fold(s: str) -> str:
    """lowercase, no accents, only letters/digits/spaces."""
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


# ---------------------------------------------------------------- dates

_EXCEL_EPOCH = date(1899, 12, 30)


_RX_DMY = re.compile(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4}|\d{2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?$")
_RX_YMD = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?$")


def parse_local(s: str | None) -> datetime | None:
    """Sinergia local time (Europe/Rome) -> aware datetime. Formats seen: dd/mm/yyyy[ HH:MM[:SS]],
    yyyy-mm-dd[ HH:MM:SS], dd-mm-yyyy, dd.mm.yy, d/m/yyyy, Excel serial (5 digits)."""
    s = (s or "").strip()
    if not s:
        return None
    if len(s) == 5 and s.isdigit():  # Excel serial date
        return datetime.combine(_EXCEL_EPOCH + timedelta(days=int(s)), datetime.min.time(), ROME)
    m = _RX_YMD.match(s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = _RX_DMY.match(s)
        if not m:
            return None
        d, mo, y = int(m.group(1)), int(m.group(2)), m.group(3)
        y = int(y) + 2000 if len(y) == 2 else int(y)
    try:
        return datetime(y, mo, d, int(m.group(4) or 0), int(m.group(5) or 0), int(m.group(6) or 0), tzinfo=ROME)
    except ValueError:
        return None


def parse_day(s: str | None) -> date | None:
    dt = parse_local(s)
    return dt.date() if dt else None


def iso_utc(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def iso_day(d: date | None) -> str | None:
    """Date-only values (closedate): midnight UTC of that calendar day, like HubSpot date inputs."""
    return f"{d.isoformat()}T00:00:00.000Z" if d else None


# ---------------------------------------------------------------- numbers / money

def to_decimal(num: str, has_multiplier: bool = False) -> Decimal | None:
    """'1.247.204,29' '24,376.08' '1027956.14' '488210,35' '5.000' '6.5' -> Decimal.
    Rule: with both separators the last one is the decimal mark; with one kind, repeated = thousands,
    single followed by exactly 3 digits = thousands (unless a k/mila/mln multiplier follows), else decimal."""
    s = re.sub(r"[^\d.,]", "", num or "")
    if not s or not re.search(r"\d", s):
        return None
    if "." in s and "," in s:
        dec = "." if s.rfind(".") > s.rfind(",") else ","
        s = s.replace("," if dec == "." else ".", "").replace(dec, ".")
    elif "." in s or "," in s:
        sep = "." if "." in s else ","
        parts = s.split(sep)
        if len(parts) > 2 or (len(parts[-1]) == 3 and not has_multiplier):
            s = s.replace(sep, "")
        else:
            s = s.replace(sep, ".")
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


@lru_cache(maxsize=8192)
def currency_of(*texts: str) -> str | None:
    t = " ".join(texts).upper()
    if "$" in t or "USD" in t or "DOLL" in t:
        return "USD"
    if "£" in t or "GBP" in t or "STERL" in t:
        return "GBP"
    if "€" in t or "EUR" in t:
        return "EUR"
    return None


def parse_amount(raw: str | None) -> tuple[Decimal | None, str | None, bool]:
    """Deal amount -> (value, currency-in-text, monthly). Handles '€ -5.131,24', '(20020,40)',
    'EUR 223.370,86', '€206,5k', '6.5mila', '1,2 mln', '51.315,91 mensili', '500,59 /mese'."""
    s = clean(raw)
    if not s:
        return None, None, False
    low = s.lower()
    mult = Decimal(1)
    if re.search(r"mln\b|milion|\d\s*mio\b", low):          # '1.4mln' has no word boundary before 'mln
        mult = Decimal(1_000_000)
    elif re.search(r"\d\s*k\b|\bk\b|mila", low):
        mult = Decimal(1000)
    m = re.search(r"\d[\d.,]*", s)
    if not m:
        return None, currency_of(s), False
    v = to_decimal(m.group(0), has_multiplier=mult != 1)
    if v is None:
        return None, currency_of(s), False
    v *= mult
    neg = "-" in s[: m.start()] or (s.startswith("(") and s.endswith(")")) or s.endswith("-")
    if neg:
        v = -v
    monthly = bool(re.search(r"mese|mensil|monthly", low))
    return v, currency_of(s), monthly


def money(v: Decimal | None) -> str | None:
    if v is None:
        return None
    return str(v.quantize(CENT, rounding=ROUND_HALF_UP))


def plain_number(raw: str | None) -> Decimal | None:
    """quantity '2,5 m' '10 pz', price '€ 1.151,12', list price '2.82'."""
    s = clean(raw)
    m = re.search(r"-?\d[\d.,]*", s)
    return to_decimal(m.group(0)) if m else None


def parse_discount(raw: str | None) -> Decimal:
    """'15%' '15 %' '15' '15,0' '0,15' (fraction) -> percent. Empty -> 0."""
    s = clean(raw)
    if not s:
        return Decimal(0)
    m = re.search(r"\d[\d.,]*", s)
    if not m:
        return Decimal(0)
    s2 = m.group(0).replace(",", ".")
    try:
        v = Decimal(s2)
    except InvalidOperation:
        return Decimal(0)
    if "%" not in s and 0 < v < 1:
        v *= 100  # fractions: 0,25 = 25%
    return v


def num_str(v: Decimal | None) -> str | None:
    if v is None:
        return None
    v = v.normalize()
    s = format(v, "f")
    return s


# ---------------------------------------------------------------- identifiers

_EMAIL = re.compile(r"^[a-z0-9._%+'-]+@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$")


def parse_email(raw: str | None) -> str | None:
    """Valid email or None. Repairs '(at)' obfuscation and spaces around '@'."""
    s = clean(raw).lower()
    if not s:
        return None
    s = re.sub(r"\s*\(\s*at\s*\)\s*|\s*\[\s*at\s*\]\s*", "@", s)
    s = re.sub(r"\s*@\s*", "@", s)
    s = s.strip(" .;,<>\"'")
    return s if _EMAIL.match(s) else None


def parse_domain(raw: str | None) -> str | None:
    s = clean(raw).lower()
    if not s:
        return None
    s = re.sub(r"^[a-z]+://", "", s)
    s = s.split("/")[0].split("?")[0].split("#")[0].strip(".")
    if s.startswith("www."):
        s = s[4:]
    return s if re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", s) else None


_PIVA = re.compile(r"(?:p\.?\s*iva|partita\s*iva)\s*[:.]?\s*((?:it)?\s*[\d\s]{11,16})", re.I)


def parse_piva(note: str | None) -> str | None:
    m = _PIVA.search(note or "")
    if not m:
        return None
    digits = re.sub(r"\D", "", m.group(1))
    return digits[:11] if len(digits) >= 11 else None


def parse_sku(raw: str | None) -> str | None:
    """'BF38295' 'bf-38295' 'art. 38295' 'BF.3829' '38295' -> 'BF-38295' (5 digits, zero-padded)."""
    d = re.sub(r"\D", "", raw or "")
    return f"BF-{d.zfill(5)}" if d else None


# ---------------------------------------------------------------- enumerations

@lru_cache(maxsize=8192)
def lifecycle(raw: str | None) -> str | None:
    s = fold(raw).replace("-", " ")
    if s.startswith("ex"):
        return "other"
    if "client" in s:
        return "customer"
    if "prospect" in s:
        return "opportunity"
    if "lead" in s:
        return "lead"
    return None


_SALES = {"1": "appointmentscheduled", "2": "qualifiedtobuy", "3": "presentationscheduled", "4": "decisionmakerboughtin",
          "5": "contractsent", "6": "closedwon", "7": "closedlost"}
_SALES_WORDS = [("vint", "6"), ("pers", "7"), ("contatt", "1"), ("qualif", "2"), ("present", "3"),
                ("decis", "4"), ("contratt", "5")]
RINNOVI_LABELS = {1: "Da rinnovare", 2: "In trattativa", 3: "Rinnovato", 4: "Non rinnovato"}
_REN_WORDS = [("non rinnov", 4), ("rinnovato", 3), ("trattativa", 2), ("da rinnov", 1)]


@lru_cache(maxsize=8192)
def parse_stage(raw: str | None) -> tuple[str, str | int] | None:
    """-> ('vendite', '1'..'7') or ('rinnovi', 1..4)."""
    s = fold(raw)
    if not s:
        return None
    m = re.match(r"^r\s*([1-4])\b", s)
    if m:
        return "rinnovi", int(m.group(1))
    for w, n in _REN_WORDS:
        if w in s:
            return "rinnovi", n
    m = re.match(r"^0?([1-7])\b", s)
    if m:
        return "vendite", m.group(1)
    for w, n in _SALES_WORDS:
        if w in s:
            return "vendite", n
    return None


def sales_stage_id(code: str) -> str:
    return _SALES[code]


@lru_cache(maxsize=8192)
def parse_pipeline(raw: str | None) -> str | None:
    s = fold(raw)
    if s.startswith("rinnov"):
        return "rinnovi"
    if s.startswith("vend"):
        return "vendite"
    return None


@lru_cache(maxsize=8192)
def ticket_priority(raw: str | None) -> str | None:
    s = fold(raw)
    if not s:
        return None
    if "urgent" in s or s.startswith("4"):
        return "URGENT"
    if "alta" in s or "high" in s or s.startswith("3"):
        return "HIGH"
    if "media" in s or "normal" in s or "medium" in s or s.startswith("2"):
        return "MEDIUM"
    if "bassa" in s or "low" in s or s.startswith("1"):
        return "LOW"
    return None


@lru_cache(maxsize=8192)
def ticket_state(raw: str | None) -> str:
    """-> Assistenza stage label."""
    s = fold(raw)
    if "chius" in s or "risolt" in s or "closed" in s:
        return "Chiuso"
    if "attesa" in s:
        return "In attesa del cliente"
    if "lavoraz" in s or "corso" in s:
        return "In lavorazione"
    return "Aperto"


@lru_cache(maxsize=8192)
def activity_type(raw: str | None) -> str:
    s = fold(raw)
    if s.startswith(("chiam", "telef", "tel")) or "call" in s:
        return "calls"
    if "mail" in s:
        return "emails"
    if s.startswith(("incontr", "meet", "riun", "visit")):
        return "meetings"
    return "notes"  # NOTA, Appunto (= note), nota, unknown


BODY_PROP = {"notes": "hs_note_body", "calls": "hs_call_body", "emails": "hs_email_text", "meetings": "hs_meeting_body"}
