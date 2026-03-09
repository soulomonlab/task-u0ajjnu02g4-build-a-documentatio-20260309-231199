# Anthropic Worker Mapping API — Documentation Draft

## Overview
This document describes the changes required to document the Anthropic worker mapping feature introduced in the recent PR. It is a draft prepared by Documentation to be finalized after backend confirmation of exact API diffs.

Who this is for
- Backend engineers (confirm API diffs)
- SDK consumers (devs integrating our worker routing)
- QA (test validation against acceptance criteria)

Status: Draft — Requires backend confirmation (see Open Questions)

---

## Endpoints (draft)
> NOTE: The exact endpoint paths and field names below are provisional. Marcus must confirm the final API diffs.

### GET /api/v1/workers/anthropic/mapping
Retrieve the current mapping configuration for Anthropic workers.

Request
- Query parameters (draft):
  - environment (string, optional): `production` | `staging`

Response (200) — provisional
{
  "environment": "production",
  "mappings": [
    {
      "worker_id": "anthropic-001",      // TODO: confirm field name
      "model": "claude-2",              // TODO: confirm
      "capacity": 0.75,
      "tags": ["text-generation", "priority-high"]
    }
  ]
}

Error responses (draft)
- 400 Bad Request — invalid query params
- 401 Unauthorized — invalid api key
- 500 Internal Server Error — server-side failure

---

### POST /api/v1/workers/anthropic/mapping
Create or update mapping entries.

Request (application/json) — provisional
{
  "environment": "production",
  "mappings": [
    {
      "worker_id": "anthropic-001",
      "model": "claude-2",
      "capacity": 0.5,
      "tags": ["text-generation"]
    }
  ]
}

Response (200) — provisional
{
  "status": "ok",
  "updated": 1
}

---

## Authentication
- Standard API key-based header: `Authorization: Bearer <API_KEY>`

## Examples
> These examples are placeholders. Marcus: please confirm exact request/response shapes; we will update samples once you confirm.

cURL (draft)

curl -X POST "https://api.example.com/api/v1/workers/anthropic/mapping" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"environment":"production","mappings":[{"worker_id":"anthropic-001","model":"claude-2","capacity":0.5}]}'

Python (draft)

from requests import post

resp = post(
    "https://api.example.com/api/v1/workers/anthropic/mapping",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={"environment":"production","mappings":[{"worker_id":"anthropic-001","model":"claude-2","capacity":0.5}]}
)
print(resp.json())

---

## Acceptance criteria for docs
- Backend (Marcus) confirms final endpoint paths and request/response field names.
- API reference includes at least one validated request/response example per endpoint.
- Error codes and edge cases documented.
- QA (Dana) validates examples against a staging environment and marks them green.

---

## Open questions (action required from backend)
1. Confirm exact endpoint paths (GET/POST) and whether `/anthropic/` is correct.
2. Confirm final field names: `worker_id` vs `id`, `model` vs `model_name`.
3. Confirm additional required fields (e.g., `region`, `priority`) not present in the PR diff.
4. Provide sample payloads from the canonical implementation (staging response) so we can replace placeholders.

---

## Notes for reviewers
- I intentionally kept examples minimal to avoid drifting from the implementation. Once Marcus provides the canonical payloads, docs will be finalized.
- QA test cases referenced in the runbook should be validated by Dana.
