from datetime import timedelta

import entities
import services
from app import App


class ModeManager(App):

    def initialize(self):
        self.log(f'Initializing mode manager.', level="DEBUG")
        self.run_at_sunrise(self.on_day, offset=timedelta(minutes=30).total_seconds())
        self.run_at_sunset(self.on_night, offset=timedelta(minutes=-30).total_seconds())

    def on_day(self, kwargs):
        self.on_schedule("Day")

    def on_night(self, kwargs):
        self.on_schedule("Night")

    def on_schedule(self, mode):
        mode = self.get_state(entities.INPUT_SELECT_HOMEASSISTANT_MODE)
        if mode not in ["Away", "Bedtime", "Sleeping"]:
            self.call_service(services.INPUT_SELECT_SELECT_OPTION, entity_id=entities.INPUT_SELECT_HOMEASSISTANT_MODE,
                              option=mode)
