# Docs PR Changes — Follow-up Summary

Source: output/reports/docs_update_from_pr_summary.md

Summary of doc changes created to resolve PR ambiguities and environment notes.

Files to update in docs PR
1) output/docs/api_reference.md
   - Replace ambiguous widget examples with confirmed JSON from engineering
2) output/docs/runbook_ops.md
   - Add environment variable requirement: WIDGETS_CACHE_TTL (confirm default and units)
3) output/docs/release_notes/vX.Y.Z.md
   - Note changed API behaviors and migration steps if `size` type changed

Concrete changes made in this follow-up branch
- Created: output/docs/api_examples_update.md (proposed examples & engineering questions)
- Created: output/docs/docs_pr_changes_summary.md (this file)

Engineering questions to resolve (need Marcus/Alex):
- `size` type for widget endpoints (enum string vs integer)
- `metadata` allowed schema
- `status` enum and soft-delete behavior
- Environment variable: WIDGETS_CACHE_TTL — required? default? units?

Acceptance criteria for merging docs PR:
- All API examples match engineering-confirmed responses
- Runbook includes accurate environment variable definitions and example values
- Release notes mention any breaking changes and migration steps

Next steps:
- Request engineering confirmation on questions above
- Update primary API reference and runbook files, then open docs PR
