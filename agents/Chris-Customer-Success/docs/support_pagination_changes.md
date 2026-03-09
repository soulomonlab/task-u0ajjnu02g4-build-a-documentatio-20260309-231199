# Support Article: Pagination Behavior Changes

Summary
- Recent changes modify pagination behavior in customer-facing APIs: default page size, next-page token semantics, and error handling for invalid tokens.
- This article explains what changed, how it affects integrations, migration steps, and troubleshooting tips for support agents.

Key changes (customer-visible)
- Default page size increased from 20 to 50 when page_size is not specified.
- next_page_token semantics: tokens are now opaque and time-limited (valid for 5 minutes). Attempting to use an expired token returns 400 with error code INVALID_PAGINATION_TOKEN.
- Using an invalid token now returns a clear 400 error instead of silently returning the first page.

When customers notice this
- Unexpectedly larger result sets when they don't set page_size.
- 400 INVALID_PAGINATION_TOKEN errors when clients retry with stale tokens or after timeouts.
- Existing SDK implementations that assumed token permanence may break.

Root causes
- Pagination tokens now encode server-side state and include a timestamp to support stateless backend scaling and re-sharding.
- Default page size change intended to reduce number of API calls for common list operations.

Support troubleshooting steps
1. Verify the API and endpoint version the customer is calling.
2. Ask for request/response examples, timestamps, and next_page_token values.
3. If customer sees larger results, advise explicitly setting page_size to the desired value.
4. For INVALID_PAGINATION_TOKEN:
   - Advise retrying the request without the token to fetch the first page.
   - Recommend refreshing tokens within 5 minutes and implementing retry logic that requests the next page from the last successful response when token errors occur.
5. If SDK-managed pagination broke, ask which SDK/version; check if they are using an outdated SDK that assumes persistent tokens.

Migration guidance for customers
- Update client code to:
  - Explicitly set page_size if deterministic behavior is required.
  - Treat next_page_token as opaque and short-lived. Store tokens only briefly (<=5 minutes).
  - Implement logic: on INVALID_PAGINATION_TOKEN, request the first page or resume from last known state.
- Update integrations and scheduled jobs to fetch pages promptly and avoid long delays between paginated calls.

Developer/Docs tasks
- Update API reference to document new defaults and token TTL.
- Add migration guide snippets showing sample client retry/backoff logic.
- Flag SDKs to implement token refresh helpers and tests for token TTL scenarios.

Acceptance criteria
- Support article published: output/docs/support_pagination_changes.md
- KB includes migration snippets and sample code.
- Tickets created for SDK owners and API docs owners to update references.

Related files
- docs PR follow-up: output/docs/docs_pr_followup.md

