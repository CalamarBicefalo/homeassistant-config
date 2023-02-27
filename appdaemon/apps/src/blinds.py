from __future__ import annotations

from appdaemon.plugins.hass import hassapi as hass


class BlindsHandler:
    def __init__(self, app: hass.Hass) -> None:
        self.app = app

    def open_all(self) -> None:
        self.app.call_service("cover/open_cover",
                              entity_id="all")

    def close_all(self) -> None:
        self.app.call_service("cover/close_cover",
                              entity_id="all")
