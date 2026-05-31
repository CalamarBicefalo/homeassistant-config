from __future__ import annotations

import json
from typing import Any, Optional

import certifi
from websocket import create_connection

from ops.client import HA_HOST, load_token

WS_TIMEOUT = 20


def _ws_url(host: str) -> str:
    base = host.replace("https://", "wss://").replace("http://", "ws://").rstrip("/")
    return f"{base}/api/websocket"


def call(command: dict[str, Any], host: str = HA_HOST, token: Optional[str] = None) -> Any:
    """Authenticate and run a single Home Assistant WebSocket command.

    Used for data not available over REST on this instance (e.g. system_log,
    since file logging is disabled and /api/error_log returns 404). Returns the
    command's `result` payload.
    """
    token = token or load_token()
    # certifi CA bundle: macOS framework Python lacks a usable default for raw sockets.
    ws = create_connection(_ws_url(host), timeout=WS_TIMEOUT,
                        sslopt={"ca_certs": certifi.where()})
    try:
        ws.recv()  # auth_required handshake
        ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth = json.loads(ws.recv())
        if auth.get("type") != "auth_ok":
            raise SystemExit(f"WebSocket auth failed: {auth}")

        ws.send(json.dumps({"id": 1, **command}))
        while True:
            message = json.loads(ws.recv())
            if message.get("id") == 1:
                break
    finally:
        ws.close()

    if not message.get("success", False):
        raise SystemExit(f"WebSocket command failed: {message.get('error', message)}")
    return message.get("result")


def system_log() -> list[dict[str, Any]]:
    """Return Home Assistant's captured core WARNING/ERROR records (newest first)."""
    result: list[dict[str, Any]] = call({"type": "system_log/list"})
    return result
