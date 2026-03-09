Ops Runbook — Updates Related to PR

Purpose
Update operational runbooks to include rollout steps, feature-flag instructions, monitoring checks, and rollback steps for the changes introduced by the upstream PR.

Runbook entries (draft)

Prerequisites
- SRE access to production monitoring dashboards and alerting tools.
- Deployment window scheduled (if necessary).
- Confirm whether NEW_FEATURE_FLAG must be toggled per-tenant or globally.

Rollout Steps
1. Deploy service changes to staging and run smoke tests (API health, basic create/read flows).
2. Enable NEW_FEATURE_FLAG in staging and re-run end-to-end tests.
3. Canary deploy to a small percentage of production (e.g., 5%) and monitor error rates and latency for 15 minutes.
4. If no regressions, increase canary to 25% for another 30 minutes, then full rollout.

Monitoring
- Key metrics to watch:
  - 5xx error rate for /api/v1/xyz and /api/v1/abc
  - p95 latency for affected endpoints
  - queue/backlog metrics if async processing involved
- Alerts:
  - >1% 5xx for 15 minutes: Page SRE
  - p95 latency > 2x baseline: Page SRE

Rollback
- Steps to rollback:
  1. Disable NEW_FEATURE_FLAG (if feature-flagged).
  2. Redeploy previous stable revision.
  3. Verify that errors return to baseline and perform sanity checks.

Post-deployment validation
- Run sample create/update flows using the sample scripts in code_samples_python_js.md.
- Confirm created resources are queryable and have expected fields.

Prepared by: Emma (Technical Writer)
