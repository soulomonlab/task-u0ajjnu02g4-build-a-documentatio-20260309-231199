# Ops Runbook — CustomerInsights Follow-up

Purpose

This runbook documents deployment, monitoring, rollback, and on-call escalations for the CustomerInsights feature changes.

Prerequisites

- Deployment user has permissions to the insights service
- Datadog and Prometheus access for the service

Deployment steps

1. Merge PR into main and tag release: git tag -a vX.Y.Z -m "CustomerInsights follow-up"
2. CI will build and push the docker image to registry
3. Deploy to staging: kubectl set image deployment/insights insights=registry/example:vX.Y.Z -n staging
4. Smoke test: run sample queries in staging using the provided code samples

Rollback steps

1. If post-deploy errors occur, rollback to previous image: kubectl set image deployment/insights insights=registry/example:vX.Y.Z-1 -n staging
2. Notify on-call and open incident in PagerDuty

Monitoring (Datadog)

- Query latency (p95) — datadog query: avg:trace.http.request.duration{service:insights}.rollup(95)
- Error rate — datadog query: sum:trace.http.request.errors{service:insights}.as_count()
- Rate limiting alerts for 429 responses

On-call escalation

- 1st: Service owner (Marcus) — pagerduty
- 2nd: Backend tech lead (Taylor)
- 3rd: SRE (Noah)

Contacts

- Marcus (Backend)
- Taylor (Tech Lead)
- Noah (DevOps)
