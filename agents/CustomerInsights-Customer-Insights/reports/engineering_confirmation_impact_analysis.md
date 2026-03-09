Title: Impact Analysis & Recommended Defaults — Engineering Confirmation Request

Context
- Docs PR blocked pending engineering confirmation on four canonical behaviors: widget.size, metadata schema, status/soft-delete semantics, and WIDGETS_CACHE_TTL.
- Delay in merging docs slows downstream onboarding, support triage, and frontend/back-end alignment.

Purpose
- Explain customer and product impact of each undecided item.
- Recommend temporary (reversible) defaults to unblock the docs PR and engineering work.
- Specify acceptance criteria and owners for final confirmation.

Summary of items, impact, and recommended defaults

1) widget.size (canonical behavior)
- Customer impact if unspecified: UI inconsistency across products, broken layout for integrations, increased support tickets for display bugs.
- Recommended default (temporary): Define widget.size as a fixed enum: [SMALL, MEDIUM, LARGE] with explicit px mapping (SMALL=240px, MEDIUM=480px, LARGE=768px). Frontend should accept both enum and numeric px in an advanced field for backward compatibility.
- Acceptance criteria: Frontend renders correctly for all three sizes; existing integrations using numeric px continue to work; docs include explicit mapping table and examples.
- Owner: Marcus (engineering) to confirm behavior and ensure backend validation; Alex to confirm product UX expectations.

2) metadata schema
- Customer impact if unspecified: inconsistent metadata across widgets (missing fields, conflicting types), downstream parsing errors in analytics and SDKs, increased integration friction.
- Recommended default (temporary): Canonical metadata is a JSON object with optional 'title' (string), 'description' (string), 'tags' (array of strings), 'version' (semver string), and a freeform 'extras' object for extensions. All fields documented and strictly typed where possible.
- Acceptance criteria: API validation accepts the schema; SDKs surface typed fields; docs include example payloads and guidance for 'extras'.
- Owner: Marcus to implement schema validation; Alex to confirm mandatory vs optional fields.

3) status / soft-delete semantics
- Customer impact if unspecified: unclear lifecycle leading to data-visibility bugs, inability for support to restore content, inconsistent retention behavior across UIs.
- Recommended default (temporary): Use a status enum: [ACTIVE, ARCHIVED, DELETED]. DELETED is soft-delete (retained for 30 days by default) with an audit log entry and a retention TTL before physical deletion. ARCHIVED = hidden from default listings but recoverable indefinitely.
- Acceptance criteria: APIs expose status in responses; delete endpoints set status=DELETED and return restoration endpoint; docs explain retention defaults and admin overrides.
- Owner: Marcus to implement; Alex to confirm retention duration (default 30 days) or change.

4) WIDGETS_CACHE_TTL
- Customer impact if unspecified: unpredictable caching causing stale widgets or excessive load; performance regressions impacting large deployments.
- Recommended default (temporary): Default WIDGETS_CACHE_TTL = 300 seconds (5 minutes). Env var override allowed (WIDGETS_CACHE_TTL seconds). Cache invalidation: update events should invalidate relevant keys.
- Acceptance criteria: Cache TTL configurable via env; cache invalidation mechanism documented and demonstrated in tests; performance baseline unchanged for typical load.
- Owner: Marcus (implementation) + Ops to document env var; Alex to confirm if 5 minutes meets product expectations.

Trade-offs and rationale (one line each)
- Enum widget sizes increase predictability for designers and QA; numeric px keeps backward compatibility.
- Typed metadata reduces integration errors at minimal overhead; 'extras' preserves extensibility.
- Soft-delete with a 30-day retention balances recoverability vs storage cost; can be changed later via config.
- 5-minute cache TTL balances freshness and load; teams can tune per deployment.

Recommended decision path (to unblock docs PR)
1. Alex (Product) confirms or overrides product-facing defaults (widget.size enum mapping, mandatory metadata fields, retention duration, cache TTL) within 2 business days.
2. If Alex does not respond in 2 business days, the temporary defaults listed here should be used to finalize the docs PR and unblock engineering. These defaults are reversible.
3. Marcus implements validation + behaviors and informs Docs owner to finish the PR.

Next steps (for the approver)
- Review this analysis and either approve the defaults or specify changes.
- Confirm ownership and timelines for implementation.

Appendix: Quick decision checklist for confirmations (one-line answers expected)
- widget.size mapping approved? (Y/n — if n, provide mapping)
- metadata schema approved (fields mandatory/optional)? (Y/n — if n, specify)
- retention for DELETED soft-delete (default 30 days)? (Y/n — if n, specify)
- WIDGETS_CACHE_TTL default 300s? (Y/n — if n, specify)

Document author: Customer Insights Agent
Date: 2026-03-09
