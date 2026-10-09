"""HubSpot defaults restored by POST /__reset: object types, default properties,
pipelines and association types. Brambilla-specific things are NOT here: the
migration creates them (see PLAN.md)."""

# canonical name -> (objectTypeId, singular)
OBJECT_TYPES: dict[str, tuple[str, str]] = {
    "contacts": ("0-1", "contact"),
    "companies": ("0-2", "company"),
    "deals": ("0-3", "deal"),
    "tickets": ("0-5", "ticket"),
    "products": ("0-7", "product"),
    "line_items": ("0-8", "line_item"),
    "quotes": ("0-14", "quote"),
    "tasks": ("0-27", "task"),
    "notes": ("0-46", "note"),
    "meetings": ("0-47", "meeting"),
    "calls": ("0-48", "call"),
    "emails": ("0-49", "email"),
}

_ALIASES: dict[str, str] = {}
for _name, (_tid, _sing) in OBJECT_TYPES.items():
    for _a in (_name, _tid, _sing, _name.replace("_", ""), _sing.replace("_", "")):
        _ALIASES[_a.lower()] = _name
_ALIASES["lineitems"] = "line_items"
_ALIASES["lineitem"] = "line_items"


def canon_type(name: str) -> str | None:
    return _ALIASES.get((name or "").lower())


def type_id(name: str) -> str:
    return OBJECT_TYPES[name][0]


# lastmodified property name differs for contacts
def lastmod_prop(otype: str) -> str:
    return "lastmodifieddate" if otype == "contacts" else "hs_lastmodifieddate"


# Properties returned when the request has no `properties` param.
DEFAULT_RETURNED: dict[str, list[str]] = {
    "contacts": ["createdate", "email", "firstname", "hs_object_id", "lastmodifieddate", "lastname"],
    "companies": ["createdate", "domain", "hs_lastmodifieddate", "hs_object_id", "name"],
    "deals": ["amount", "closedate", "createdate", "dealname", "dealstage", "hs_lastmodifieddate", "hs_object_id", "pipeline"],
    "tickets": ["content", "createdate", "hs_lastmodifieddate", "hs_object_id", "hs_pipeline", "hs_pipeline_stage", "hs_ticket_category", "hs_ticket_priority", "subject"],
    "products": ["createdate", "description", "hs_lastmodifieddate", "hs_object_id", "name", "price"],
    "line_items": ["createdate", "hs_lastmodifieddate", "hs_object_id", "hs_product_id", "name", "price", "quantity"],
    "quotes": ["hs_createdate", "hs_expiration_date", "hs_lastmodifieddate", "hs_object_id", "hs_title"],
    "tasks": ["hs_createdate", "hs_lastmodifieddate", "hs_object_id", "hs_task_status", "hs_task_subject", "hs_timestamp"],
    "notes": ["hs_createdate", "hs_lastmodifieddate", "hs_object_id", "hs_note_body", "hs_timestamp"],
    "meetings": ["hs_createdate", "hs_lastmodifieddate", "hs_object_id", "hs_meeting_body", "hs_meeting_title", "hs_timestamp"],
    "calls": ["hs_createdate", "hs_lastmodifieddate", "hs_object_id", "hs_call_body", "hs_call_title", "hs_timestamp"],
    "emails": ["hs_createdate", "hs_lastmodifieddate", "hs_object_id", "hs_email_subject", "hs_email_text", "hs_timestamp"],
}

LIFECYCLE = ["subscriber", "lead", "marketingqualifiedlead", "salesqualifiedlead", "opportunity", "customer", "evangelist", "other"]
TICKET_PRIORITY = ["LOW", "MEDIUM", "HIGH", "URGENT"]
TASK_STATUS = ["NOT_STARTED", "IN_PROGRESS", "WAITING", "COMPLETED", "DEFERRED"]

# (name, label, type, fieldType, options?)  — type: string|number|date|datetime|enumeration|bool
_P = tuple
_COMMON_SYS = [
    ("hs_object_id", "Record ID", "number", "number"),
    ("hs_createdate", "Create Date", "datetime", "date"),
    ("hs_lastmodifieddate", "Last Modified Date", "datetime", "date"),
]
_ENGAGEMENT = [
    ("hs_timestamp", "Activity date", "datetime", "date"),
    ("hubspot_owner_id", "Activity assigned to", "enumeration", "select"),
]

