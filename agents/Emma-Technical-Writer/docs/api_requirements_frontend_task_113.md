# API Requirements for Frontend Task #113

Overview
- Purpose: Collect the exact API contract details frontend needs to implement task #113 without spec drift.
- Owner: Marcus (Backend) — requested by Kevin (Frontend). Reference frontend plan: output/specs/frontend_task_113.md

What we need from Backend (explicit, machine-readable)
1. Endpoints (for each endpoint involved in this feature)
   - URL path (e.g., /api/v1/items)
   - HTTP method (GET, POST, PUT, DELETE, PATCH)
   - Purpose/short description

2. Request details
   - Query parameters (name, type, required, description)
   - Request body JSON schema for POST/PUT/PATCH (field name, type, required, allowed values)
   - Content-Type expected (application/json)
   - Example request (curl + JSON payload)

3. Response details
   - Full success response JSON schema (field name, type, description)
   - Example success response (realistic JSON) for each endpoint
   - Pagination parameters (cursor vs page/offset, default & max page size, response fields for paging: next_cursor, total, links)
   - Date/time formats (ISO8601 / unix ms) and timezone assumptions
   - ID formats (UUID / integer) and if relationships are nested or via IDs

4. Error handling
   - Error response shape (top-level fields, e.g., {error: {code, message, details}})
   - HTTP status codes used for common error cases (400, 401, 403, 404, 409, 422, 500)
   - Example error responses for validation error, auth error, rate limit, and server error
   - Error codes/enums and machine-readable identifiers (e.g., ERR_ITEM_NOT_FOUND)

5. Authentication & Authorization
   - Auth method used (Bearer token in Authorization header, cookie-based session, API key)
   - Required scopes/permissions per endpoint (if applicable)
   - Token expiry behavior and refresh mechanism (if relevant)

6. Rate limiting & headers
   - Any rate-limiting headers returned (X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After)
   - CORS requirements (allowed origins) if applicable

7. Contracts & Stability
   - Which fields are guaranteed stable vs experimental
   - Deprecation policy and versioning expectations

Acceptance criteria (what Kevin needs to proceed)
- For every endpoint listed in output/specs/frontend_task_113.md, Marcus provides:
  1) Path + HTTP method
  2) Request examples and JSON schema
  3) At least one example success response JSON
  4) If paginated, exact pagination params and example paginated response
  5) Error response examples and status codes
  6) Auth method and required headers

Examples (templates)

Success response example (single resource):
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Example item",
  "status": "active",
  "created_at": "2025-03-01T12:34:56Z"
}

Paginated response example:
{
  "items": [ /* array of resource objects */ ],
  "paging": {
    "next_cursor": "abc123", 
    "limit": 20,
    "total": 345
  }
}

Error response example:
{
  "error": {
    "code": "ERR_INVALID_PARAM",
    "message": "'limit' must be <= 100",
    "details": { "field": "limit" }
  }
}

Quick checklist for Marcus (copyable)
- [ ] Confirm endpoint paths & HTTP methods
- [ ] Provide request schemas and request examples
- [ ] Provide success response examples for each endpoint
- [ ] Provide pagination contract (if used)
- [ ] Provide error response shape + examples
- [ ] Confirm auth method and required headers

Where this lives
- Frontend plan (existing): output/specs/frontend_task_113.md
- This doc (requirements to unblock frontend): output/docs/api_requirements_frontend_task_113.md

Why this matters
- Prevents rework from API spec drift; enables frontend to implement typed interfaces, tests, and smoke checks in one pass.

Next steps for Backend (Marcus)
- Reply in the PR thread or to #ai-backend with the items above. Prefer JSON examples and a short OpenAPI/JSON Schema snippet where possible.

Contact
- Creator (requestor): Emma (Technical Writer)
- Frontend owner: Kevin — referenced in output/specs/frontend_task_113.md
