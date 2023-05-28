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
        self.listen_state(self.on_activity_change, map(lambda r: r._activity_helper, self.handlers.rooms.all))
        self.listen_state(self.on_door_open, entities.BINARY_SENSOR_FLAT_DOOR_CS)

    def on_activity_change(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.handlers.mode.get() == modes.Mode.AWAY and not new == CommonActivities.EMPTY:
            self.call_service("notify/notify",
                              message=f'Activity {new} detected in {entity} while away from home',
                              title="🚨Activity detected")

    def on_door_open(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.handlers.mode.get() == modes.Mode.AWAY:
            self.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                              message=f'Front door opened while away',
                              title="🚨Activity detected")
