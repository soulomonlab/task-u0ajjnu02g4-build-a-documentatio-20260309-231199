Situation
- Chris requested confirmation of three technical defaults for the docs PR (rate limit, retry policy, SDK compatibility).

Complication
- Engineering must confirm: whether the rate limit is per-client or per-key; which 5xx errors the retry policy should cover; and whether SDK compatibility range is acceptable given breaking changes.

Mobile team's input & constraints (summary)
1) Rate limit: Mobile prefers per-client (per-device / per-installation) rate-limiting rather than per-key.
   - Rationale: API keys can be shared across devices or proxied by client apps (e.g., for SSO or server-side usage). Per-client limits protect individual users/devices from throttling due to other consumers of the same key and give a better UX for mobile (less cross-device noisy throttling).
   - If backend must use per-key for infra reasons, please state expected collision cases and a fallback strategy (e.g., token bucket per-client on gateway).

2) Retry policy: Mobile recommends applying exponential-backoff retries to idempotent requests (GET, safe PUT/DELETE when server guarantees idempotency) only; avoid automatic retries for non-idempotent POSTs that create resources.
   - Rationale: Automatic retries on POST can cause duplicate resource creation or side effects; mobile apps often operate on poor networks where duplicate detection is non-trivial.
   - Suggested default: exponential backoff starting at 500ms, max 3 total attempts (i.e., initial + 2 retries or initial + 3 attempts? confirm exact counting). Ensure the docs clearly state whether the "max 3 attempts" includes the initial request.
   - Clarify which 5xx codes should trigger retries. Mobile suggests: retry on transient server errors (e.g., 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout). Avoid retrying on 500 Internal Server Error unless backend confirms it indicates a transient condition.

3) SDK compatibility: SDK >=1.2.0 <2.0.0 is OK for mobile provided no breaking changes landed in 1.x before 1.2.0. Mobile request: include brief changelog note in docs listing any behavioral changes in SDK 1.2.0 that affect mobile (auth flows, request/response shapes, retry helpers).

Concrete asks for Marcus (P1, today requested)
- Confirm or propose alternatives for each item above: rate limit (accept 60 req/min and whether that's per-client or per-key), retry policy (accept initial 500ms, max 3 attempts and which 5xx codes), SDK compatibility range acceptance.
- For retry policy: confirm whether "max 3 attempts" counts the initial attempt as 1, and whether retries are applied globally or per-endpoint.
- For rate limit: if per-key is required, provide guidance for mobile mitigations (client-side throttling, exponential backoff, or adaptive sync windows).
- Note any infra/SLO constraints or operational limits that make the defaults infeasible.

Files referenced
- output/reports/docs_values_confirmation.md (Alex/Chris master summary)

Why this matters for Mobile
- UX: mistaken rate-limiting semantics or unclear retry rules lead to poor offline recovery, duplicate actions, and escalations from users.
- Implementation: Mobile will implement client-side backoff, request queuing, and idempotency-safe retries only after engineering clarifies server guarantees.

Next step
- Marcus: please respond today with per-item "Confirm" or an alternate value + one-line rationale. Mobile will wait and implement client behavior accordingly.
