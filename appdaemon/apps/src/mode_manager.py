from datetime import timedelta
from typing import Any

from app import App
from modes import Mode


class ModeManager(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode manager.', level="DEBUG")
        self.run_at_sunrise(self.on_schedule)
        self.run_at_sunset(self.on_schedule)
        self.listen_event(self.on_alarm_dismissed, "SleepAsAndroid_phone")

    def on_schedule(self, kwargs: Any) -> None:
        if self.mode.get() not in [Mode.AWAY, Mode.SLEEPING]:
            self.set_mode_by_time()

    def on_alarm_dismissed(self, event_name: str, data: Any, kwargs: Any) -> None:
        if data['event'] == 'alarm_alert_dismiss':
            self.set_mode_by_time()

    def set_mode_by_time(self) -> None:
        if self.sunset() < self.sunrise():
            self.mode.set(Mode.DAY)
        else:
            self.mode.set(Mode.NIGHT)