DEFAULT_PROPERTIES: dict[str, list[tuple]] = {
    "contacts": [
        ("hs_object_id", "Record ID", "number", "number"),
        ("createdate", "Create Date", "datetime", "date"),
        ("lastmodifieddate", "Last Modified Date", "datetime", "date"),
        ("firstname", "First Name", "string", "text"),
        ("lastname", "Last Name", "string", "text"),
        ("email", "Email", "string", "text"),
        ("phone", "Phone Number", "string", "phonenumber"),
        ("mobilephone", "Mobile Phone Number", "string", "phonenumber"),
        ("company", "Company Name", "string", "text"),
        ("jobtitle", "Job Title", "string", "text"),
        ("website", "Website URL", "string", "text"),
        ("city", "City", "string", "text"),
        ("state", "State/Region", "string", "text"),
        ("country", "Country/Region", "string", "text"),
        ("address", "Street Address", "string", "text"),
        ("zip", "Postal Code", "string", "text"),
        ("lifecyclestage", "Lifecycle Stage", "enumeration", "radio", LIFECYCLE),
        ("hs_lead_status", "Lead Status", "enumeration", "radio", ["NEW", "OPEN", "IN_PROGRESS", "OPEN_DEAL", "UNQUALIFIED", "ATTEMPTED_TO_CONTACT", "CONNECTED", "BAD_TIMING"]),
        ("hubspot_owner_id", "Contact owner", "enumeration", "select"),
        ("associatedcompanyid", "Primary Associated Company ID", "number", "number"),
        ("hs_additional_emails", "Additional email addresses", "enumeration", "checkbox"),
    ],
    "companies": [
        ("hs_object_id", "Record ID", "number", "number"),
        ("createdate", "Create Date", "datetime", "date"),
        ("hs_lastmodifieddate", "Last Modified Date", "datetime", "date"),
        ("name", "Company name", "string", "text"),
        ("domain", "Company Domain Name", "string", "text"),
        ("hs_additional_domains", "Additional Domains", "enumeration", "checkbox"),
        ("website", "Website URL", "string", "text"),
        ("phone", "Phone Number", "string", "phonenumber"),
        ("address", "Street Address", "string", "text"),
        ("city", "City", "string", "text"),
        ("state", "State/Region", "string", "text"),
        ("zip", "Postal Code", "string", "text"),
        ("country", "Country/Region", "string", "text"),
        ("industry", "Industry", "enumeration", "select"),
        ("description", "Description", "string", "textarea"),
        ("numberofemployees", "Number of Employees", "number", "number"),
        ("annualrevenue", "Annual Revenue", "number", "number"),
        ("lifecyclestage", "Lifecycle Stage", "enumeration", "radio", LIFECYCLE),
        ("hubspot_owner_id", "Company owner", "enumeration", "select"),
        ("num_associated_contacts", "Number of Associated Contacts", "number", "number"),
        ("num_associated_deals", "Number of Associated Deals", "number", "number"),
    ],
    "deals": [
        ("hs_object_id", "Record ID", "number", "number"),
        ("createdate", "Create Date", "datetime", "date"),
        ("hs_lastmodifieddate", "Last Modified Date", "datetime", "date"),
        ("dealname", "Deal Name", "string", "text"),
        ("amount", "Amount", "number", "number"),
        ("deal_currency_code", "Currency", "enumeration", "select", ["EUR", "USD", "GBP"]),
        ("pipeline", "Pipeline", "enumeration", "select"),
        ("dealstage", "Deal Stage", "enumeration", "radio"),
        ("closedate", "Close Date", "datetime", "date"),
        ("dealtype", "Deal Type", "enumeration", "radio", ["newbusiness", "existingbusiness"]),
        ("description", "Deal Description", "string", "textarea"),
        ("hubspot_owner_id", "Deal owner", "enumeration", "select"),
        ("hs_is_closed", "Is Deal Closed?", "bool", "booleancheckbox"),
        ("hs_is_closed_won", "Is Closed Won", "bool", "booleancheckbox"),
        ("hs_deal_stage_probability", "Deal probability", "number", "number"),
        ("hs_priority", "Priority", "enumeration", "select", ["low", "medium", "high"]),
    ],
    "tickets": [
        ("hs_object_id", "Record ID", "number", "number"),
        ("createdate", "Create date", "datetime", "date"),
        ("hs_lastmodifieddate", "Last Modified Date", "datetime", "date"),
        ("subject", "Ticket name", "string", "text"),
        ("content", "Ticket description", "string", "textarea"),
        ("hs_pipeline", "Pipeline", "enumeration", "select"),
        ("hs_pipeline_stage", "Ticket status", "enumeration", "select"),
        ("hs_ticket_priority", "Priority", "enumeration", "select", TICKET_PRIORITY),
        ("hs_ticket_category", "Category", "enumeration", "checkbox", ["PRODUCT_ISSUE", "BILLING_ISSUE", "FEATURE_REQUEST", "GENERAL_INQUIRY"]),
        ("closed_date", "Close date", "datetime", "date"),
        ("source_type", "Source", "enumeration", "select", ["CHAT", "EMAIL", "FORM", "PHONE"]),
        ("hubspot_owner_id", "Ticket owner", "enumeration", "select"),
    ],
    "products": [
        ("hs_object_id", "Record ID", "number", "number"),
        ("createdate", "Create Date", "datetime", "date"),
        ("hs_lastmodifieddate", "Last Modified Date", "datetime", "date"),
        ("name", "Name", "string", "text"),
        ("description", "Description", "string", "textarea"),
        ("price", "Unit price", "number", "number"),
        ("hs_sku", "SKU", "string", "text"),
        ("hs_cost_of_goods_sold", "Unit cost", "number", "number"),
        ("hs_recurring_billing_period", "Term", "string", "text"),
    ],
    "line_items": [
        ("hs_object_id", "Record ID", "number", "number"),
        ("createdate", "Create Date", "datetime", "date"),
        ("hs_lastmodifieddate", "Last Modified Date", "datetime", "date"),
        ("name", "Name", "string", "text"),
        ("description", "Description", "string", "textarea"),
        ("quantity", "Quantity", "number", "number"),
        ("price", "Unit price", "number", "number"),
        ("amount", "Net price", "number", "number"),
        ("hs_discount_percentage", "Discount (%)", "number", "number"),
        ("discount", "Unit discount", "number", "number"),
        ("hs_product_id", "Product ID", "number", "number"),
        ("hs_sku", "SKU", "string", "text"),
        ("hs_line_item_currency_code", "Currency", "enumeration", "select", ["EUR", "USD", "GBP"]),
    ],
    "quotes": _COMMON_SYS + [
        ("hs_title", "Quote name", "string", "text"),
        ("hs_expiration_date", "Expiration date", "datetime", "date"),
        ("hs_status", "Quote approval status", "enumeration", "select", ["DRAFT", "APPROVAL_NOT_NEEDED", "PENDING_APPROVAL", "APPROVED", "REJECTED"]),
        ("hs_currency", "Currency", "enumeration", "select", ["EUR", "USD", "GBP"]),
    ],
    "tasks": _COMMON_SYS + _ENGAGEMENT + [
        ("hs_task_subject", "Task Title", "string", "text"),
        ("hs_task_body", "Notes", "string", "html"),
        ("hs_task_status", "Task Status", "enumeration", "select", TASK_STATUS),
        ("hs_task_priority", "Priority", "enumeration", "select", ["NONE", "LOW", "MEDIUM", "HIGH"]),
        ("hs_task_type", "Task Type", "enumeration", "select", ["CALL", "EMAIL", "TODO", "LINKED_IN"]),
    ],
    "notes": _COMMON_SYS + _ENGAGEMENT + [
        ("hs_note_body", "Note body", "string", "html"),
        ("hs_attachment_ids", "Attached file IDs", "enumeration", "checkbox"),
    ],
    "meetings": _COMMON_SYS + _ENGAGEMENT + [
        ("hs_meeting_title", "Meeting name", "string", "text"),
        ("hs_meeting_body", "Meeting description", "string", "html"),
        ("hs_internal_meeting_notes", "Internal notes", "string", "html"),
        ("hs_meeting_location", "Location", "string", "text"),
        ("hs_meeting_start_time", "Start Time", "datetime", "date"),
        ("hs_meeting_end_time", "End Time", "datetime", "date"),
        ("hs_meeting_outcome", "Meeting outcome", "enumeration", "select", ["SCHEDULED", "COMPLETED", "RESCHEDULED", "NO_SHOW", "CANCELED"]),
    ],
    "calls": _COMMON_SYS + _ENGAGEMENT + [
        ("hs_call_title", "Call Title", "string", "text"),
        ("hs_call_body", "Call notes", "string", "html"),
        ("hs_call_direction", "Call direction", "enumeration", "select", ["INBOUND", "OUTBOUND"]),
        ("hs_call_duration", "Call duration", "number", "number"),
        ("hs_call_status", "Call status", "enumeration", "select", ["BUSY", "CALLING_CRM_USER", "CANCELED", "COMPLETED", "CONNECTING", "FAILED", "IN_PROGRESS", "NO_ANSWER", "QUEUED", "RINGING"]),
        ("hs_call_to_number", "To number", "string", "text"),
        ("hs_call_from_number", "From number", "string", "text"),
    ],
    "emails": _COMMON_SYS + _ENGAGEMENT + [
        ("hs_email_subject", "Email subject", "string", "text"),
        ("hs_email_text", "Email body", "string", "textarea"),
        ("hs_email_html", "Email HTML body", "string", "html"),
        ("hs_email_direction", "Email direction", "enumeration", "select", ["EMAIL", "INCOMING_EMAIL", "FORWARDED_EMAIL"]),
        ("hs_email_status", "Email send status", "enumeration", "select", ["BOUNCED", "FAILED", "SCHEDULED", "SENDING", "SENT"]),
        ("hs_email_headers", "Email headers", "string", "textarea"),
    ],
}

