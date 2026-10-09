"""Brambilla's reference model: the ideal Sinergia process, as code.

Two sources, each rule tagged with where it comes from:
  [RICHIESTE Rn]  stated by Brambilla in legacy/RICHIESTE.md
  [DATA]          a Sinergia habit that holds on 100% of the export (an invariant);
                  a record that breaks it is an anomaly.

Pure Python, no I/O: the migration can import the same normalisers.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

EXPORT_DATE = datetime(2026, 12, 1)          # [RICHIESTE intro] export of 1 Dec 2026

# ---------------------------------------------------------------- flags
_DELETED = {"s", "si", "sì", "1", "y", "yes", "true", "x"}
_ACTIVE_NO = {"n", "no", "0", "false"}


def is_deleted(v: str) -> bool:
    """[RICHIESTE all] deleted rows are not migrated. 9 spellings in the export."""
    return (v or "").strip().lower() in _DELETED


def is_active_user(v: str) -> bool:
    return (v or "").strip().lower() not in _ACTIVE_NO


# ---------------------------------------------------------------- text
_MOJIBAKE = re.compile("[ÃÂ][\u0080-ÿ‘-›€ŒœŠšŽžŸƒˆ˜]|â€")


def fix_text(v: str) -> str:
    """Trim [RICHIESTE all] and repair UTF-8-read-as-CP1252 ('SocietÃ\xa0' -> 'Società')."""
    if v is None:
        return ""
    s = v
    if _MOJIBAKE.search(s):
        for enc in ("cp1252", "latin-1"):
            try:
                s = s.encode(enc).decode("utf-8")
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
    return s.strip()


def has_mojibake(v: str) -> bool:
    return bool(v and _MOJIBAKE.search(v))


# ---------------------------------------------------------------- dates
_DATE_FORMATS = (
    "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
    "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%y", "%d.%m.%Y", "%Y-%m-%dT%H:%M:%S",
)


def parse_dt(v: str) -> datetime | None:
    s = (v or "").strip()
    if not s:
        return None
    if re.fullmatch(r"\d{5}", s):                      # Excel serial (e.g. 43669)
        return datetime(1899, 12, 30) + timedelta(days=int(s))
    for f in _DATE_FORMATS:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    # d/m/yyyy with single digits
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return datetime(int(m[3]), int(m[2]), int(m[1]))
    return None


# ---------------------------------------------------------------- numbers
def parse_number(v: str) -> Decimal | None:
    """Italian or English notation, currency symbols, trailing minus ('8146,18-')."""
    s = (v or "").strip()
    if not s:
        return None
    neg = False
    s = re.sub(r"(?i)\b(eur|euro|usd|gbp)\b|[€$£]", "", s)
    s = re.sub(r"(?i)al mese|/\s*mese|mensil\w*", "", s).strip()
    mult = 1
    m = re.search(r"(?i)\s*(k|mila|mln|milioni|milione|mio|m)\s*$", s)       # '206,5k', '6.5mila', '1,2 mln'
    if m and re.search(r"\d", s[:m.start()]):
        mult = 1000 if m[1].lower() in ("k", "mila") else 1_000_000
        s = s[:m.start()].strip()
    if re.fullmatch(r"\(.*\)", s):                      # accounting negative '(20020,40)'
        neg, s = True, s[1:-1].strip()
    if s.endswith("-"):
        neg, s = True, s[:-1]
    if s.startswith("-"):
        neg, s = True, s[1:]
    s = s.replace(" ", "").replace(" ", "")
    if not s:
        return None
    if "," in s and "." in s:
        dec = "," if s.rfind(",") > s.rfind(".") else "."
    elif "," in s:
        # '1,151,12' impossible; '2,496' ambiguous -> comma decimal unless 3 digits groups repeat
        dec = "," if not re.fullmatch(r"\d{1,3}(,\d{3}){2,}", s) else None
    elif "." in s:
        dec = "." if not re.fullmatch(r"\d{1,3}(\.\d{3}){2,}", s) else None
    else:
        dec = None
    if dec == ",":
        s = s.replace(".", "").replace(",", ".")
    elif dec == ".":
        s = s.replace(",", "")
    else:
        s = s.replace(",", "").replace(".", "")
    try:
        d = Decimal(s) * mult
    except InvalidOperation:
        return None
    return -d if neg else d


def is_shorthand(v: str) -> bool:
    return bool(re.search(r"(?i)\d\s*(k|mila|mln|milioni|milione|mio)\s*$", (v or "").strip()))


def is_monthly(v: str) -> bool:
    return bool(re.search(r"(?i)al mese|/\s*mese|mensil", v or ""))


def money(d: Decimal | None) -> str:
    return "" if d is None else str(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------- currency  [RICHIESTE R3, R8]
FX_TO_EUR = {"EUR": Decimal("1"), "USD": Decimal("0.92"), "GBP": Decimal("1.17")}


def currency(valuta: str, importo: str) -> str | None:
    v = (valuta or "").strip().lower()
    a = (importo or "")
    if v in ("$", "usd") or re.search(r"\$|\busd\b", a, re.I):
        return "USD"
    if v in ("£", "gbp") or re.search(r"£|\bgbp\b", a, re.I):
        return "GBP"
    return "EUR"


def currency_conflict(valuta: str, importo: str) -> bool:
    """valuta says one thing, the symbol in importo another."""
    v = (valuta or "").strip().lower()
    vv = {"$": "USD", "usd": "USD", "£": "GBP", "gbp": "GBP", "€": "EUR", "eur": "EUR", "euro": "EUR"}.get(v)
    a = importo or ""
    av = "USD" if re.search(r"\$|\busd\b", a, re.I) else "GBP" if re.search(r"£|\bgbp\b", a, re.I) else \
        "EUR" if re.search(r"€|\beur\b", a, re.I) else None
    return bool(vv and av and vv != av)


# ---------------------------------------------------------------- pipelines & stages  [RICHIESTE appendix]
SALES = {"V01": ("appointmentscheduled", "Contatto"), "V02": ("qualifiedtobuy", "Qualifica"),
         "V03": ("presentationscheduled", "Presentazione"), "V04": ("decisionmakerboughtin", "Decisione"),
         "V05": ("contractsent", "Contratto"), "V06": ("closedwon", "Vinta"), "V07": ("closedlost", "Persa")}
RENEW = {"R1": "Da rinnovare", "R2": "In trattativa", "R3": "Rinnovato", "R4": "Non rinnovato"}
WON = {"V06", "R3"}
LOST = {"V07", "R4"}
CLOSED = WON | LOST
ORDER = {"V01": 1, "V02": 2, "V03": 3, "V04": 4, "V05": 5, "V06": 6, "V07": 6,
         "R1": 1, "R2": 2, "R3": 3, "R4": 3}
_STAGE_NAMES = {"contatto": "V01", "qualifica": "V02", "presentazione": "V03", "decisione": "V04",
                "contratto": "V05", "vinta": "V06", "persa": "V07", "da rinnovare": "R1",
                "in trattativa": "R2", "rinnovato": "R3", "non rinnovato": "R4"}
# the form Sinergia itself writes most often, reused in the amended export
STAGE_LABEL_OUT = {**{k: f"{k[1:]} - {v[1]}" for k, v in SALES.items()},
                   **{k: f"{k} - {v}" for k, v in RENEW.items()}}


def stage(v: str) -> str | None:
    s = (v or "").strip().lower()
    if not s:
        return None
    m = re.match(r"^(0[1-7])\b", s)
    if m:
        return "V" + m[1]
    m = re.match(r"^r([1-4])\b", s)
    if m:
        return "R" + m[1]
    return _STAGE_NAMES.get(s)


def pipeline(v: str, stage_code: str | None) -> str:
    """[RICHIESTE appendix] no pipeline = Vendite. [DATA] stage family always matches."""
    p = (v or "").strip().lower()
    if p.startswith("rinn"):
        return "Rinnovi"
    if p.startswith("vend"):
        return "Vendite"
    return "Rinnovi" if (stage_code or "").startswith("R") else "Vendite"


# Sinergia invariants on storico_fasi [DATA, 100% of 35,020 deals]
INVARIANTS = {
    "created_at_first_stage": "every deal's first history row has no previous stage and lands in 01 / R1",
    "chain_continuous": "each row's previous stage equals the previous row's new stage",
    "no_backward": "stages never move backwards",
    "no_reopen": "nothing moves after a closing stage (Vinta, Persa, Rinnovato, Non rinnovato)",
    "gap_2_89_days": "consecutive stage changes are 2-89 days apart",
    "family_matches_pipeline": "Vendite deals only use 01-07, Rinnovi only R1-R4",
    "closedate_is_closing_day": "data_chiusura of a closed deal = date of its closing history row",
    "history_before_last_modified": "no history row is later than the deal's ultima_modifica",
}
GAP_MIN_DAYS, GAP_MAX_DAYS = 2, 89

# ---------------------------------------------------------------- deals: kinds of document
_CREDIT = re.compile(r"(?i)^\s*(storno\b|nc\b|n\.c\.|nota di credito)")


def is_credit_note(titolo: str) -> bool:
    """[RICHIESTE R8] 'tolto quello che abbiamo stornato': reversals / credit notes."""
    return bool(_CREDIT.search(titolo or ""))


# ---------------------------------------------------------------- contacts  [RICHIESTE R2, appendix]
LIFECYCLE = {"lead": "lead", "prospect": "opportunity", "cliente": "customer",
             "ex cliente": "other", "ex-cliente": "other", "excliente": "other"}
LIFECYCLE_OUT = {"lead": "Lead", "opportunity": "Prospect", "customer": "Cliente", "other": "Ex cliente"}
_EMAIL = re.compile(r"^[a-z0-9._%+'-]+@[a-z0-9.-]+\.[a-z]{2,}$")


def lifecycle(v: str) -> str | None:
    return LIFECYCLE.get(re.sub(r"\s+", " ", (v or "").strip().lower()))


def email(v: str) -> str | None:
    """[RICHIESTE R2] a field without a valid email is an absent email. Obvious typos are repaired first
    ('nome(at)dominio.it', 'nome @dominio.it'), same as the CRM's migration."""
    s = (v or "").strip().lower()
    s = re.sub(r"\s*\(\s*at\s*\)\s*|\s*\[\s*at\s*\]\s*", "@", s)
    s = re.sub(r"\s*@\s*", "@", s).strip(" .;,<>\"'")
    return s if _EMAIL.match(s) else None


