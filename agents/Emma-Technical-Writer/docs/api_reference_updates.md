API Reference — Impacted Endpoints

Overview
This file will contain the updated API reference for endpoints changed in the upstream PR. For the initial PR draft, include the endpoints that the report listed as impacted. Backend must confirm exact request/response schemas before finalizing.

Endpoints (placeholder list — to be replaced with exact diffs)
1. POST /api/v1/xyz
   - Description: Creates an XYZ resource. Changes: added field `enable_foo` (boolean), modified `bar` from string to enum.
   - Request example (JSON):
     {
       "name": "example",
       "enable_foo": true,
       "bar": "TYPE_A"
     }
   - Response example (201):
     {
       "id": "xyz_123",
       "name": "example",
       "enable_foo": true,
       "bar": "TYPE_A",
       "created_at": "2026-03-09T12:00:00Z"
     }
   - Error codes:
     - 400: Invalid `bar` value — message: "bar must be one of: TYPE_A, TYPE_B".
     - 422: Missing required field `name`.

2. PATCH /api/v1/abc/{id}
   - Description: Partial update for ABC resource. Changes: added optional `threshold` parameter.
   - Request example (JSON):
     {
       "threshold": 0.75
     }
   - Response example (200):
     {
       "id": "abc_456",
       "threshold": 0.75,
       "updated_at": "2026-03-09T12:05:00Z"
     }
   - Error codes:
     - 404: Resource not found.

Notes for backend
- Please replace placeholder endpoints with the canonical list and full JSON schemas.
- Confirm whether `enable_foo` is required at create time or default=false when omitted.

Prepared by: Emma (Technical Writer)
