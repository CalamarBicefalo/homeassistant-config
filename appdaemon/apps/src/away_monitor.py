from typing import Any

import entities
import mode_controller
import modes
import services
from app import App
from rooms import *


class AwayMonitor(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode monitor.', level="DEBUG")
        self.listen_state(self.on_door_open, entities.BINARY_SENSOR_FLAT_DOOR_CS)

    def on_door_open(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.handlers.mode.get() == modes.Mode.AWAY:
            self.handlers.notifications.notify(title="🚨Activity detected", message=f'Front door opened while away')