# Read-only system props the store maintains itself.
SYSTEM_PROPS = {"hs_object_id", "createdate", "hs_createdate", "lastmodifieddate", "hs_lastmodifieddate"}


def property_rows(otype: str):
    """Yield dicts ready for the property_defs table."""
    for i, p in enumerate(DEFAULT_PROPERTIES[otype]):
        name, label, ptype, field = p[0], p[1], p[2], p[3]
        opts = p[4] if len(p) > 4 else []
        yield {
            "object_type": otype, "name": name, "label": label, "type": ptype, "field_type": field,
            "group_name": f"{OBJECT_TYPES[otype][1]}information",
            "options": [{"label": o, "value": o, "displayOrder": j, "hidden": False} for j, o in enumerate(opts)],
            "display_order": i, "has_unique_value": False, "hubspot_defined": True,
            "calculated": name in SYSTEM_PROPS, "read_only": name in SYSTEM_PROPS,
        }


# ---- pipelines -----------------------------------------------------------
DEFAULT_PIPELINES = [
    {
        "object_type": "deals", "id": "default", "label": "Sales Pipeline", "display_order": 0,
        "stages": [
            ("appointmentscheduled", "Appointment Scheduled", {"isClosed": "false", "probability": "0.2"}),
            ("qualifiedtobuy", "Qualified To Buy", {"isClosed": "false", "probability": "0.4"}),
            ("presentationscheduled", "Presentation Scheduled", {"isClosed": "false", "probability": "0.6"}),
            ("decisionmakerboughtin", "Decision Maker Bought-In", {"isClosed": "false", "probability": "0.8"}),
            ("contractsent", "Contract Sent", {"isClosed": "false", "probability": "0.9"}),
            ("closedwon", "Closed Won", {"isClosed": "true", "probability": "1.0"}),
            ("closedlost", "Closed Lost", {"isClosed": "true", "probability": "0.0"}),
        ],
    },
    {
        "object_type": "tickets", "id": "0", "label": "Support Pipeline", "display_order": 0,
        "stages": [
            ("1", "New", {"ticketState": "OPEN", "isClosed": "false"}),
            ("2", "Waiting on contact", {"ticketState": "OPEN", "isClosed": "false"}),
            ("3", "Waiting on us", {"ticketState": "OPEN", "isClosed": "false"}),
            ("4", "Closed", {"ticketState": "CLOSED", "isClosed": "true"}),
        ],
    },
]

