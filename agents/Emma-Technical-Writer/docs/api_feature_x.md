API Reference: Feature X

Overview
- Purpose: Feature X lets authorized clients activate and check the activation status of a new product capability.
- Audience: Backend integrators and SDK authors.

Base URL
- https://api.example.com/v1

Authentication
- All endpoints require Bearer tokens (OAuth 2.0). Include Authorization: Bearer <token>.

Endpoints

1) POST /v1/feature-x/activate
- Description: Activate Feature X for a given tenant or resource.
- Authorization: Requires scope: feature_x:write
- Request
  - Content-Type: application/json
  - Body schema:
    {
      "tenant_id": "string",
      "resource_id": "string",
      "activate": true
    }
  - Example (curl):
    curl -X POST "https://api.example.com/v1/feature-x/activate" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"tenant_id":"t-123","resource_id":"r-456","activate":true}'
- Responses
  - 200 OK
    {
      "status": "activated",
      "feature_id": "feature-x",
      "activated_at": "2026-03-09T12:34:56Z"
    }
  - 400 Bad Request — invalid input
  - 401 Unauthorized — missing/invalid token
  - 403 Forbidden — insufficient scope
  - 422 Unprocessable Entity — 422_FEATURE_INACTIVE: Feature cannot be activated due to precondition (see error codes)
  - 500 Internal Server Error

2) GET /v1/feature-x/status
- Description: Retrieve activation status for a tenant/resource.
- Authorization: Requires scope: feature_x:read
- Query parameters
  - tenant_id (required) — string
  - resource_id (optional) — string
  - include_history (optional, boolean, default=false) — return activation event history
  - page_size (optional, int, default=50) — pagination size
- Example
  curl -X GET "https://api.example.com/v1/feature-x/status?tenant_id=t-123&include_history=true&page_size=10" \
    -H "Authorization: Bearer $TOKEN"
- Responses
  - 200 OK
    {
      "tenant_id": "t-123",
      "resource_id": "r-456",
      "status": "activated",
      "activated_at": "2026-03-09T12:34:56Z",
      "history": [ /* events */ ]
    }
  - 400 Bad Request — missing required params
  - 401 Unauthorized
  - 404 Not Found — tenant/resource not found
  - 500 Internal Server Error

Error Codes (summary)
- 422_FEATURE_INACTIVE — Feature X cannot be activated due to business precondition. Remediation: ensure preconditions met; contact support if stuck.

Notes
- Pagination follows cursor-based pattern when include_history=true. Provide Link headers for next page.
- Ensure clients handle 422 specially with suggested remediation.

