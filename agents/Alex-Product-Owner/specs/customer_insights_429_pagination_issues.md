# Feature Bundle: Fix recurring 429 (dry-run) and pagination token TTL issues

**Goal:** Reduce client-facing 429 incidents and retry storms caused by dry-run traffic and short-lived pagination tokens; ensure robust monitoring and runbook for rapid ops response.

**North Star Impact:** Reduce 429 incident rate by 80% and decrease related support tickets by 60% within quarter.

**Context:** See analysis: output/reports/customer_insights_429_pagination_analysis.md (clusters, root causes, KPIs).

---

## Issue 1: Server-side mitigation for high-volume dry-run clients (P1)
**Goal:** Prevent surge of 429s caused by high-frequency dry-run requests by applying targeted server-side throttling and backoff guidance.

**Users:** API clients performing dry-run (integration partners, QA tools). Reduces false positives for rate-limiting and improves stability for normal users.

**RICE Score:** Reach=30,000 requests affected/qtr × Impact=2 (noticeable) × Confidence=70% / Effort=2w = 210
**Kano Category:** Performance / Must-have

**Acceptance Criteria:**
- [ ] Implement server-side detection for dry-run requests (e.g., dry-run header or detect no-op patterns).
- [ ] Apply adaptive throttling for dry-run clients that prevents them from triggering cluster-wide 429s while preserving capacity for production traffic.
- [ ] Emit metrics: dry-run request rate, throttled dry-run count, 429s attributable to dry-run clients.
- [ ] Add a feature flag to enable/disable server-side mitigation for gradual rollout and canary.
- [ ] Integration test that simulates dry-run burst and verifies production traffic unaffected.

**Out of Scope:** Client SDK changes (handled later if needed).

**Success Metrics:** 429s from dry-run client cluster reduced ≥80% in production; no adverse impact on latency for production requests.

---

## Issue 2: Increase pagination token TTL and add resumable pagination (P1)
**Goal:** Reduce repeated pagination requests and retry storms caused by short-lived pagination tokens by increasing TTL and implementing resumable token behavior.

**Users:** Consumers paginating large result sets (end users, integrations). Prevents re-runs from clients when tokens expire mid-collection.

**RICE Score:** Reach=50,000 paginated flows/qtr × Impact=3 (high) × Confidence=70% / Effort=3w = 350
**Kano Category:** Performance

**Acceptance Criteria:**
- [ ] Increase pagination token TTL from current value (documented in analysis) to a proposed new default (e.g., 24 hours) or configurable per-tenant.
- [ ] Implement resumable pagination semantics: if token expired, return a 410 with a resume token or include idempotency/resume hints to allow efficient resume without restarting full query.
- [ ] Update API docs and SDKs (task handed off to Docs/SDK later).
- [ ] Load test showing reduced duplicate queries when token TTL increased; latency impact within SLA.

**Out of Scope:** Migrating historical tokens beyond TTL; client-side SDK updates (follow-up tasks).

**Success Metrics:** Reduction in duplicate pagination requests ≥70%; drop in 429s correlated with pagination flows ≥60%.

---

## Issue 3: Monitoring, runbook, and automated ops playbook for 429 incidents (P2)
**Goal:** Ensure on-call and SRE can detect, diagnose, and mitigate 429 incidents quickly with runbooks and automated mitigation triggers.

**Users:** SRE/On-call, Support (Dana), Product (Alex).

**RICE Score:** Reach=all customers × Impact=2 × Confidence=80% / Effort=1.5w = 213
**Kano Category:** Must-have (for operational reliability)

**Acceptance Criteria:**
- [ ] Create a runbook for 429 incidents covering detection, common root causes (dry-run bursts, pagination TTL), mitigation steps (traffic shaping, feature-flag rollback, cache warming), and comms templates.
- [ ] Implement dashboards/alerts that surface: rising 429 rate (>X%), % of 429s by root-cause tag (dry-run, pagination, other), top client IPs/keys causing 429s.
- [ ] Add automated playbook partials: temporary throttling rules, automated scaling triggers, and a kill-switch to disable the mitigation feature-flag.
- [ ] QA/Dana to validate runbook via a runbook game day (dry-run simulation) and sign-off.

**Out of Scope:** Full automation of remediation without human-in-loop (future enhancement).

**Success Metrics:** Mean time to detect (MTTD) < 5 min; mean time to mitigate (MTTM) < 20 min for 429 incidents.

---

## Implementation notes & constraints
- Prefer server-side mitigations that are reversible via feature flags (low-risk, canary rollout).
- Monitor for false positives: ensure detection heuristics for dry-run do not misclassify production traffic.
- Coordinate TTL increase with cache and storage concerns (token storage duration and GC).

## Next steps recommended
1. Product confirms priority (P1/P2) and accepts scope or requests adjustments.
2. Product creates engineering issues (done below) and assigns primary owner for each.
3. Schedule a grooming session with Marcus to produce implementation plan and canary strategy.
4. Dana/QA to prepare runbook validation plan and game day scenario.

