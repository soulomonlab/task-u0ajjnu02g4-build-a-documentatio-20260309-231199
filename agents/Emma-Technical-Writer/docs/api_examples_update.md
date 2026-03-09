# API Examples — PR Follow-up

Source: output/reports/docs_update_from_pr_summary.md

Overview
- This document contains updated API request/response examples and notes to resolve ambiguities found in the PR.
- Target audience: backend engineers (Marcus) for confirmation, and docs reviewer (Chris).

Endpoints updated
1) POST /api/v1/widgets
   - Purpose: Create a widget
   - Key ambiguity: "size" field accepted values (int in PR vs string "S|M|L")

Example (proposed)
- Request (application/json):
  {
    "name": "blue widget",
    "size": "M",         // confirm: enum string vs integer
    "metadata": {"source":"ui"}
  }
- Success Response (201):
  {
    "id": "w_123",
    "name": "blue widget",
    "size": "M",
    "created_at": "2026-03-01T12:34:56Z"
  }
- Error Responses:
  - 400 Bad Request — invalid size value
  - 401 Unauthorized — missing/invalid token

Notes / Questions for Engineering (to be confirmed by Marcus):
- Is `size` an enum string ("S","M","L") or integer? If enum, list allowed values and casing.
- Does metadata accept arbitrary JSON? Any reserved keys?
- Are timestamps always ISO-8601 UTC?

2) GET /api/v1/widgets/{id}
   - Purpose: Retrieve widget details

Example (proposed)
- Success Response (200):
  {
    "id": "w_123",
    "name": "blue widget",
    "size": "M",
    "metadata": {"source":"ui"},
    "status": "active"  // confirm: possible status values
  }

Notes / Questions:
- Confirm `status` enum values and whether `deleted_at` is returned when soft-deleted.

Acceptance criteria for docs update (Engineering confirmation required):
- For each endpoint above, engineering confirms field types and allowed values.
- Confirmed examples produce exact JSON returned by the API (field names, casing, and optional fields documented).

Next steps:
- Engineer confirms answers in the tasks created alongside this PR.
- After confirmation, update these examples in the primary API reference and merge the docs PR.
