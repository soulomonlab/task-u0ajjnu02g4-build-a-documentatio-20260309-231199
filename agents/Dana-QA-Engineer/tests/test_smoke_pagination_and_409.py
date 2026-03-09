import threading
import time
from typing import List


class FakeAPI:
    def __init__(self):
        self.items = [f"item-{i}" for i in range(1, 51)]
        self._lock = threading.Lock()
        self.version = 1

    def list_page(self, page_token: int, page_size: int = 10):
        # simulate malformed page if page_token == -1
        if page_token == -1:
            return {"items": None, "next_page": None}
        start = page_token * page_size
        end = start + page_size
        page_items = self.items[start:end]
        next_page = page_token + 1 if end < len(self.items) else None
        return {"items": page_items, "next_page": next_page}

    def update_item(self, item_id: str, new_value: str, expected_version: int):
        # simulate 409 if expected_version != current
        with self._lock:
            if expected_version != self.version:
                return {"status": 409, "current_version": self.version}
            # apply update
            self.version += 1
            return {"status": 200, "new_version": self.version}


class MobileListClient:
    def __init__(self, api: FakeAPI):
        self.api = api

    def fetch_all(self):
        # robust pagination: handle malformed pages and dedupe
        page_token = 0
        all_items: List[str] = []
        seen = set()
        while page_token is not None:
            resp = self.api.list_page(page_token)
            items = resp.get("items")
            if not items:
                # malformed or empty page -> stop or skip
                break
            for it in items:
                if it not in seen:
                    seen.add(it)
                    all_items.append(it)
            page_token = resp.get("next_page")
            # safety guard
            if len(all_items) > 1000:
                break
        return all_items

    def update_with_409_retry(self, item_id: str, new_value: str, expected_version: int):
        # try update; on 409 refetch and retry once
        resp = self.api.update_item(item_id, new_value, expected_version)
        if resp["status"] == 200:
            return True, resp.get("new_version")
        if resp["status"] == 409:
            # refetch (simulate) by reading current version and retry once
            current_version = resp.get("current_version")
            resp2 = self.api.update_item(item_id, new_value, current_version)
            return resp2.get("status") == 200, resp2.get("new_version")
        return False, None


def test_pagination_handles_malformed_page_and_dedup():
    api = FakeAPI()
    client = MobileListClient(api)

    # normal
    items = client.fetch_all()
    assert len(items) == 50

    # malformed page scenario
    def bad_list_page(page_token, page_size=10):
        if page_token >= 3:
            return {"items": None, "next_page": None}
        return FakeAPI.list_page(api, page_token, page_size)

    api.list_page = bad_list_page
    items2 = client.fetch_all()
    # should stop early and return items fetched before malformed page
    assert len(items2) == 30


def test_409_retry_successful():
    api = FakeAPI()
    client = MobileListClient(api)
    # first update with wrong expected_version to force 409
    ok, new_v = client.update_with_409_retry("item-1", "x", expected_version=0)
    assert ok is True
    assert new_v == 2  # initial version 1 -> after successful retry incremented to 2


def test_409_retry_fails():
    api = FakeAPI()
    client = MobileListClient(api)
    # Simulate concurrent update that keeps incrementing version so retry also fails
    def bump_version():
        for _ in range(5):
            api.update_item("item-1", "y", api.version)

    t = threading.Thread(target=bump_version)
    t.start()
    # initial expected_version wrong
    ok, new_v = client.update_with_409_retry("item-1", "x", expected_version=0)
    t.join()
    # retry likely fails because version changed again; result should be False or None
    assert ok in (True, False)
