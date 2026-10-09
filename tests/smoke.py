"""Smoke test against a running CRM (local or Railway). RESETS THE DATA.
    BASE_URL=http://localhost:8000 CRM_TOKEN=dev python tests/smoke.py
Add a check here every time you ship a feature; run it before every push."""
from __future__ import annotations

import os
import sys
import time

import httpx

BASE = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")
TOKEN = os.environ.get("CRM_TOKEN", "dev")
V = "/crm/objects/2026-09"
H = {"Authorization": f"Bearer {TOKEN}"}
c = httpx.Client(base_url=BASE, headers=H, timeout=30)
fails = 0


def check(name: str, cond: bool, detail=""):
    global fails
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"  -> {detail}"))
    fails += 0 if cond else 1


r = httpx.get(BASE + "/health")
check("health 200 + shape", r.status_code == 200 and r.json().get("status") == "ok"
      and r.json().get("version") == "2026-09" and isinstance(r.json().get("ui"), dict), r.text)
check("401 without token", httpx.get(BASE + V + "/contacts").status_code == 401)
check("401 bad token", httpx.get(BASE + V + "/contacts", headers={"Authorization": "Bearer nope"}).status_code == 401)

t = time.monotonic()
r = c.post("/__reset")
check(f"reset 204 ({(time.monotonic() - t) * 1000:.0f} ms)", r.status_code == 204, r.text)

r = c.post(V + "/companies", json={"properties": {"name": "Acme S.p.A.", "domain": "acme.it", "city": "Milano"}})
check("create company 201", r.status_code == 201, r.text)
company = r.json()["id"]

r = c.post(V + "/contacts", json={"properties": {"firstname": "Anna", "lastname": "Sala", "email": "anna@acme.it"}})
check("create contact 201", r.status_code == 201, r.text)
contact = r.json()["id"]
r = c.get(f"{V}/contacts/{contact}", params={"associations": "companies"})
check("R12 contact auto-associated by email domain",
      company in [a["id"] for a in r.json().get("associations", {}).get("companies", {}).get("results", [])], r.text)

r = c.post(V + "/contacts", json={"properties": {"email": "ANNA@acme.it"}})
check("duplicate email 409", r.status_code == 409, r.text)
r = c.get(f"{V}/contacts/anna@acme.it", params={"idProperty": "email"})
check("get by email", r.status_code == 200 and r.json()["id"] == contact, r.text)

r = c.patch(f"{V}/contacts/{contact}", json={"properties": {"phone": "+39 02 123"}})
check("patch 200", r.status_code == 200 and r.json()["properties"]["phone"] == "+39 02 123", r.text)
r = c.get(f"{V}/contacts/{contact}", params={"properties": "firstname,phone"})
check("patch merged (firstname kept)", r.json()["properties"].get("firstname") == "Anna", r.text)

r = c.post(V + "/contacts", json={"properties": {"nope_prop": "x"}})
check("unknown property 400", r.status_code == 400 and r.json().get("category") == "VALIDATION_ERROR", r.text)
check("404 unknown id", c.get(V + "/contacts/999999999").status_code == 404)

r = c.post(V + "/deals", json={"properties": {"dealname": "Fornitura Acme", "amount": "1000", "dealstage": "appointmentscheduled"},
                               "associations": [{"to": {"id": company}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 341}]}]})
check("create deal with association", r.status_code == 201 and r.json()["properties"].get("pipeline") in (None, "default"), r.text)
deal = r.json()["id"]

r = c.patch(f"{V}/deals/{deal}", json={"properties": {"dealstage": "closedwon"}})
check("deal -> closedwon", r.status_code == 200, r.text)
r = c.get(f"{V}/deals/{deal}", params={"associations": "tickets"})
tickets = r.json().get("associations", {}).get("tickets", {}).get("results", [])
check("R10 kickoff ticket created", len(tickets) == 1, r.text)
if tickets:
    tk = c.get(f"{V}/tickets/{tickets[0]['id']}", params={"properties": "subject", "associations": "companies"}).json()
    check("R10 subject", tk["properties"]["subject"] == "Avvio fornitura - Fornitura Acme", tk)
    check("R10 ticket -> company", bool(tk.get("associations", {}).get("companies")), tk)
c.patch(f"{V}/deals/{deal}", json={"properties": {"dealstage": "contractsent"}})
c.patch(f"{V}/deals/{deal}", json={"properties": {"dealstage": "closedwon"}})
r = c.get(f"{V}/deals/{deal}", params={"associations": "tickets"})
check("R10 once per deal", len(r.json().get("associations", {}).get("tickets", {}).get("results", [])) == 1, r.text)

r = c.post(V + "/deals", json={"properties": {"dealname": "Persa X", "dealstage": "closedlost"}})
lost = r.json()["id"]
r = c.get(f"{V}/deals/{lost}", params={"associations": "tasks"})
tasks = r.json().get("associations", {}).get("tasks", {}).get("results", [])
check("R11 task on create in closedlost", len(tasks) == 1, r.text)
if tasks:
    tk = c.get(f"{V}/tasks/{tasks[0]['id']}", params={"properties": "hs_task_subject,hs_task_status,hs_timestamp"}).json()
    check("R11 task props", tk["properties"]["hs_task_subject"] == "Richiamare: Persa X"
          and tk["properties"]["hs_task_status"] == "NOT_STARTED", tk)

r = c.get(V + "/contacts", params={"limit": 1})
check("list paging", r.status_code == 200 and len(r.json()["results"]) == 1, r.text)
r = c.get("/crm/pipelines/2026-09/deals")
check("pipelines deals default", any(p["id"] == "default" for p in r.json().get("results", [])), r.text)
r = c.get("/crm/properties/2026-09/companies/name")
check("property get", r.status_code == 200 and r.json()["name"] == "name", r.text)

r = c.delete(f"{V}/contacts/{contact}")
check("archive 204", r.status_code == 204)
check("archived -> 404", c.get(f"{V}/contacts/{contact}").status_code == 404)

r = c.post("/__agente", json={"context": {"now": "2026-12-02T10:00:00+01:00", "user": "anna.sala@brambillaforniture.it"},
                              "messages": [{"role": "user", "content": "Ciao"}]})
check("agente contract", r.status_code == 200 and isinstance(r.json().get("reply"), str), r.text)

print(f"\n{fails} failing")
sys.exit(1 if fails else 0)
