from __future__ import annotations

from typing import Optional

import appdaemon.plugins.hass.hassapi as hass

from entities import Entity

# Per-room companion sensors published from AppDaemon (via set_state, the same
# pattern as error_reporter.py) so the brightness more-info card can explain, in
# plain English, WHY the room's lights and blinds are in their current state.
#
# These are runtime entities with no YAML backing: they hold their value while
# HA runs and only change when we publish a new decision. They read `unknown`
# between an HA restart and the next publish — SceneApp.initialize() publishes an
# initial lights value to close the AppDaemon-restart gap; blinds populate on the
# first best_for_temperature()/close()/open() (an activity or mode change).
LIGHTS_STATUS = "sensor.{room}_lights_status"
BLINDS_STATUS = "sensor.{room}_blinds_status"


def room_key(brightness_sensor: Entity) -> str:
    """`sensor.office_brightness` -> `office`."""
    name = str(brightness_sensor)
    if name.startswith("sensor."):
        name = name[len("sensor."):]
    if name.endswith("_brightness"):
        name = name[: -len("_brightness")]
    return name


class StatusHandler:
    """Publishes the per-room lights/blinds "state + why" explanation sensors.

    Callers pass a short ``state`` word (kept as the sensor state for a clean
    history) and a ``reason`` phrased as a *because-clause*; the card renders the
    ``explanation`` attribute ("On because there isn't enough daylight").
    """

    def __init__(self, app: hass.Hass, room: str) -> None:
        self.app = app
        self.room = room
        self.lights_sensor = LIGHTS_STATUS.format(room=room)
        self.blinds_sensor = BLINDS_STATUS.format(room=room)

    def publish_lights(self, state: str, reason: str, detail: Optional[str] = None) -> None:
        self._publish(self.lights_sensor, "Lights", "mdi:lightbulb", state, reason, detail)

    def publish_blinds(self, state: str, reason: str, detail: Optional[str] = None) -> None:
        self._publish(self.blinds_sensor, "Blinds", "mdi:blinds", state, reason, detail)

    def _publish(self, sensor: str, label: str, icon: str,
                 state: str, reason: str, detail: Optional[str]) -> None:
        friendly_room = self.room.replace("_", " ").title()
        self.app.set_state(
            sensor,
            state=state,
            attributes={
                "reason": reason,
                "explanation": f"{state} because {reason}",
                "detail": detail,
                "friendly_name": f"{friendly_room} {label}",
                "icon": icon,
            },
        )
