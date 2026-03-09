import os
import pytest

# Tests to verify readiness to run the Product Review acceptance checklist for Task #173.
# These tests assert presence of key artifacts that Product (Alex) must produce before QA can run the checklist.

BASE_SPECS = os.path.join("output", "specs")
RESPONSE_FILE = os.path.join(BASE_SPECS, "product_review_response_task_173.md")
CHECKLIST_FILE = os.path.join(BASE_SPECS, "product_review_acceptance_checklist.md")
REQUEST_FOR_KBS = os.path.join(BASE_SPECS, "product_review_request_for_published_kbs.md")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_product_review_response_exists():
    """Product review response file must exist.

    QA cannot proceed until Product publishes their Approve/Request edits decisions.
    """
    assert os.path.exists(RESPONSE_FILE), (
        f"Blocked: missing product review response file: {RESPONSE_FILE}"
    )


def test_acceptance_checklist_exists():
    """Acceptance checklist must be present for QA to execute.
    """
    assert os.path.exists(CHECKLIST_FILE), (
        f"Missing acceptance checklist: {CHECKLIST_FILE}"
    )


def test_product_review_includes_post_review_handoff():
    """Product response file should state that Product will complete review and then QA will run the checklist.

    This verifies Product acknowledged the QA step and that QA is the next owner.
    """
    content = read(RESPONSE_FILE)
    assert (
        "After I complete my review" in content or "After I complete the review" in content
    ), (
        "Product response file does not include an explicit post-review handoff to QA."
    )


def test_request_for_published_kbs_included():
    """There must be a supporting file listing the published KBs (URLs or INT refs) for QA to validate.

    If this file is missing we cannot run the checklist.
    """
    assert os.path.exists(REQUEST_FOR_KBS), (
        f"Blocked: product must provide published KBs list/file: {REQUEST_FOR_KBS}"
    )
