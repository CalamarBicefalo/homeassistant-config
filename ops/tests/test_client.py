from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ops.client import HaClient, load_token


def _resp(status: int = 200, json_data: object = None, text: str = "") -> MagicMock:
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    resp.text = text
    return resp


@patch("ops.client.requests.get")
def test_get_builds_url_and_sends_bearer_token(mock_get: MagicMock) -> None:
    mock_get.return_value = _resp(json_data={"ok": True})

    HaClient(host="https://h.example/", token="tok").get("/api/states", params={"a": "b"})

    assert mock_get.call_args.args[0] == "https://h.example/api/states"
    assert mock_get.call_args.kwargs["headers"]["Authorization"] == "Bearer tok"
    assert mock_get.call_args.kwargs["params"] == {"a": "b"}


@patch("ops.client.requests.get")
def test_try_state_returns_none_on_404(mock_get: MagicMock) -> None:
    mock_get.return_value = _resp(status=404)

    assert HaClient(token="t").try_state("sensor.missing") is None


@patch("ops.client.requests.get")
def test_try_state_returns_json_on_200(mock_get: MagicMock) -> None:
    mock_get.return_value = _resp(status=200, json_data={"state": "on"})

    assert HaClient(token="t").try_state("sensor.x") == {"state": "on"}


def test_load_token_rejects_placeholder(tmp_path: Path) -> None:
    secrets = tmp_path / "secrets.yaml"
    secrets.write_text('apiToken: "PASTE_LONG_LIVED_ACCESS_TOKEN_HERE"')

    with pytest.raises(SystemExit):
        load_token(str(secrets))


def test_load_token_reads_value(tmp_path: Path) -> None:
    secrets = tmp_path / "secrets.yaml"
    secrets.write_text('apiToken: "real-token-123"')

    assert load_token(str(secrets)) == "real-token-123"
