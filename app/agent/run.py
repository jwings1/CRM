"""POST /__agente. Lane C owns this package.

Contract: body {"context": {"now", "user"}, "messages": [{"role", "content", "attachments"?}]}
          -> reply text in Italian. Stateless, 60 s per turn, 4 concurrent conversations.

Plan (see PLAN.md "Lane C details"):
- OpenRouter chat completions with tools, model config.OPENROUTER_MODEL ONLY, key config.OPENROUTER_API_KEY.
- Tools call app.store directly (inside `async with db.pool.acquire() as conn`) so R7/R10/R11/R12 apply.
- <= 8 tool steps, stop at ~45 s and answer with what is known.
- $10 budget for the whole day: never loop on the model in dev.
"""
from __future__ import annotations

STUB_REPLY = ("Ciao! Sono l'assistente del CRM di Brambilla Forniture. "
              "Al momento non riesco a completare la richiesta: riprova tra poco.")


async def reply(body: dict) -> str:
    # TODO Lane C: real tool loop. The stub keeps the contract valid without spending the key.
    return STUB_REPLY
