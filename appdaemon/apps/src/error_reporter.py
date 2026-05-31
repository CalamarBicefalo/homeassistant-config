from datetime import datetime
from typing import Any

from app import App

# Entity + event used to surface AppDaemon problems inside Home Assistant so they
# can be read over the REST API (see ops/appderrors.py).
LAST_ERROR_SENSOR = "sensor.appdaemon_last_error"
ERROR_EVENT = "appdaemon.error"

# Heartbeat state set on startup so the sensor always exists (liveness check).
STATUS_OK = "ok"

# HA state values are capped at 255 chars; keep the headline within that.
MAX_STATE_LENGTH = 255


class ErrorReporter(App):
    """Mirrors AppDaemon WARNING/ERROR log records into Home Assistant.

    Subscribes to the AppDaemon log stream and republishes anything at WARNING or
    above (including uncaught callback exceptions, which AppDaemon logs to its
    error log) so failures are visible without shelling into the add-on:
    - `sensor.appdaemon_last_error` holds the most recent problem (+ attributes),
    - an `appdaemon.error` event is fired so the full history lands in the logbook.
    """

    def initialize(self) -> None:
        self.log('Initializing error reporter.', level="DEBUG")
        self.listen_log(self.on_log, level="WARNING")
        # Heartbeat: create the sensor on startup so the app's liveness is
        # verifiable and ops.appderrors never 404s. Real errors overwrite it.
        self.set_state(
            LAST_ERROR_SENSOR,
            state=STATUS_OK,
            attributes={"status": STATUS_OK, "initialized_at": str(self.datetime())},
        )

    def on_log(self, name: str, ts: datetime, level: str, log_type: str,
               message: str, kwargs: Any) -> None:
        # Skip our own records to avoid a feedback loop (AppDaemon also guards
        # against this, but the explicit check keeps intent obvious).
        if name == self.name:
            return

        self.set_state(
            LAST_ERROR_SENSOR,
            state=self._headline(name, level, message),
            attributes={
                "app": name,
                "level": level,
                "type": log_type,
                "message": message,
                "timestamp": str(ts),
            },
        )
        self.fire_event(ERROR_EVENT, app=name, level=level, message=message)

    @staticmethod
    def _headline(name: str, level: str, message: str) -> str:
        first_line = (message.splitlines() or [""])[0]
        return f'{level} [{name}] {first_line}'[:MAX_STATE_LENGTH]
