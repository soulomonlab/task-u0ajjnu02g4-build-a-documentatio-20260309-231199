# API Contract for Frontend Task #113

Summary
- Primary resource: Resource (id:string, name:string, createdAt:string (ISO8601), updatedAt?:string, metadata?:object)
- Base API prefix: /api/v1
- Auth: Bearer JWT access token + refresh token rotation via POST /api/v1/auth/refresh

1) Endpoints (paths & methods)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET    | /api/v1/resources | List resources (paginated) | Bearer |
| GET    | /api/v1/resources/{id} | Get single resource | Bearer |
| POST   | /api/v1/resources | Create resource | Bearer |
| PUT    | /api/v1/resources/{id} | Update (replace) resource | Bearer |
| PATCH  | /api/v1/resources/{id} | Update (partial) resource | Bearer |
| POST   | /api/v1/auth/refresh | Refresh access token (rotation) | none / send refresh token |

2) Pagination (confirmed defaults)
- Query params: page (1-indexed, default=1) & per_page (default=25, max=100)
- Response wrapper: data + meta
- Meta fields:
  - page: number
  - per_page: number
  - total_pages: number
  - total_count: number
  - next_page: number | null

Example paginated response (200):
{
  "data": [
    {
      "id": "r_01F...",
      "name": "Resource A",
      "createdAt": "2026-03-09T12:00:00Z",
      "updatedAt": "2026-03-10T08:00:00Z",
      "metadata": { "color": "blue" }
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 25,
    "total_pages": 10,
    "total_count": 250,
    "next_page": 2
  }
}

3) Resource shape (primary fields)
- id: string (UUID-like or service id)
- name: string
- createdAt: string (ISO8601)
- updatedAt: string | null (ISO8601)
- metadata: object | null (free-form JSON)

List wrapper: "data" (array of resources)
Single resource response: { "data": { <resource> } }

Examples:
- Successful single resource (200):
{
  "data": {
    "id": "r_01F...",
    "name": "Resource A",
    "createdAt": "2026-03-09T12:00:00Z",
    "updatedAt": "2026-03-10T08:00:00Z",
    "metadata": { "color": "blue" }
  }
}

- Create resource (POST /api/v1/resources) behavior:
  - Request: JSON body with name + optional metadata
  - Response: 201 Created
    - Location header: /api/v1/resources/{id}
    - Body: { "data": { <created resource> } }

4) Error schema & status codes
- Global error payload:
{
  "error": {
    "code": "STRING_CODE",
    "message": "Human readable message",
    "details": { ... optional additional info ... }
  }
}

- Validation errors (400): details will be a map of field -> [messages]
Example 400 (validation):
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Validation failed",
    "details": {
      "name": ["must not be empty"],
      "metadata.color": ["must be a valid hex color"]
    }
  }
}

- 401 Unauthorized: missing/invalid/expired access token
  - code: "UNAUTHORIZED"
  - Client behavior: trigger token refresh flow (once) if a refresh token exists; do NOT loop refresh infinitely.
- 403 Forbidden: authenticated but insufficient permissions
  - code: "FORBIDDEN"
- 404 Not Found: resource absent
  - code: "NOT_FOUND"
- 409 Conflict: concurrency or unique-constraint conflict
  - Typical causes: duplicate unique key on create OR stale update (optimistic locking)
  - Response body example:
{
  "error": {
    "code": "CONFLICT",
    "message": "Resource conflict: duplicate name",
    "details": { "resource_id": "r_existingId", "field": "name" }
  }
}
  - Client guidance: for create duplicates — stop and surface conflict to user (offer merge or use idempotency token). For updates due to stale data — re-fetch latest resource and reapply changes or use an If-Match/ETag workflow. Automatic retries: only with idempotency and exponential backoff; do not retry blind.
- 429 Too Many Requests: include Retry-After header (seconds) and rate limit headers (see below)
- 500 Server Error: generic server error, include request_id header for support correlation

