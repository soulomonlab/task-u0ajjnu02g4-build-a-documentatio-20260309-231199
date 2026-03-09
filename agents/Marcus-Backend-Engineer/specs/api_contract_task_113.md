API Contract for Frontend Task #113

Summary
- This document provides exact endpoint paths, methods, request/response schemas, pagination, error formats, and auth details the frontend (Kevin) needs to implement task #113 without spec drift.

Endpoints

1) List Features
- Method: GET
- Path: /api/v1/features
- Auth: Bearer token (Authorization: Bearer <token>)
- Query parameters:
  - page (integer, optional, default=1): 1-based page number
  - per_page (integer, optional, default=20, max=100)
  - q (string, optional): text search across title and description

- Request example (GET /api/v1/features?page=2&per_page=10&q=onboarding):
  - No request body for GET

- Success response: 200
  - JSON schema:
    {
      "total_count": integer,
      "page": integer,
      "per_page": integer,
      "items": [ Feature ]
    }
  - Feature schema:
    {
      "id": string,
      "title": string,
      "description": string | null,
      "created_at": string (ISO-8601 UTC),
      "updated_at": string (ISO-8601 UTC) | null
    }

- Success example:
  {
    "total_count": 123,
    "page": 1,
    "per_page": 20,
    "items": [
      {"id": "f_01GXYZ", "title": "New onboarding flow", "description": "A/B test for onboarding screens", "created_at": "2026-03-01T12:34:56Z", "updated_at": "2026-03-02T11:20:00Z"}
    ]
  }

- Pagination contract: server returns total_count. Frontend should calculate totalPages = ceil(total_count / per_page). If items is empty and page > 1, server returns items: [] and 200.

- Error responses:
  - 400 Bad Request
    {"error": {"code": "INVALID_PARAMS", "message": "per_page must be <= 100"}}
  - 401 Unauthorized
    {"error": {"code": "UNAUTHORIZED", "message": "Missing or invalid Authorization header"}}
  - 500 Server Error
    {"error": {"code": "SERVER_ERROR", "message": "Unexpected error"}}

2) Get Feature
- Method: GET
- Path: /api/v1/features/{id}
- Auth: Bearer token (Authorization: Bearer <token>)
- Path parameters:
  - id (string): feature id

- Success response: 200
  - JSON schema: Feature (see above)
- Success example:
  {"id": "f_01GXYZ", "title": "New onboarding flow", "description": "A/B test for onboarding screens", "created_at": "2026-03-01T12:34:56Z", "updated_at": "2026-03-02T11:20:00Z"}

- Error responses:
  - 401 Unauthorized
    {"error": {"code": "UNAUTHORIZED", "message": "Missing or invalid Authorization header"}}
  - 404 Not Found
    {"error": {"code": "NOT_FOUND", "message": "Feature not found"}}
  - 500 Server Error
    {"error": {"code": "SERVER_ERROR", "message": "Unexpected error"}}

Auth
- Method: Bearer token using Authorization header
- Header: Authorization: Bearer <JWT>
- Token expiry and refresh: access token 15 minutes; refresh token rotation 7 days. (Frontend should only need the access token for these read endpoints.)

Rate limits & constraints
- per_page max 100. Default 20. No other rate limits specified; backend enforces standard org-wide rate limits and will return 429 if exceeded.

Notes / Decisions
- Cursor pagination avoided for this feature; frontend requested page/per_page and total_count for simple pagination controls.
- Field names use snake_case to match existing backend conventions (created_at, total_count).
- Error shape includes an 'error' object with code + message; details is optional.

Files
- OpenAPI spec: output/docs/openapi_features_task_113.yaml

Acceptance criteria for frontend
- Typescript interfaces should match Feature and FeaturesListResponse above.
- GET /api/v1/features must accept page/per_page and return total_count to compute total pages.

