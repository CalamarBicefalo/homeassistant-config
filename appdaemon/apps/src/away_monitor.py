from typing import Any

import modes
from app import App
from rooms import *


class AwayMonitor(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode monitor.', level="DEBUG")
        self.listen_state(self.on_activity_change, map(lambda r: r.activity._helper, self.rooms.all))

    def on_activity_change(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.mode.get() == modes.Mode.AWAY and not new == CommonActivities.EMPTY:
            self.call_service("notify/notify",
                              message=f'Activity {new} detected in {entity} while away from home',
                              title="🚨Activity detected")
