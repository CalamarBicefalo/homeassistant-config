from typing import Any

import entities
import selects
from app import App


class AwayMonitor(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode monitor.', level="DEBUG")
        self.listen_state(self.on_door_open, entities.BINARY_SENSOR_FLAT_DOOR_CS)

    def on_door_open(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.handlers.mode.get() == selects.Mode.AWAY:
            self.handlers.notifications.security_alert(title="🚨Activity detected", message=f'Front door opened while away')
