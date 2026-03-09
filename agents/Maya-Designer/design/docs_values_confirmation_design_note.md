Title: Design Note — Docs PR: Confirmation Needed for Technical Defaults

Purpose
- Summarize user-facing impact of the three technical defaults in output/reports/docs_values_confirmation.md and request backend confirmation needed to finalize docs PR.

Context
- Chris (Support) created the request and Alex (Product) asked Engineering to confirm three values so Emma can merge the docs PR.
- Current proposed defaults (from reports/docs_values_confirmation.md):
  • Feature: OFF (default)
  • Rate limit: 60 requests/min
  • Retry policy: retry on 5xx with exponential backoff, initial delay 500ms, max 3 attempts
  • SDK compatibility: >=1.2.0 <2.0.0

Design / User-impact analysis
1) Rate limit (60 req/min)
   - UX impact: affects high-frequency clients (batch jobs, integrations). If enforced per-key, a single misbehaving client could be throttled; if per-client (IP+user), multiple keys from same customer could be aggregated and cause unexpected throttling.
   - Error surface: clients will see 429 responses. Docs must explain scope (per-key vs per-client), expected retry behavior, and suggest client-side rate-limiting guidance.
   - Recommendation: Prefer per-key limits for clearer customer billing/ownership; if infra/SLOs require per-client, call that out explicitly in docs with examples.

2) Retry policy (initial 500ms, max 3 attempts) on 5xx
   - UX impact: retries can mask transient server errors for clients and reduce error noise, but can amplify load spikes during partial outages.
   - Which 5xx to include matters: 500, 502, 503, 504 are common transient cases; 501 (Not Implemented) and 505 (HTTP Version Not Supported) are not transient and should not be retried.
   - Recommendation: Retry only on 500, 502, 503, 504. Document that retries are client-driven with exponential backoff and a cap to avoid request storms.

3) SDK compatibility (>=1.2.0 <2.0.0)
   - UX impact: SDK users outside supported range may encounter breaking changes or unsupported features. Docs should explain compatibility matrix and provide migration notes if major versions change.
   - Recommendation: Confirm minimum supported stable SDK (>=1.2.0) and clearly call out that 2.0.0 is a breaking change.

Acceptance Criteria for Docs
- Engineering confirms and provides the exact wording for docs for these elements:
  A) Rate limit numeric value and scope: per-key or per-client
  B) Retry policy: accept default OR provide alternate values; specify which 5xx codes will be retried and rationale
  C) SDK compatibility: confirm supported version range
- Any infra / SLO constraints or concerns that should be surfaced to product/docs.

Questions for Marcus (please answer inline below or update this file)
1) Rate limit: Do you accept 60 req/min? Is this enforced per-key or per-client? Any exceptions (admin keys, internal integrations)?
2) Retry policy: Do you accept initial 500ms, max 3 attempts? Which 5xx codes should clients retry on (recommend: 500, 502, 503, 504)? Any additional constraints (circuit breaker, server-driven Retry-After handling)?
3) SDK compatibility: Accept >=1.2.0 <2.0.0? Any known SDK versions with issues we should call out?

Suggested doc text snippets (to speed Emma)
- Rate limiting: "Requests are limited to 60 requests per minute per API key. Exceeding this limit returns HTTP 429. We recommend implementing client-side rate limiting and exponential backoff to handle throttling."
- Retry guidance: "Clients may retry on transient server errors (HTTP 500, 502, 503, 504) using exponential backoff. Start with an initial delay of 500ms and up to 3 attempts. Do not retry on 4xx errors or non-transient 5xx (e.g., 501)."
- SDK compatibility: "We support SDK versions >=1.2.0 and <2.0.0. Versions 2.0.0 and above may include breaking changes; please consult the SDK changelog for migration steps."

Next steps / timeline
- Engineering (Marcus) to confirm the three items (A/B/C) and provide exact wording where applicable. Priority: P1 — please respond today so Emma can merge docs PR.

File location: output/design/docs_values_confirmation_design_note.md
