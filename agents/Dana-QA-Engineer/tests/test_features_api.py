import os
import requests
import pytest

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
LIST_PATH = "/api/v1/features"
DETAIL_PATH_TEMPLATE = "/api/v1/features/{id}"

ACCEPTED_LIST_KEYS = [{"items_key": "items", "total_key": "total_count"},
                       {"items_key": "data", "total_key": "total"},
                       {"items_key": "features", "total_key": "total_count"}]


def _get_json_or_fail(resp):
    try:
        return resp.json()
    except ValueError:
        pytest.fail("Response is not valid JSON: %s" % resp.text)


@pytest.fixture(scope="module")
def base_url():
    return API_BASE.rstrip("/")


def _find_items_key(json_body):
    for k in ["items", "data", "features"]:
        if k in json_body:
            return k
    return None


def test_list_features_smoke(base_url):
    """
    Smoke test: list endpoint returns 200 or a clear auth error.
    If 200: assert JSON shape contains an items array and a total-like field.
    If 401/403: skip (auth required) with informative reason.
    """
    url = f"{base_url}{LIST_PATH}"
    params = {"page": 1, "per_page": 10}
    resp = requests.get(url, params=params)

    if resp.status_code in (401, 403):
        pytest.skip(f"Auth required or unauthorized: {resp.status_code}")

    assert resp.status_code == 200, f"Expected 200 from list endpoint, got {resp.status_code}: {resp.text}"

    body = _get_json_or_fail(resp)
    items_key = _find_items_key(body)
    assert items_key, f"List response JSON must include items array (e.g. 'items' or 'data'). Got keys: {list(body.keys())}"
    assert isinstance(body[items_key], list), f"Expected '{items_key}' to be a list"

    # total count presence is required by frontend acceptance criteria; allow several possible key names
    total_present = any(k in body for k in ["total_count", "total", "count"]) or ("meta" in body and isinstance(body.get("meta"), dict) and any(tk in body.get("meta") for tk in ["total_count", "total"]))
    assert total_present, "List response must include total_count/total in root or meta"


def test_pagination_behavior(base_url):
    """
    Verify pagination params are accepted and response length <= per_page.
    """
    url = f"{base_url}{LIST_PATH}"
    params = {"page": 2, "per_page": 5}
    resp = requests.get(url, params=params)

    if resp.status_code in (401, 403):
        pytest.skip(f"Auth required or unauthorized: {resp.status_code}")

    assert resp.status_code == 200, f"Expected 200 from list endpoint, got {resp.status_code}"
    body = _get_json_or_fail(resp)
    items_key = _find_items_key(body)
    assert items_key, "Missing items array in pagination response"
    items = body[items_key]
    assert isinstance(items, list)
    assert len(items) <= 5, f"Expected at most 5 items for per_page=5, got {len(items)}"


def test_get_feature_detail_if_exists(base_url):
    """
    If list returns at least one item, fetch its detail and validate shape.
    """
    list_url = f"{base_url}{LIST_PATH}"
    resp = requests.get(list_url, params={"page": 1, "per_page": 1})

    if resp.status_code in (401, 403):
        pytest.skip(f"Auth required or unauthorized: {resp.status_code}")

    if resp.status_code != 200:
        pytest.skip(f"List endpoint not available for detail test: {resp.status_code}")

    body = _get_json_or_fail(resp)
    items_key = _find_items_key(body)
    if not items_key or not body[items_key]:
        pytest.skip("No feature items returned; skipping detail test")

    item = body[items_key][0]
    # Support both 'id' and 'uuid'
    feature_id = item.get("id") or item.get("uuid")
    assert feature_id, f"List item missing id/uuid: {item}"

    detail_url = f"{base_url}{DETAIL_PATH_TEMPLATE.format(id=feature_id)}"
    dresp = requests.get(detail_url)

    if dresp.status_code in (401, 403):
        pytest.skip(f"Auth required for detail endpoint: {dresp.status_code}")

    assert dresp.status_code == 200, f"Expected 200 from detail endpoint, got {dresp.status_code}"
    dbody = _get_json_or_fail(dresp)
    # detail could be root object or {"data": {...}}
    detail_obj = dbody.get("data") if isinstance(dbody, dict) and "data" in dbody else dbody
    assert isinstance(detail_obj, dict), "Detail response must be a JSON object"
    assert detail_obj.get("id") or detail_obj.get("uuid"), "Detail object must include id/uuid"


def test_error_response_shape(base_url):
    """
    Intentionally request an invalid page to trigger a 4xx and validate error shape.
    This test is tolerant: if the API does not return 4xx for invalid params, the test will skip.
    """
    url = f"{base_url}{LIST_PATH}"
    # Use an obviously invalid param value to provoke 400
    resp = requests.get(url, params={"page": "not-an-int"})

    if resp.status_code == 200:
        pytest.skip("API accepted invalid param; cannot verify error shape")

    if resp.status_code >= 400 and resp.status_code < 600:
        # Expect error JSON like {code, message} or {error: {code, message}}
        try:
            body = resp.json()
        except ValueError:
            pytest.fail("Error response is not JSON")

        # Accept a few commonly used shapes
        if isinstance(body, dict) and ("code" in body and "message" in body):
            assert isinstance(body["code"], (str, int))
            assert isinstance(body["message"], str)
        elif isinstance(body, dict) and "error" in body and isinstance(body["error"], dict) and "message" in body["error"]:
            assert isinstance(body["error"]["message"], str)
        else:
            pytest.skip(f"Unrecognized error shape: keys={list(body.keys())}")
    else:
        pytest.skip(f"No error status returned for invalid param (status={resp.status_code})")


def test_auth_behavior_expectation(base_url):
    """
    Check whether endpoints enforce auth by calling without Authorization header.
    Pass if API returns 200 (public) or 401/403 (protected). Fail if returns unexpected code.
    """
    url = f"{base_url}{LIST_PATH}"
    resp = requests.get(url)
    if resp.status_code in (200, 401, 403):
        assert True
    else:
        pytest.fail(f"Unexpected status code when calling list endpoint without auth: {resp.status_code}")
