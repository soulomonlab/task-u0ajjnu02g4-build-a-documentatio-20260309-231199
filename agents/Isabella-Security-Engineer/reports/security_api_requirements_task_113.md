Security API Requirements & Checklist — Task #113

Purpose
- Provide Marcus with a concise security-focused checklist and required API details so frontend (Kevin) can implement safely without rework.

Files created
- output/reports/security_api_requirements_task_113.md (this file)

Required API details (confirm each)
1) Endpoint surface
   - Full URL paths for each frontend-needed endpoint (e.g., GET /api/v1/items, POST /api/v1/items/{id}/action).
   - HTTP method per path.

2) Response shapes
   - Exact JSON schema for success responses (field names, types, optional/nullable, example values).
   - Which fields are considered PII or sensitive and must be redacted in logs.
   - Consistent timestamp format (ISO 8601, UTC).

3) Pagination
   - Pagination scheme: page/limit OR cursor-based (cursor, next_cursor).
   - Param names and types (page:int, limit:int, cursor:string).
   - Max/min limits and default page size.
   - Whether total_count is returned (and if it's expensive to compute).
   - How empty sets are represented.

4) Error format
   - Canonical error object shape (e.g., {code: string, message: string, details?: object}).
   - HTTP status codes used for common cases (400, 401, 403, 404, 409, 429, 500).
   - Error codes (machine-friendly) and mapping to user-facing messages.

5) Auth & Authorization
   - Type of auth: Bearer JWT in Authorization header OR cookie-based session.
   - If JWT: signing algorithm (RS256/HMAC?), claim names (sub, exp, scope), expiry policy, refresh token flow and endpoint.
   - Required scopes/roles per endpoint (read:list, write:create, admin:delete). Provide a minimal RBAC mapping for frontend features.
   - For cookie approach: SameSite and Secure flags, CSRF protection approach.
   - Whether tokens are rotated and how token refresh is expected from the frontend (silent refresh, refresh endpoint).

6) Rate limiting & abuse protection
   - Per-user and per-IP limits, headers to expose (X-RateLimit-Remaining, Retry-After), 429 behavior.

7) CORS & security headers
   - Allowed origins (production + staging), allowed methods and headers.
   - Required response security headers (Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy).

8) Input validation & injection defenses
   - Validation rules for user-controlled inputs surfaced to frontend.
   - Any fields that contain HTML/markup (should be escaped or sanitized by backend).

9) Caching & sensitive data
   - Which responses are cacheable (Cache-Control headers), which must never be cached.
   - Rules for not returning sensitive tokens/PII in responses.

10) Logging, monitoring, observability
   - If frontend should surface any correlation id (X-Request-ID) or log token.
   - Audit events of interest for security (login, logout, permission changes).

11) Example payloads
   - Provide one minimal and one full JSON example for each success endpoint.
   - Provide one example error JSON per common error case (401, 403, 404, 422, 500).

Security Threat Summary (STRIDE) — quick hits for the feature
- Spoofing: Ensure Authorization header validation, enforce token signature checks. (HIGH)
- Tampering: Validate and canonicalize all inputs. Use parameterized DB queries on backend. (HIGH)
- Repudiation: Return and persist correlation IDs and user IDs in audit logs for actions. (MED)
- Information Disclosure: Avoid returning sensitive fields, PII masking, enforce TLS. (HIGH)
- Denial of Service: Rate limiting & pagination limits to prevent expensive full scans. (MED)
- Elevation of Privilege: Enforce RBAC server-side; never trust client flags. (HIGH)

Minimum Security Acceptance Criteria (must be answered/implemented before frontend proceeds)
- TLS required (HTTPS) for all endpoints. No tokens in URLs.
- Auth method confirmed (Bearer JWT recommended) and Authorization header expected.
- Endpoint-specific required scopes/roles documented.
- Error shape documented and consistent.
- Pagination contract confirmed (cursor vs page) and defaults/limits defined.
- Sensitive fields flagged and redaction policy provided.

Blocking Questions for Marcus (explicit answers needed)
1. Please confirm exact endpoint paths and HTTP methods for all frontend-required operations.
2. Provide canonical success JSON schema + one full example per endpoint.
3. Provide canonical error JSON format and example per status code we should handle (401,403,404,422,500).
4. Confirm pagination strategy and provide param names, defaults, limits, and sample paginated response.
5. Confirm auth approach: Bearer JWT (Authorization header) OR cookies. If JWT: algorithm, expiry, refresh flow, and required scopes per endpoint.
6. Which fields are considered PII/sensitive and must not be surfaced in the UI or logs?
7. CORS: which origins will be allowed for frontend (prod & staging)?
8. Any rate limit headers or behaviors frontend should react to? (e.g., Retry-After semantics)
9. Provide X-Request-ID or correlation id usage contract (header name, whether backend returns one).
10. Are there any server-side validation rules (e.g., max string lengths, allowed characters) we must mirror in the UI to reduce round trips?

What I (Security) did now
- Compiled this security-focused checklist and blocking questions to avoid rework and reduce security risk.

Next step (action for Marcus)
- Answer the 10 blocking questions above and attach example JSON payloads for each endpoint.
- If using JWT, provide a sample token claims payload and the signing algorithm.

If blocked or questions unclear
- I will follow up with a short threat-model doc for any endpoints Marcus marks as HIGH risk.

Contact
- Isabella (Security) — I will review Marcus's responses and sign off on security acceptance criteria.