# ---------------------------------------------------------------- companies  [RICHIESTE R1, R7]
def domain(v: str) -> str | None:
    s = (v or "").strip().lower()
    if not s:
        return None
    s = re.sub(r"^[a-z]+://", "", s)
    s = s.split("/")[0].split("?")[0].split(":")[0]
    s = re.sub(r"^www\d*\.", "", s)
    return s if re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", s) else None


_PIVA = re.compile(r"(?i)(?:p\.?\s*iva|partita\s*iva)\W*((?:it\s?)?[\d ]{11,14})")


def piva_from_note(note: str) -> str | None:
    m = _PIVA.search(note or "")
    if not m:
        return None
    d = re.sub(r"\D", "", m[1])
    return d if len(d) == 11 else None


# ---------------------------------------------------------------- products  [RICHIESTE R4]
def sku(v: str) -> str | None:
    d = re.sub(r"\D", "", v or "")
    return f"BF-{d.zfill(5)}" if d else None


def quantity(v: str) -> Decimal | None:
    m = re.match(r"\s*([\d.,]+)", v or "")
    return parse_number(m[1]) if m else None


def discount_pct(v: str) -> Decimal:
    """'0,25' is a fraction (25%), '25', '25%', '25,0' are percent. Absent = 0."""
    s = (v or "").strip()
    if not s:
        return Decimal("0")
    d = parse_number(s.replace("%", "")) or Decimal("0")
    if "%" not in s and Decimal("0") < d < Decimal("1"):
        d = d * 100
    return d.quantize(Decimal("0.01"))


