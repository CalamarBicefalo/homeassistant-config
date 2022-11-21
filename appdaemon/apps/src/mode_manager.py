from datetime import timedelta

from app import App
from modes import Mode


class ModeManager(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode manager.', level="DEBUG")
        self.run_at_sunrise(self.on_day, offset=timedelta(minutes=30).total_seconds())
        self.run_at_sunset(self.on_night, offset=timedelta(minutes=-30).total_seconds())

    def on_day(self, kwargs) -> None:
        self.on_schedule(Mode.DAY)

    def on_night(self, kwargs) -> None:
        self.on_schedule(Mode.NIGHT)

    def on_schedule(self, mode: Mode) -> None:
        if self.mode.get() not in [Mode.AWAY, Mode.BEDTIME, Mode.SLEEPING]:
            self.mode.set(mode)