# ---- associations ----------------------------------------------------------
# (from, to, typeId, label)  label None = unlabeled default; "Primary" = primary.
_A = [
    ("contacts", "companies", 279, None), ("companies", "contacts", 280, None),
    ("contacts", "companies", 1, "Primary"), ("companies", "contacts", 2, "Primary"),
    ("contacts", "contacts", 449, None),
    ("contacts", "deals", 4, None), ("deals", "contacts", 3, None),
    ("contacts", "tickets", 15, None), ("tickets", "contacts", 16, None),
    ("contacts", "calls", 193, None), ("calls", "contacts", 194, None),
    ("contacts", "emails", 197, None), ("emails", "contacts", 198, None),
    ("contacts", "meetings", 199, None), ("meetings", "contacts", 200, None),
    ("contacts", "notes", 201, None), ("notes", "contacts", 202, None),
    ("contacts", "tasks", 203, None), ("tasks", "contacts", 204, None),
    ("contacts", "quotes", 70, None), ("quotes", "contacts", 69, None),
    ("companies", "companies", 450, None),
    ("companies", "deals", 342, None), ("deals", "companies", 341, None),
    ("companies", "deals", 6, "Primary"), ("deals", "companies", 5, "Primary"),
    ("companies", "tickets", 340, None), ("tickets", "companies", 339, None),
    ("companies", "tickets", 25, "Primary"), ("tickets", "companies", 26, "Primary"),
    ("companies", "calls", 181, None), ("calls", "companies", 182, None),
    ("companies", "emails", 185, None), ("emails", "companies", 186, None),
    ("companies", "meetings", 187, None), ("meetings", "companies", 188, None),
    ("companies", "notes", 189, None), ("notes", "companies", 190, None),
    ("companies", "tasks", 191, None), ("tasks", "companies", 192, None),
    ("quotes", "companies", 71, None),
    ("deals", "deals", 451, None),
    ("deals", "tickets", 27, None), ("tickets", "deals", 28, None),
    ("deals", "line_items", 19, None), ("line_items", "deals", 20, None),
    ("deals", "quotes", 63, None), ("quotes", "deals", 64, None),
    ("deals", "calls", 205, None), ("calls", "deals", 206, None),
    ("deals", "emails", 209, None), ("emails", "deals", 210, None),
    ("deals", "meetings", 211, None), ("meetings", "deals", 212, None),
    ("deals", "notes", 213, None), ("notes", "deals", 214, None),
    ("deals", "tasks", 215, None), ("tasks", "deals", 216, None),
    ("tickets", "calls", 219, None), ("calls", "tickets", 220, None),
    ("tickets", "emails", 223, None), ("emails", "tickets", 224, None),
    ("tickets", "meetings", 225, None), ("meetings", "tickets", 226, None),
    ("tickets", "notes", 227, None), ("notes", "tickets", 228, None),
    ("tickets", "tasks", 229, None), ("tasks", "tickets", 230, None),
    ("quotes", "line_items", 67, None), ("line_items", "quotes", 68, None),
    ("quotes", "tasks", 217, None), ("tasks", "quotes", 218, None),
]

