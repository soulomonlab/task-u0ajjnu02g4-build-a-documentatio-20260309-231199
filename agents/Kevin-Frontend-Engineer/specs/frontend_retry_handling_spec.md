Frontend Retry Handling Spec

Purpose
- Define how the frontend should handle API rate-limiting (429) and DRY_RUN_LIMIT errors, and what UX feedback to show users.

Scope
- Single-page React app components that call backend endpoints via apiFetch (output/code/useApiRetry.ts)
- Patterns for: retrying (with backoff), surfacing non-retryable errors with clear user guidance and links to Support KBs.

Requirements
1) Retry behavior
  - For 429 and 5xx responses, automatically retry with exponential backoff.
  - Observe Retry-After header when present.
  - Max retries = 4 (configurable per-call).
  - Base delay = 300ms.

2) DRY_RUN_LIMIT handling
  - DRY_RUN_LIMIT responses should NOT be automatically retried.
  - UI should show a dismissible banner with:
     - Short explanation: "Too many dry-run requests. Please try again later or contact support." 
     - Link to KB: placeholder (to be filled by Support): <KB_DRY_RUN_LIMIT_URL>
     - A secondary action to open Support contact modal.

3) 429 handling UX
  - If transient (single retry succeeds), show no error.
  - If after all retries the request still fails with 429, show a banner:
     - Message: "Request rate limit reached. Please wait a few minutes."
     - Link to KB: <KB_429_URL>

4) Pagination migration handling
  - When encountering responses that indicate pagination migration problems (e.g., missing total_count, changed page tokens), surface a contextual inline warning near the list or table with guidance and KB link: <KB_PAGINATION_MIGRATION_URL>

5) Telemetry
  - Frontend should log events for: retry attempted, final failure (429), DRY_RUN_LIMIT encountered, pagination migration detected.
  - Event payloads: endpoint, status, error_code, attempt_count, timestamp.

6) Tests
  - Unit tests for apiFetch: simulate 429 with Retry-After, simulate DRY_RUN_LIMIT payload, simulate 500 responses.
  - Component tests: banner appears for non-retryable DRY_RUN_LIMIT and after max retries for 429.

Next steps
- #ai-support: provide published KB URLs to replace placeholders.
- #ai-qa: write QA test cases based on the tests section.

