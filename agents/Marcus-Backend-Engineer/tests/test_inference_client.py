"""Unit tests for inference client auth header behaviour.

Tests implemented:
- Anthropic: when env var present, header uses 'x-api-key'
- OpenAI: when env var present, header uses 'Authorization: Bearer <key>'
- Missing env var raises ValueError
- api_key override in constructor takes precedence over env var

We mock os.environ and requests.post where network calls would happen.
"""
from __future__ import annotations

import os
import json
import pytest
from unittest.mock import patch, MagicMock

from output.code.inference_client import InferenceClient


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "anthropic-env-key"}, clear=True)
def test_anthropic_header_from_env():
    client = InferenceClient(provider="anthropic")
    headers = client._build_headers()
    assert headers["x-api-key"] == "anthropic-env-key"
    assert headers["Content-Type"] == "application/json"


@patch.dict(os.environ, {"OPENAI_API_KEY": "openai-env-key"}, clear=True)
def test_openai_header_from_env():
    client = InferenceClient(provider="openai")
    headers = client._build_headers()
    assert headers["Authorization"] == "Bearer openai-env-key"


def test_missing_env_raises():
    with patch.dict(os.environ, {}, clear=True):
        client = InferenceClient(provider="anthropic")
        with pytest.raises(ValueError):
            client._build_headers()


def test_override_api_key():
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "env-key"}, clear=True):
        client = InferenceClient(provider="anthropic", api_key="override-key")
        headers = client._build_headers()
        assert headers["x-api-key"] == "override-key"


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "env-key"}, clear=True)
@patch("output.code.inference_client.requests.post")
def test_send_request_calls_requests_post(mock_post):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"ok": True}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    client = InferenceClient(provider="anthropic", base_url="https://api.anthropic.com/v1")
    res = client.send_request("/test", {"input": "hello"})
    mock_post.assert_called_once()
    assert res == {"ok": True}
