Title: Alembic Migration Plan — profile_completed_at & items.category_id

Summary:
This plan covers adding a new nullable column `profile_completed_at` to users and creating a foreign key `category_id` on items. It includes steps for safe rollout, backfill strategy, and verification checks.

Migration files required:
- versions/<timestamp>_add_profile_completed_at.py
- versions/<timestamp>_add_items_category_fk.py

Steps:
1) Add columns as NULLABLE
   - Add migration to add `profile_completed_at` as TIMESTAMP NULLABLE
   - Add migration to add `category_id` as INT NULLABLE with FK to categories(id) (or add constraint after populating values)

2) Deploy application and migration (Phase 1)
   - Run alembic upgrade head in staging
   - Ensure application code handles null values for new columns
   - Run integration tests

3) Backfill data (if needed) — phase 2
   - Run background job to populate `profile_completed_at` for existing users where applicable
   - Populate `items.category_id` based on business rules or default mapping
   - Use batched updates with small transactions to avoid locks

4) Apply NOT NULL constraints (optional) — phase 3
   - After successful backfill and verification, run a migration to set NOT NULL (if required)
   - Monitor for errors and rollback if thresholds exceeded

Verification:
- Count of NULLs < threshold (e.g., 0 for NOT NULL application)
- Integration tests pass
- Spot-check API responses for affected endpoints

Rollback:
- If issues, revert to previous DB state using backups and rollback migrations

Owners:
- Marcus (Backend) — write and run migrations, implement backfill job
- Dana (QA) — validate staging
- Noah (DevOps) — run migrations in production during maintenance window

