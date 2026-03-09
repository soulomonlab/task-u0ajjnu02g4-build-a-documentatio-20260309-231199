# New/Changed Environment Variables

This document lists environment variables introduced or changed by the backend PR that Samantha needs to implement ETL patches and tests.

Required new env vars:
- INGEST_DEDUP_ENABLED (boolean, default=true)
  - Enables server-side deduplication using unique_key. If false, server falls back to id-based conflict behavior (409 on duplicates).
- INGEST_DEDUP_STRATEGY (string, values: "unique_key", "id")
  - How deduplication is evaluated. "unique_key" preferred.
- TOKEN_ROTATION_ENABLED (boolean, default=true)
  - Enables token rotation metadata validation and token_id tracking.
- TOKEN_ISSUER (string)
  - Logical issuer id included in token metadata for auditing.
- LIST_PAGINATION_MODE (string, values: "page", "cursor", default="cursor")
  - Determines the list response format returned by API. ETL must handle both until migration complete.
- PAGINATION_DEFAULT_PAGE_SIZE (integer, default=50)
- PAGINATION_MAX_PAGE_SIZE (integer, default=1000)

Optional / diagnostic env vars:
- INGEST_DEDUP_TTL_SECONDS (integer, default=86400)
  - TTL for deduplication keys stored in Redis when using unique_key strategy.
- TOKEN_METADATA_STRICT (boolean, default=false)
  - If true, reject requests without token.token_id/token_version.

Notes:
- Backwards compatibility: when INGEST_DEDUP_ENABLED=false and LIST_PAGINATION_MODE=page, behavior approximates v1.
- Samantha should instrument ETL to read TOKEN_ROTATION_ENABLED and INGEST_DEDUP_ENABLED to decide whether to expect token metadata and unique_key fields.
