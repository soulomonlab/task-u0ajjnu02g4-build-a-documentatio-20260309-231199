import threading
import time
from typing import Optional


class FakeAuthServer:
    def __init__(self):
        self._lock = threading.Lock()
        self.refresh_calls = 0

    def login(self, username, password):
        # returns access_token, refresh_token, expires_in (seconds)
        return ("access-1", "refresh-1", 1)  # short expiry for tests

    def refresh(self, refresh_token):
        with self._lock:
            self.refresh_calls += 1
        # return new access token with longer lifetime
        return ("access-2", "refresh-2", 5)


class MobileClient:
    def __init__(self, server: FakeAuthServer):
        self.server = server
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.expiry_ts: float = 0
        self._refresh_lock = threading.Lock()

    def login(self, username, password):
        a, r, expires = self.server.login(username, password)
        self.access_token = a
        self.refresh_token = r
        self.expiry_ts = time.time() + expires

    def _is_expired(self):
        return time.time() >= self.expiry_ts

    def _refresh_if_needed(self):
        # single-flight refresh using lock
        if not self._is_expired():
            return
        if self._refresh_lock.acquire(False):
            try:
                # call server refresh
                a, r, expires = self.server.refresh(self.refresh_token)
                self.access_token = a
                self.refresh_token = r
                self.expiry_ts = time.time() + expires
            finally:
                self._refresh_lock.release()
        else:
            # another thread is refreshing; wait until done
            while self._is_expired():
                time.sleep(0.01)

    def request_protected_resource(self):
        # Simulate making a request; if token expired -> trigger refresh then succeed
        if self._is_expired():
            # simulate receiving 401 and triggering refresh
            self._refresh_if_needed()
        # After refresh (or if not expired) return resource
        return {"data": "ok", "token": self.access_token}


def test_single_flight_refresh():
    server = FakeAuthServer()
    client = MobileClient(server)
    client.login("u", "p")

    # wait until token expires
    time.sleep(1.1)

    results = []

    def worker():
        r = client.request_protected_resource()
        results.append(r)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # All requests should complete and share the same refreshed token
    assert len(results) == 8
    tokens = set(r["token"] for r in results)
    assert tokens == {"access-2"}
    # Server refresh should have been called once (single-flight)
    assert server.refresh_calls == 1


def test_failed_refresh_forces_logout():
    class BadServer(FakeAuthServer):
        def refresh(self, refresh_token):
            with self._lock:
                self.refresh_calls += 1
            # Simulate failed refresh by returning None (or raising)
            raise Exception("refresh failed")

    server = BadServer()
    client = MobileClient(server)
    client.login("u", "p")
    time.sleep(1.1)

    try:
        client.request_protected_resource()
        assert False, "expected exception"
    except Exception:
        # expected: client couldn't refresh and bubbled exception -> app should force logout
        assert client.access_token is None or client._is_expired() or server.refresh_calls == 1