def line_total(q: Decimal, price: Decimal, disc: Decimal) -> Decimal:
    return (q * price * (1 - disc / 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------- tickets  [RICHIESTE R5, appendix]
TICKET_STAGE = {"nuovo": "Aperto", "aperto": "Aperto", "in lavorazione": "In lavorazione",
                "lavorazione": "In lavorazione", "in attesa cliente": "In attesa del cliente",
                "attesa cliente": "In attesa del cliente", "in attesa": "In attesa del cliente",
                "chiuso": "Chiuso", "risolto": "Chiuso"}
TICKET_CLOSED = {"Chiuso"}
PRIORITY = {"bassa": "LOW", "1 - bassa": "LOW", "media": "MEDIUM", "2 - media": "MEDIUM", "normale": "MEDIUM",
            "alta": "HIGH", "3 - alta": "HIGH", "urgente": "URGENT", "4 - urgente": "URGENT", "urgente!!": "URGENT"}


def ticket_stage(v: str) -> str | None:
    return TICKET_STAGE.get((v or "").strip().lower())


def priority(v: str) -> str | None:
    return PRIORITY.get((v or "").strip().lower())


_SENDER = re.compile(r"(?i)\b(?:da|from|mittente)\s*:\s*<?([^\s<>;,]+@[^\s<>;,]+)")


def ticket_sender(desc: str) -> str | None:
    m = _SENDER.search(desc or "")
    return email(m[1]) if m else None


# ---------------------------------------------------------------- activities  [RICHIESTE R6]
ACTIVITY = {"nota": "notes", "appunto": "notes", "chiamata": "calls", "telefonata": "calls", "tel.": "calls",
            "e-mail": "emails", "email": "emails", "mail": "emails",
            "incontro": "meetings", "meeting": "meetings", "riunione": "meetings", "visita": "meetings"}


def activity_type(v: str) -> str | None:
    return ACTIVITY.get((v or "").strip().lower())


# ---------------------------------------------------------------- owners  [RICHIESTE R3]
OWNER_POLICIES = ("empty", "manager")


def split_ids(v: str) -> list[str]:
    return [x for x in re.split(r"[;,\s]+", (v or "").strip()) if x]
