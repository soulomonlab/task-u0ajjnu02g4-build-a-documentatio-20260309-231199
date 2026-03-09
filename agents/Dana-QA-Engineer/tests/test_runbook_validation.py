import os
import re

DOC_FILES = [
    "output/docs/support_429_dry_run_limit.md",
    "output/docs/support_pagination_changes.md",
    "output/docs/kb_triage_assignment.md",
]

NUMERIC_PATTERN = re.compile(r"\b(\d{1,6})(s|m|h|d|%|\b)")
KEYWORDS = ["threshold", "limit", "quota", "TTL", "ttl", "alert", "env", "environment", "ENV_"]


def test_doc_files_exist():
    missing = [p for p in DOC_FILES if not os.path.exists(p)]
    assert not missing, f"Missing expected doc files: {missing}"


def _file_contains_keyword(path, keywords):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    for kw in keywords:
        if kw in text:
            return True
    return False


def test_dry_run_doc_has_threshold_or_limit():
    path = DOC_FILES[0]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert any(k.lower() in text.lower() for k in ["limit", "threshold", "quota"]), \
        "Dry-run doc should document a limit/threshold/quota"
    # also check for a numeric value near those words
    assert NUMERIC_PATTERN.search(text), "No numeric value (e.g. '1000', '10m') found in dry-run doc"


def test_pagination_doc_has_ttl_and_token_behavior():
    path = DOC_FILES[1]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert any(k.lower() in text.lower() for k in ["ttl", "token", "pagination"]), \
        "Pagination doc should describe TTL/token behavior"
    assert NUMERIC_PATTERN.search(text), "No TTL duration found in pagination doc"


def test_env_vars_documented_somewhere():
    found = False
    for path in DOC_FILES:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if "ENV_" in text or "environment variable" in text.lower() or "env var" in text.lower():
            found = True
            break
    assert found, "No environment variable documentation found in support docs"
