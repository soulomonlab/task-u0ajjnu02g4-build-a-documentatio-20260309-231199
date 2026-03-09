# 409 Conflict Semantics — Confirmed Marcus Decision

Summary decision:
- Default behavior: deduplicate using unique_key when present. If unique_key present and a duplicate exists, return 200 OK with body {"status":"duplicate","existing_id": "<id>"}.
- If unique_key absent, fall back to previous id-based behavior: if client-provided id conflicts with existing id, return 409 Conflict.
- If INGEST_DEDUP_ENABLED=false, system reverts to id-based 409 for all duplicates.

Rationale (short):
- Safer for idempotent clients: unique_key lets retries be idempotent without 409 errors.
- Minimizes ETL complications: ETL can rely on stable unique_key mapping rather than 409s.

Edge cases and notes for ETL:
- ETL should treat 200+status:duplicate responses as successful ingestion and map incoming data to existing_id for downstream joins.
- Logs: include token_id and token_version in ingestion logs for tracing. ETL should capture token_id when present.
- Backfill: when backfilling to reconcile duplicates, use unique_key when available; otherwise, dedupe by content hash.

Open questions for Samantha:
1) Should ETL mark records originally ingested under 409 semantics differently? Recommended: add ingestion_status column with values {ingested, duplicate, conflict}.
2) For analytics relying on total counts, do we want duplicates counted as separate events or collapsed? Recommend collapsed when unique_key present.

