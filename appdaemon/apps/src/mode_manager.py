from datetime import timedelta
from typing import Any

from app import App
from modes import Mode


class ModeManager(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode manager.', level="DEBUG")
        self.run_at_sunrise(self.on_day, offset=timedelta(minutes=30).total_seconds())
        self.run_at_sunset(self.on_night, offset=timedelta(minutes=-30).total_seconds())
        self.listen_event(self.on_alarm_dismissed, "SleepAsAndroid_phone")

    def on_day(self, kwargs: Any) -> None:
        self.on_schedule(Mode.DAY)  # type: ignore

    def on_night(self, kwargs: Any) -> None:
        self.on_schedule(Mode.NIGHT)  # type: ignore

    def on_schedule(self, mode: Mode) -> None:
        if self.mode.get() not in [Mode.AWAY, Mode.BEDTIME, Mode.SLEEPING]:
            self.mode.set(mode)

    def on_alarm_dismissed(self, event_name: str, data: Any, kwargs: Any) -> None:
        if data['event'] == 'alarm_alert_dismiss':
            if self.sunset() < self.sunrise():
                self.mode.set(Mode.DAY)
            else:
                self.mode.set(Mode.NIGHT)
