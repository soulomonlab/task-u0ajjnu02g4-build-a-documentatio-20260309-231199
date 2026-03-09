Summary (Conclusion)
- Approved with adjustments: rate limit = 60 req/min per API key (with a small burst allowance); retry policy = exponential backoff starting at 500ms, max 3 attempts total, but only for specific transient 5xx (502, 503, 504) and for idempotent requests (or when client provides idempotency-key for non-idempotent requests); SDK compatibility >=1.2.0 <2.0.0 accepted.

Decisions (one-line each)
1) Rate limit
- Decision: APPROVE 60 requests/minute as the default enforcement unit = per-API-key (not per-client IP).
- Rationale: API-key enforcement is unambiguous, aligns with billing/auth model, and avoids IP spoofing or NAT ambiguity. Per-key allows us to grant exceptions for internal/partner keys.
- Operational details: Token-bucket style with a burst of up to 10 requests. On limit breach: HTTP 429 + Retry-After header (seconds rounded up). Enforcement implemented in Redis (clustered, local TTL counters) at the gateway/load-balancer layer.
- Exceptions: Internal privileged keys (admin/partner) can be whitelisted with higher limits; documented on the key management page.

2) Retry policy
- Decision: PARTIAL APPROVAL. Keep base: exponential backoff starting 500ms, max 3 total attempts (initial + 2 retries) but restrict when retries apply.
- Which 5xx to retry: only 502 (Bad Gateway), 503 (Service Unavailable), 504 (Gateway Timeout). Do NOT auto-retry on 500 (Internal Server Error) or application-specific 5xx unless the response includes a Retry-After header or explicit transient flag.
- Idempotency: Only automatically retry idempotent methods (GET, HEAD, PUT, DELETE). For POST (non-idempotent), require an Idempotency-Key header; if present, safe to retry up to the same limit.
- Jitter: Add randomized jitter to backoff to avoid thundering herd (e.g., base*2^(n-1) +/- 0-200ms).
- Client guidance to docs: Clarify "max 3 attempts" = total attempts including the initial request. Suggest clients implement exponential backoff + jitter and honor Retry-After.

3) SDK compatibility
- Decision: APPROVE SDK constraint >=1.2.0 <2.0.0.
- Rationale: We guarantee backward-compatible minor releases; major versions may include breaking changes. We'll document breaking-change policy and add server-side feature flags for gradual rollouts.

SLO/Infra notes & constraints
- Performance targets remain: p95 < 100ms, p99 < 200ms. Rate-limit checks implemented in Redis per-key will add ~1-3ms overhead for hit/miss; acceptable under current SLO.
- Rolling enforcement: start with soft-limits in 2-week canary mode (log-but-not-block) for a subset of keys to validate traffic patterns before enforced 429s.
- Monitoring: create metrics for rate_limit.allowed, rate_limit.blocked, retry.attempts, retry.success_after_retry, and alerts if blocked rate > 0.1% of requests or if retry success rate < 70%.

Acceptance criteria for docs PR
- Docs state: "Rate limit: 60 req/min per API key (burst 10). 429 + Retry-After on breach."
- Docs state: "Retry: exponential backoff starting 500ms, max 3 total attempts, only on 502/503/504 (and 500 only with Retry-After or transient flag). Retries only for idempotent methods or when client provides Idempotency-Key for non-idempotent methods. Include jitter." 
- Docs state: "SDK compatibility: >=1.2.0 <2.0.0" and link to versioning policy.

Open questions / follow-ups (recommend short entries in docs)
- Clarify which API key classes are considered "privileged" and the process to request higher limits.
- Document the canary rollout schedule for enforcement (recommended: 2 weeks soft-enforce then enable blocking).

Contact & next steps
- I implemented these decisions for docs reference in this file. For runtime rollout, engineering will (1) add Redis-based counters at the gateway, (2) instrument metrics/alerts, (3) run a 2-week soft-enforcement canary, then enable hard 429 enforcement.

Files created
- output/reports/docs_values_confirmation_marcus_response.md
