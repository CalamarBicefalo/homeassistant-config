from typing import Any

import helpers
from app import App
from selects import Mode


class ModeScene(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            helpers.MODE
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        match new:
            case Mode.SLEEPING:
                self.turn_off_lights()
                self.turn_off_plugs()
            case Mode.AWAY:
                self.turn_off_media()
                self.turn_off_lights()
                self.turn_off_plugs()