ASSOC_TYPES = [{"from": f, "to": t, "type_id": i, "label": l, "category": "HUBSPOT_DEFINED"} for f, t, i, l in _A]

# default (unlabeled) type per direction
DEFAULT_ASSOC: dict[tuple[str, str], int] = {(a["from"], a["to"]): a["type_id"] for a in ASSOC_TYPES if a["label"] is None}
# primary type per direction (contact/deal/ticket -> company and inverses)
PRIMARY_ASSOC: dict[tuple[str, str], int] = {(a["from"], a["to"]): a["type_id"] for a in ASSOC_TYPES if a["label"] == "Primary"}
# inverse typeId lookup for HUBSPOT_DEFINED types
_BY_DIR: dict[tuple[str, str, str | None], int] = {(a["from"], a["to"], a["label"]): a["type_id"] for a in ASSOC_TYPES}
INVERSE: dict[int, int] = {}
for a in ASSOC_TYPES:
    inv = _BY_DIR.get((a["to"], a["from"], a["label"]))
    if inv is not None:
        INVERSE[a["type_id"]] = inv
# self-associations are their own inverse
for _t in (449, 450, 451):
    INVERSE[_t] = _t


def assoc_type_name(from_type: str, to_type: str, label: str | None) -> str:
    """e.g. contact_to_company, contact_to_company_unlabeled is NOT used here."""
    return f"{OBJECT_TYPES[from_type][1]}_to_{OBJECT_TYPES[to_type][1]}"
