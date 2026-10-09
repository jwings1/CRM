import os

API_VERSION = "2026-09"

CRM_TOKEN = os.environ.get("CRM_TOKEN", "")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/crm")
DB_POOL_MIN = int(os.environ.get("DB_POOL_MIN", "2"))
DB_POOL_MAX = int(os.environ.get("DB_POOL_MAX", "20"))

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-6-luna")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# UI routes advertised in /health (module -> route). Pages are served by app/ui.
UI_ROUTES = {
    "companies": "/companies",
    "contacts": "/contacts",
    "deals": "/deals",
    "tickets": "/tickets",
    "dormant": "/dormant",
}