5) Auth & Token rotation
- Scheme: Authorization: Bearer <access_token> (JWT opaque or signed)
- Access token: TTL 15 minutes (expires_in in seconds returned on refresh)
- Refresh token: TTL 7 days, rotated on refresh
- Refresh endpoint:
  - POST /api/v1/auth/refresh
  - Request: { "refresh_token": "<token>" } OR send refresh token as HttpOnly cookie if client uses cookies (frontend default will use in-memory storage and HTTP-only cookie not used unless opted-in)
  - Response: 200 OK
{
  "access_token": "<new_access_token>",
  "expires_in": 900,
  "refresh_token": "<new_refresh_token>" // rotated; client must replace stored refresh token
}
  - Rotation semantics: server invalidates previous refresh token when a refresh succeeds. If an attacker replays an old refresh token, server will reject and require re-login.
  - Delivery: new tokens returned in response body. We do NOT set Authorization header or Set-Cookie by default.
  - Recommended client flow: on 401, attempt refresh once, update storage, retry original request. If refresh returns 401/400, redirect to login.
  - Idempotency/replay protections: refresh tokens are single-use and rotated.

6) Rate limiting & retry guidance
- Response headers on successful responses (and 429):
  - X-RateLimit-Limit: integer
  - X-RateLimit-Remaining: integer
  - X-RateLimit-Reset: unix epoch seconds
- On 429: include Retry-After (seconds). Client should back off and retry after Retry-After or use exponential backoff with jitter.

7) Long-running operations & batch semantics
- For large async operations, endpoints will return 202 Accepted with Location header pointing to /api/v1/operations/{op_id}
- Polling endpoint: GET /api/v1/operations/{op_id} returns { status: "pending"|"running"|"succeeded"|"failed", result?: {...}, errors?: {...} }
- Partial success for batch endpoints: 207 Multi-Status is NOT used. Instead, API returns 200 with per-item results and an overall "success_count"/"failed_count" plus an array of items with status per item.

8) Examples (request/response)

List (GET /api/v1/resources?page=1&per_page=25)
Request: GET /api/v1/resources?page=1&per_page=25
Response 200: (see paginated example above)

Single (GET /api/v1/resources/r_01F...)
Request: GET /api/v1/resources/r_01F...
Response 200:
{ "data": { "id":"r_01F...","name":"Resource A","createdAt":"2026-03-09T12:00:00Z","updatedAt":null } }
Errors:
- 404: { "error": { "code":"NOT_FOUND","message":"Resource not found" } }
- 401: { "error": { "code":"UNAUTHORIZED","message":"Access token expired" } }

Create (POST /api/v1/resources)
Request body:
{ "name": "My new resource", "metadata": { "color":"#00ff00" } }
Response 201
Headers: Location: /api/v1/resources/r_abc123
Body:
{ "data": { "id":"r_abc123","name":"My new resource","createdAt":"2026-03-09T15:00:00Z" } }
Errors: 400 validation (see validation example); 409 conflict if duplicate unique key

Update (PATCH /api/v1/resources/{id})
Request body: { "name": "New name" }
Response 200: { "data": { <updated resource> } }
409 example for stale update:
Status 409
{ "error": { "code":"CONFLICT","message":"Update conflict: resource has been modified","details": { "current_version": 5 } } }

Auth refresh (POST /api/v1/auth/refresh)
Request: POST /api/v1/auth/refresh
Body: { "refresh_token": "rt_..." }
Response 200:
{ "access_token": "at_...", "expires_in": 900, "refresh_token": "rt_new_..." }
Errors: 400/401 invalid token -> require re-login

9) API headers for observability & debugging
- X-Request-Id: echoed per request
- X-Server-Version: service build id (optional)

10) Client-side recommendations (frontend)
- Use central ApiClient to manage Authorization header, token storage, refresh flow, retries
- On 401: attempt single refresh then retry original request once
- For POST creates that must be idempotent, include an Idempotency-Key header when appropriate
- Use ETag/If-Match for optimistic concurrency on updates (server will emit ETag header with resource version)

11) OpenAPI offer
- I can produce an OpenAPI snippet for the above contract. Let me know if you want a full YAML. (I included a minimal YAML in docs folder.)

---
Files created:
- output/specs/api_contract_task_113.md (this file)
- output/docs/openapi_resources_api.yaml (OpenAPI snippet)

If these shapes look good, confirm and frontend (Kevin) can proceed with implementation using the TS interfaces in output/specs/frontend_task_113.md. If you want adjustments (field names, pagination keys, delivery via cookie), tell me which exact change and I will update the spec.
