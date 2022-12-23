from datetime import timedelta
from typing import Any

import entities
import helpers
import services
import activities
from app import App
from modes import Mode


class Playground(App):
    def initialize(self) -> None:
        pass

    def on_schedule(self, kwargs: Any) -> None:
        pass

    def on_event(self, event_name: str, data: Any, kwargs: Any) -> None:
        pass

    def on_state(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        pass
