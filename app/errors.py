"""HubSpot-shaped errors. Raise ApiError anywhere; main.py renders it."""
from __future__ import annotations

import uuid

from fastapi.responses import ORJSONResponse

_STATUS_CATEGORY = {
    400: "VALIDATION_ERROR",
    401: "INVALID_AUTHENTICATION",
    403: "MISSING_SCOPES",
    404: "OBJECT_NOT_FOUND",
    405: "VALIDATION_ERROR",
    409: "CONFLICT",
    429: "RATE_LIMITS",
    500: "INTERNAL_ERROR",
    501: "VALIDATION_ERROR",
}


class ApiError(Exception):
    def __init__(self, status: int, message: str, category: str | None = None,
                 errors: list | None = None, context: dict | None = None, sub_category: str | None = None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.category = category or _STATUS_CATEGORY.get(status, "VALIDATION_ERROR")
        self.errors = errors
        self.context = context
        self.sub_category = sub_category


def error_body(status: int, message: str, category: str | None = None, errors=None, context=None,
               sub_category=None) -> dict:
    body = {
        "status": "error",
        "message": message,
        "correlationId": str(uuid.uuid4()),
        "category": category or _STATUS_CATEGORY.get(status, "VALIDATION_ERROR"),
    }
    if sub_category:
        body["subCategory"] = sub_category
    if errors:
        body["errors"] = errors
    if context:
        body["context"] = context
    return body


def error_response(status: int, message: str, **kw) -> ORJSONResponse:
    return ORJSONResponse(error_body(status, message, **kw), status_code=status)


def not_found(otype: str, oid) -> ApiError:
    return ApiError(404, f"resource not found: {otype} {oid}", "OBJECT_NOT_FOUND")
