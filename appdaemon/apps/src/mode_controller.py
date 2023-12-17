from typing import Any

import alarmclock
import entities
from app import App
from modes import Mode

EVENT_MODE_RECOMPUTE_NEEDED = "mode.recompute_needed"


class ModeController(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode manager.', level="DEBUG")
        self.run_at_sunrise(self.on_schedule)
        self.run_at_sunset(self.on_schedule)
        self.handlers.alarmclock.listen(self._handle_mode_unless_away, alarmclock.Event.ALARM_DISMISSED)
        self.listen_event(self.on_recompute_mode, EVENT_MODE_RECOMPUTE_NEEDED)
        self.listen_state(self.on_person_event, "person")
        self.listen_state(self.on_door_open, entities.BINARY_SENSOR_FLAT_DOOR_CS)

    def on_door_open(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self._handle_day_night_mode()

    def on_schedule(self, kwargs: Any) -> None:
        if not self.handlers.mode.is_value(Mode.SLEEPING):
            self._handle_mode_unless_away()

    def on_recompute_mode(self, event_name: str, data: Any, kwargs: Any) -> None:
        self._handle_mode_unless_away()

    def on_person_event(self, entity, attribute, old, new, kwargs):  # type: ignore
        if self.noone_home(person=True):
            self.handlers.mode.set(Mode.AWAY)
        else:
            self._handle_mode_unless_sleeping()

    def _handle_mode_unless_away(self) -> None:
        if self.handlers.mode.is_value(Mode.AWAY):
            return

        self._handle_day_night_mode()

    def _handle_mode_unless_sleeping(self) -> None:
        if self.handlers.mode.is_value(Mode.SLEEPING):
            return

        self._handle_day_night_mode()

    def _handle_day_night_mode(self) -> None:
        if self.sunset() < self.sunrise():
            self.handlers.mode.set(Mode.DAY)
        else:
            self.handlers.mode.set(Mode.NIGHT)
