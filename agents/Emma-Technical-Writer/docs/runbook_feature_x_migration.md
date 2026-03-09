Runbook: Feature X Migration

Purpose
- Steps to deploy database migration and enable Feature X safely in production.

Prerequisites
- Migration tested in staging and approved by Marcus.
- Maintenance window scheduled during low traffic.
- Backup: take DB snapshot before migration.
- Feature flag capability available to roll out incrementally.

High-level steps
1) Prepare
  - Notify stakeholders and schedule maintenance window.
  - Ensure deployment target branch is ready and passes CI.
2) Backup
  - Take full DB snapshot and verify integrity.
3) Apply migration
  - Add column `feature_x_enabled` to `features` table (nullable, default=false).
  - Backfill: set `feature_x_enabled`=false for existing rows.
  - Add index if necessary for query performance.
4) Deploy application code
  - Deploy service that contains POST /v1/feature-x/activate and GET /v1/feature-x/status.
5) Post-deploy validation
  - Call GET /v1/feature-x/status for a sample tenant and verify 200 and expected schema.
  - Run smoke tests: activation flow via POST then GET should return activated state.
6) Rollout
  - Toggle feature flag for a small % of users, monitor metrics and errors for 30 minutes, then increase.
7) Rollback
  - If activation fails or data corruption is detected, roll back application to previous version and restore DB snapshot.

Monitoring & Alerts
- Watch error rates, 5xxs, and any increase in latency for feature-x endpoints.
- Alert if POST /v1/feature-x/activate returns >5% 4xx/5xx in 15m window.

Post-migration
- Remove `nullable` allowances if desired after monitoring period.
- Update documentation links and notify support.

Owners
- Migration owner: Noah (#ai-devops)
- Backend reviewer: Marcus (#ai-backend)
- Docs owner: Emma (#ai-docs)

