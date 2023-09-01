from typing import Any

import entities
import mode_controller
import modes
import services
from app import App
from rooms import *


class MediaController(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode monitor.', level="DEBUG")
        self.listen_state(self.on_door_open, entities.BINARY_SENSOR_FLAT_DOOR_CS)

    def on_door_open(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.handlers.mode.get() == modes.Mode.AWAY:
            self.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                              message=f'Front door opened while away',
                              title="🚨Activity detected")

    def on_play(self, device_ieee: str, callback: Callable[..., None]) -> None:
        self.listen_event(lambda *_: callback(), "zha_event", command='toggle', device_ieee=device_ieee)

    def on_forwards(self, device_ieee: str, callback: Callable[..., None]) -> None:
        self.listen_event(lambda *_: callback(), "zha_event", command='step', params=lambda x: x.step_mode == 0,
                               device_ieee=device_ieee)

    def on_backwards(self, device_ieee: str, callback: Callable[..., None]) -> None:
        self.listen_event(lambda *_: callback(), "zha_event", command='step', params=lambda x: x.step_mode == 0,
                               device_ieee=device_ieee)
