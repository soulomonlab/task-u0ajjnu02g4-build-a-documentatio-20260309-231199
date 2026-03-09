# Example Payloads — Old (v1) vs New (v2)

## 1) Create record with client id provided

Old (v1):
{
  "id": "c1_rec_0001",
  "timestamp": "2026-03-01T12:00:00Z",
  "payload": { "event": "login", "user_id": "u123" },
  "source": "webapp"
}

New (v2):
{
  "id": "c1_rec_0001",
  "timestamp": "2026-03-01T12:00:00Z",
  "payload": { "event": "login", "user_id": "u123" },
  "source": "webapp",
  "unique_key": "user:u123:event:login",
  "token": { "token_id": "tk_9a8b7c", "token_version": 2, "issued_at": "2026-03-01T11:59:50Z" }
}

## 2) Create record without client id (server-generated id)

Old (v1):
{
  "timestamp": "2026-03-01T12:05:00Z",
  "payload": { "event": "purchase", "amount": 19.99, "user_id": "u123" },
  "source": "mobile"
}

New (v2):
{
  "timestamp": "2026-03-01T12:05:00Z",
  "payload": { "event": "purchase", "amount": 19.99, "user_id": "u123" },
  "source": "mobile",
  "unique_key": "order:ord_456:user:u123",
  "token": { "token_id": "tk_9a8b80", "token_version": 1 }
}

## 3) Idempotent retry causing 409 previously — now deduped via unique_key

Old (v1) — conflict returned 409 when duplicate detected by id:
Request 1:
{
  "id": "c1_rec_0002",
  "timestamp": "2026-03-01T12:10:00Z",
  "payload": { "event": "subscribe", "user_id": "u124" },
  "source": "api"
}

Request 2 (retry with same id):
{
  "id": "c1_rec_0002",
  "timestamp": "2026-03-01T12:10:01Z",
  "payload": { "event": "subscribe", "user_id": "u124" },
  "source": "api"
}

Server response (v1): 409 Conflict

New (v2) — server deduplicates using unique_key and returns 200 with existing record id
Request 1:
{
  "timestamp": "2026-03-01T12:11:00Z",
  "payload": { "event": "subscribe", "user_id": "u124" },
  "source": "api",
  "unique_key": "user:u124:subscribe"
}

Request 2 (retry or near-duplicate):
{
  "timestamp": "2026-03-01T12:11:01Z",
  "payload": { "event": "subscribe", "user_id": "u124" },
  "source": "api",
  "unique_key": "user:u124:subscribe"
}

Server response (v2): 200 OK, body: { "id": "rec_7890", "status": "duplicate", "existing_id": "rec_7890" }
