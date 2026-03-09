KB ML Engineering Note — Lisa (ML/AI Engineer)

Purpose
- Provide ML-specific ETA, owner contact, rollback plan, user-visible behavior changes, and data impact details for the KB engineering request (see output/specs/kb_engineering_request_marcus.md).

Summary conclusion (TL;DR)
- ML deliverable: prototype + integration-ready model for KB re-ranking and confidence scoring.
- Estimated end-to-end time: 5 business days (see breakdown below).
- Owner: Lisa (ML/AI Engineer) — lisa@company.com; Slack: @lisa-ml.
- Rollback: versioned model + blue-green/canary deployment; immediate cutback to previous model possible.
- Data impact: need telemetry events, one DB migration (kb_model_version, kb_relevance_score), and an offline backfill for historical scores.

1) ML scope & approach
- Task: KB re-ranking + result confidence scoring. Model type: lightweight cross-encoder fine-tune (Transformer-based) or distilled bi-encoder + cross-encoder rescoring depending on latency need.
- Recommendation: start with distilled cross-encoder (balanced accuracy & latency). Training/fine-tune on labeled query->KB relevance pairs.
- Metrics to validate: Precision@1 (>90% target), MRR, NDCG@5, inference latency p95 <50ms.

2) ETA (end-to-end) — 5 business days (breakdown)
- Day 0–1: Confirm data, label set availability, and run quick EDA with Samantha's dataset (needed: sample size, label distribution).
- Day 1–2: Prototype training (fine-tune distilled model) + offline eval (expected training <=4 hours on a single GPU for 5–10k labeled pairs).
- Day 3: Integration work: wrap model in prediction interface (nginx/Bento-like artifact) and log telemetry hooks.
- Day 4: Internal validation, A/B or shadow runs on recent traffic; generate metrics dashboard and smoke tests.
- Day 5: Canary rollout + monitoring setup and finalize rollout plan with Marcus/Noah.

If dependencies (data/infra) are delayed, slip up to +3 business days.

3) Owner & contacts
- ML owner: Lisa (ML/AI Engineer) — lisa@company.com; Slack: @lisa-ml. I'll own model training, evaluation, MLflow tracking, and the model artifact.
- Backend owner (required): Marcus — needs to own API wiring, DB migrations, and rollout orchestration.
- Infra owner: Noah — for canary/traffic routing and production deployment (coordination required).

4) Rollback plan (reversible, automated)
- Model versioning: every model saved to MLflow with model_version tag.
- Blue-green / Canary approach:
  - Step 1: Deploy new model as vNew alongside vCurrent in shadow mode (0% traffic), collect metrics for 48h.
  - Step 2: Canary: route 5% of traffic to vNew for 2–4 hours; monitor Precision@1, latency, error rate, CTR.
  - Step 3: If metrics within thresholds, escalate to 20% → 50% → 100% with monitoring windows.
- Automated rollback triggers:
  - Precision@1 drops >5% relative to baseline OR
  - CTR of KB results drops >3 percentage points absolute OR
  - Latency p95 >100ms OR error rate spike >1%
- Execution: Marcus/Noah should provide traffic routing toggle and a one-click switch to previous model; ML will provide command to point serving layer to previous MLflow model URI.

5) User-visible behavior changes
- Primary visible change: KB result ordering will change (some users will see different top result for the same query).
- Secondary: confidence badges for KB answers (e.g., High / Medium / Low) may appear near results if product opts in.
- Expected user impact: improved top-1 relevance for targeted queries; occasional reordering for long-tail queries.
- Messaging recommendation (for Product): Notify users with a short tooltip: "Search results improved — we're experimenting with smarter ranking to surface a more relevant KB article." (see request file for copy edits)

6) Data / DB changes and telemetry (detailed)
- Telemetry events required (server-side):
  - kb_query_submitted {user_id, query_text, timestamp}
  - kb_results_served {request_id, model_version, candidate_ids[], ranked_ids[], relevance_scores[], latency_ms}
  - kb_result_clicked {request_id, clicked_id, rank, click_timestamp}
  - kb_feedback_submitted {request_id, feedback_type (up/down), comment}
- DB migration proposals:
  - Table: kb_interactions (existing) — add columns:
    - kb_model_version VARCHAR(64) NULL
    - kb_relevance_score FLOAT NULL
  - Rationale: persist model version and score to enable historical analysis and rollback comparisons.
- Backfill:
  - Backfill script to compute kb_relevance_score for historical rows (recommended window: last 3 months) — offline batch job, can be run as Spark/Pandas job.
  - Estimated runtime: depends on data volume. Example: 1M interactions => ~1–2 hours on a multi-core worker. Provide resources if faster turnaround required.
- Data retention & privacy: use hashed user_id and follow existing retention policy.

7) Monitoring & alerting
- Dashboards (Grafana / Looker): precision@1, MRR, CTR on KB results, latency p50/p95/p99, error rate, model_version rollouts.
- Drift detection: daily histogram comparison for query tokens and top-k score distributions; alert if KS-test p-value < 0.01 or score mean shifts >10%.
- Retrain triggers: automatic retrain suggested if production Precision@1 degrades >5% for 7-day rolling window.

8) Acceptance criteria (for Product sign-off)
- Offline: Precision@1 on validation set >= target (e.g., +5% improvement over baseline) and no significant latency regressions.
- Shadow/Canary: No drop in CTR or increase in support tickets related to wrong KB answers after 48h shadow and 5% canary windows.
- Performance: inference p95 <50ms.

9) Dependencies / Open questions for Marcus & Samantha
- Samantha (#ai-data): confirm availability of labeled query->KB pairs (min recommended 5k labeled pairs) and access path to recent interaction logs.
- Marcus (#ai-backend): confirm the following APIs and infra capabilities:
  - API endpoint for KB ranking (suggested: POST /api/v1/kb/rank) and expected request/response shape.
  - Ability to add columns to kb_interactions and run reversible DB migration + run backfill as a job.
  - Support for canary traffic routing (5%→20%→100%) or feature-flag control.
  - Expected SLA for model-serving latency and how to toggle model version quickly.

10) Deliverables I will produce
- output/code/ml/train_kb_ranker.py (training & evaluation script, MLflow logging)
- MLflow model artifact + model card (with run_id)
- Monitoring script: output/code/ml/monitoring/drift_detector.py
- Backfill script: output/code/ml/backfill/scores_backfill.py
- Integration notes + inference contract (JSON schema) to hand to Marcus

Next steps (action items)
- Marcus: please confirm ETA for backend tasks (DB migration window, API wiring, canary support) and whether you can own rollback orchestration.
- Samantha: confirm labeled dataset availability and sample size.

