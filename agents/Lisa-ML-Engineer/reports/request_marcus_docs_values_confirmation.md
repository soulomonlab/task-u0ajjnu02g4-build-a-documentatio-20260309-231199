Title: Confirmation request for docs values (Rate limit / Retry policy / SDK compatibility)

Conclusion (short)
- Please confirm or provide alternatives (with brief rationale) for the three values Chris/Alex proposed for the docs PR: rate limit, retry policy, and SDK compatibility. Deadline: today (P1).

Context
- Source: output/reports/docs_values_confirmation.md (prepared by Alex/Chris).
- Proposed defaults to confirm:
  A) Feature default: OFF (docs note) — informational only.
  B) Rate limit: 60 requests per minute.
  C) Retry policy: retry on 5xx with exponential backoff starting at 500 ms, max 3 attempts.
  D) SDK compatibility: >=1.2.0 and <2.0.0.

What we need from Marcus (MECE)
1) Rate limit (B)
   - Confirm (Yes/No). If No, provide an alternative numeric value.
   - Specify scope: per-client (per account/user) OR per-key (per API key). If you prefer per-endpoint or hybrid, state that.
   - Any infra/SLO constraints or burst handling notes we must document (e.g., hard quota vs token-bucket bursts, expected p95 latency under this load).

2) Retry policy (C)
   - Confirm (Yes/No). If No, provide alternative backoff/attempts.
   - Clarify which 5xx codes the policy should apply to. Suggested default to consider: only on 502, 503, 504 (transient gateway/service unavailable), NOT on 500 or 501 (application errors/unsupported) unless we have extra context.
   - Confirm whether retries should be limited to idempotent methods (GET/HEAD/PUT/DELETE) or allowed for POST as well.
   - Note any server-side guidance to clients (Retry-After header use, jitter recommended).

3) SDK compatibility (D)
   - Confirm (Yes/No). If No, propose min and max supported versions and brief rationale (breaking changes, security fixes, testing status).
   - Any known incompatibilities in >=1.2.0 <2.0.0 that should be documented as caveats?

Response format requested
- For each item (B/C/D) reply with one line: "Confirm" OR "Alternative: <value> — <1-line rationale>".
- If you need more data to decide (e.g., infra capacity numbers), state exactly which metric and I will fetch it (or tag Noah/Samantha as needed).

Priority and timing
- Priority: P1. Please reply today so we can finalize the docs PR.

Acceptance criteria for docs
- All three items confirmed or replaced with alternative + rationale.
- If alternative affects API behavior (rate-limiting scope or retryable codes), include notes we can paste into the docs (2-3 lines).

Prepared by
- Lisa (ML/AI Engineer) — facilitating the engineering confirmation step for docs.
