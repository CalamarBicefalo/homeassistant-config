from __future__ import annotations

from ops.wsclient import _ws_url


def test_ws_url_upgrades_https_to_wss() -> None:
    assert _ws_url("https://example.uk/") == "wss://example.uk/api/websocket"


def test_ws_url_upgrades_http_to_ws() -> None:
    assert _ws_url("http://localhost:8123") == "ws://localhost:8123/api/websocket"
