# Contesto e conversazioni dell’assistente


`POST /__agente`, with the token like every other call. No state is kept, neither on your side
nor ours: every turn sends the whole conversation so far.

```json
{
  "context": {
    "now": "2026-12-02T10:00:00+01:00",
    "user": "anna.sala@brambillaforniture.it"
  },
  "messages": [
    {"role": "user", "content": "...",
     "attachments": [{"name": "allegato.csv", "content_type": "text/csv", "content": "..."}]},
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "..."}
  ]
}
```

It replies `200` with `{"reply": "<text in Italian>"}`.

- **60 seconds per turn**: past that, the turn counts as an empty reply.
- `context.now` is the moment of the request: "today", "six months from now" count from there,
  not from the server's clock.
- `context.user` is who is writing, an active user from `utenti.csv`: "my customers" are theirs.
- Attachments are text only: a CSV in the `content` field, with Sinergia's `;` separator.
- Conversations arrive **4 at a time**, each on its own records.
