from __future__ import annotations

from typing import Any, Optional

import requests
import yaml

# Same host codegen talks to, and the same secrets file it loads the token from.
HA_HOST = "https://calamarbicefalo.uk"
SECRETS_PATH = "secrets/secrets.yaml"
DEFAULT_TIMEOUT = 30


def load_token(path: str = SECRETS_PATH) -> str:
    """Load the HA long-lived token from secrets.yaml (shared by REST + WS clients)."""
    with open(path, "r") as stream:
        token = (yaml.safe_load(stream) or {}).get("apiToken")
    if not token or str(token).startswith("PASTE_"):
        raise SystemExit(
            f"No usable apiToken in {path}. Add a Home Assistant long-lived "
            f"access token (HA profile -> Security -> Long-lived access tokens)."
        )
    return str(token)


class HaClient:
    """Thin wrapper over the Home Assistant REST API.

    Auth reuses the long-lived token loaded by codegen (`secrets/secrets.yaml`),
    so no extra credentials are needed.
    """

    def __init__(self, host: str = HA_HOST, token: Optional[str] = None,
                 timeout: int = DEFAULT_TIMEOUT) -> None:
        self.host = host.rstrip("/")
        self.timeout = timeout
        self._token = token or load_token()

    @property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    def get(self, path: str, params: Optional[dict[str, Any]] = None) -> requests.Response:
        resp = requests.get(self.host + path, headers=self._headers,
                            params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def post(self, path: str, json: Optional[dict[str, Any]] = None) -> requests.Response:
        resp = requests.post(self.host + path, headers=self._headers,
                            json=json, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    # --- convenience wrappers used by the CLI scripts ---

    def error_log(self) -> str:
        text: str = self.get("/api/error_log").text
        return text

    def is_reachable(self) -> bool:
        """Whether the instance answers an authenticated request (for codegen)."""
        try:
            ok: bool = requests.get(self.host + "/api/states", headers=self._headers,
                                    timeout=self.timeout).ok
            return ok
        except requests.RequestException:
            return False

    def states(self) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = self.get("/api/states").json()
        return data

    def services(self) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = self.get("/api/services").json()
        return data

    def state(self, entity_id: str) -> dict[str, Any]:
        data: dict[str, Any] = self.get(f"/api/states/{entity_id}").json()
        return data

    def try_state(self, entity_id: str) -> Optional[dict[str, Any]]:
        """Like `state`, but returns None instead of raising on a 404."""
        resp = requests.get(self.host + f"/api/states/{entity_id}",
                            headers=self._headers, timeout=self.timeout)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data: dict[str, Any] = resp.json()
        return data

    def history(self, entity_id: str, start_iso: str) -> Any:
        return self.get(f"/api/history/period/{start_iso}",
                        params={"filter_entity_id": entity_id}).json()

    def logbook(self, start_iso: str, entity_id: Optional[str] = None) -> Any:
        params = {"entity": entity_id} if entity_id else None
        return self.get(f"/api/logbook/{start_iso}", params=params).json()

    def render_template(self, template: str) -> str:
        text: str = self.post("/api/template", json={"template": template}).text
        return text

    def call_service(self, domain: str, service: str,
                     data: Optional[dict[str, Any]] = None) -> None:
        """Invoke a HA service, e.g. call_service('homeassistant', 'reload_all')."""
        self.post(f"/api/services/{domain}/{service}", json=data or {})

    def check_config(self) -> dict[str, Any]:
        """Validate the live YAML config. Returns {'result': 'valid'|'invalid', ...}."""
        data: dict[str, Any] = self.post("/api/config/core/check_config").json()
        return data
