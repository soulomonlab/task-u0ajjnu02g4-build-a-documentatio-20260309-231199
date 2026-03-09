CI test dependencies for rate-limit integration tests

Summary
- Tests created: output/tests/test_rate_limit.py (requires pytest and requests)

Recommendation
1) Add a dev requirements file: requirements-dev.txt with pinned versions for reproducibility:
   - pytest==7.4.2
   - requests==2.31.0

2) CI changes:
   - Install dev deps: pip install -r requirements-dev.txt
   - Run tests: python -m pytest output/tests/test_rate_limit.py -q

Rationale / Decisions
- Pinning ensures reproducible CI runs; chosen versions are stable and widely-used as of 2024-06.
- This is reversible: use broader ranges later or adopt Dependabot/renovate for automatic PRs.

Acceptance criteria
- CI runner has pytest and requests available.
- The test command above completes; raw pytest output is pasted to the task.
- Commit: requirements-dev.txt added to repo (or equivalent CI install step documented).

Risks / Notes
- Pinning may delay minor feature updates; recommend monthly dependency checks and automated PRs.
- If the project uses a different test runner or tooling (tox/poetry), adapt commands accordingly.
