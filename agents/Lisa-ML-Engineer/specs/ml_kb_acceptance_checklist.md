ML-specific KB Acceptance Checklist

Purpose: Supplement the existing product_review_acceptance_checklist.md with checks QA should run for KBs that reference or document ML/AI features.

Checklist items (QA actions):
1. Model references
   - Does the KB explicitly mention a model name, version, or configuration? If yes, record these details.
2. Reproducibility & examples
   - Are example inputs/outputs provided? Verify at least 5 example inputs produce the documented outputs when run against the current model (or a mock if model unavailable).
3. Metrics & claims
   - Any performance claims (accuracy, F1, precision, recall)? Verify source of the claim (link to eval or benchmark) and note whether it matches latest model metrics.
4. Privacy / PII
   - Check for any example or training data that may contain PII. Flag content that includes personal data or could be sensitive.
5. Failure modes & guidance
   - Does the KB document known failure modes, confidence thresholds, or safe-fallback behaviour? If absent for P0 ML features, mark as "missing".
6. Monitoring & rollback hooks
   - Verify KB references monitoring dashboards or alerting (if applicable). If none, note potential gap for production ML-backed features.
7. API / integration details
   - If KB gives API examples, validate endpoint names, parameter names, and expected response formats against the current API spec (if available).
8. User-facing disclaimers
   - Ensure that limitations, expected latency, and update cadence are disclosed for ML features.
9. Security & abuse
   - Flag any content that could enable abuse (e.g., prompts that encourage misuse) and escalate to Security if present.
10. Acceptance decision
   - For each KB, QA should append: Approve / Request edits + short rationale referencing checklist items above.

Notes for QA: attach any reproducer scripts, test inputs, and screenshots to the product_review record. If model access is blocked, mark tests as "blocked by model access" and notify #ai-data (#Samantha) and #ai-backend (#Marcus).
