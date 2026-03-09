Purpose

This quick-diff guide highlights the specific lines in the two published KBs where Product should focus review. It maps the exact customer-facing sentences and internal notes that are most likely to need edits.

Files to review (focus points)

1) output/docs/published_kb_429_dry_run_limit.md
   - Headline: "DRY_RUN_LIMIT: Temporary 429 errors during high-volume DRY_RUNs" — confirm headline tone and urgency.
   - Mitigation paragraph: "Workaround: Reduce batch size or retry with exponential backoff." — confirm technical correctness and whether to recommend specific retry intervals.
   - ETA section (if present): "Engineering expects a permanent fix in the next release." — confirm accuracy and whether to include a release window or remove speculative timing.
   - Reference: "See INT-PR-429 for internal tracking." — confirm this matches engineering ticket format.

2) output/docs/published_kb_pagination_migration.md
   - Headline: "Pagination Migration: Behavior changes for result ordering" — confirm tone and whether to flag breaking-change language.
   - Migration steps: "Switch to new cursor-based pagination by calling /v2/list with cursor token." — confirm API path and backward-compatibility notes.
   - Customer impact: "Some legacy clients may observe missing items in paged results." — confirm accuracy and recommended diagnostic steps.
   - Rollback/ETA: "Engineering is rolling this out over the next two weeks." — confirm schedule or remove.

How to provide edits

- Provide exact sentence replacements or approve as-is.
- If you need a release ETA included, provide the exact date or release number to reference.
- If you want Support to notify customers, specify the target segment (e.g., all paying customers, accounts with >1000 requests/day, specific account list).

Time expectation

- ~15 minutes to review if you focus only on the highlighted sentences.

Files created

- output/specs/product_review_quick_diff_guide.md

