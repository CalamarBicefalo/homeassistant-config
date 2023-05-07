from typing import Any

import alarmclock
from app import App
from modes import Mode

EVENT_MODE_RECOMPUTE_NEEDED = "mode.recompute_needed"


class ModeController(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode manager.', level="DEBUG")
        self.run_at_sunrise(self.on_schedule)
        self.run_at_sunset(self.on_schedule)
        self.alarmclock.listen(self._handle_mode, alarmclock.Event.ALARM_DISMISSED)
        self.listen_event(self.on_bedroom_unlock, EVENT_MODE_RECOMPUTE_NEEDED)
        self.listen_state(self.on_person_event, "person")

    def on_schedule(self, kwargs: Any) -> None:
        if self.mode.get() not in [Mode.AWAY, Mode.SLEEPING]:
            self._handle_mode()

    def on_bedroom_unlock(self, event_name: str, data: Any, kwargs: Any) -> None:
        self._handle_mode()

    def on_person_event(self, entity, attribute, old, new, kwargs):  # type: ignore
        self._handle_mode()

    def _handle_mode(self) -> None:
        if self.noone_home():
            self.mode.set(Mode.AWAY)
        elif self.sunset() < self.sunrise():
            self.mode.set(Mode.DAY)
        else:
            self.mode.set(Mode.NIGHT)
