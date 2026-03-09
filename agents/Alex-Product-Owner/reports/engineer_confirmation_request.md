Confirmed by Alex: 2026-03-09

---

Summary of Alex confirmations (per-item)

1) Decision 1 — DB schema migration strategy
- Confirmed decision: Follow the recommended online, backwards-compatible migration using expand-then-contract with feature flags (no downtime).
- Reason: Minimizes user impact and aligns with our scalability goal; reversible if issues appear.
- Migration notes: Add new columns nullable, backfill in background job, switch reads to new columns behind a feature flag, then drop old columns in a later release. Ensure migration jobs are idempotent and rate-limited; schedule during low-traffic windows and monitor replication lag.

2) Decision 2 — User identifier change (legacy -> new format)
- Confirmed decision: Keep legacy IDs in place; introduce new canonical_id column and populate via a background migration.
- Reason: Preserves backward compatibility for integrations and avoids immediate breaking changes.
- Migration notes: Add canonical_id nullable, run background backfill with batching, update API layer to prefer canonical_id while falling back to legacy_id, publish migration deprecation timeline in release notes (e.g., 6 months).

3) Decision 3 — Cache invalidation approach
- Confirmed decision: Use event-driven invalidation (publish-subscribe) for strong correctness; use short TTL as a fallback for missed events.
- Reason: Ensures cache consistency across scaled services and supports near-real-time updates.
- Migration notes: Instrument events for all write paths, add consumer with idempotency and retry, deploy consumer before switching producers; monitor cache hit ratio and error rates.

4) Decision 4 — Blob/file storage choice
- Confirmed decision: Use S3-compatible object storage with server-side encryption and versioning enabled.
- Reason: Scales with minimal operational burden and meets durability/security needs.
- Migration notes: Implement dual-write for a transition period (local -> S3), backfill existing files to S3 in batches, update signed URL generation, and decommission local storage after verification.

---

(Original engineer_confirmation_request contents from Chris retained below.)

[Original summary of questions and recommended choices]

# NOTE: The original report content is unchanged below this line. Marcus, please add your confirmation line(s) at the top in the same format: 'Confirmed by Marcus: YYYY-MM-DD' and include any dissenting decision, reason, or migration notes if you disagree with any item.
