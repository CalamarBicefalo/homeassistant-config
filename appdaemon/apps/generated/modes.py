from helpers import Helper
from enum import Enum


class Home:
    _helper = Helper("input_select.homeassistant_mode")

    class Mode(Enum):
        DAY = "Day"
        NIGHT = "Night"
        AWAY = "Away"
        BEDTIME = "Bedtime"
        SLEEPING = "Sleeping"

    def __init__(self, app: App):
        self._app = app

    def set_mode(self, mode: Mode):
        self.log("Setting mode " + mode.value, level="DEBUG")
        self.call_service(
            services.INPUT_SELECT_SELECT_OPTION,
            entity_id=self._helper,
            option=mode.value
        )

    def is_mode(self, helper: Helper, mode: Mode):
        return self._app.has_state(self._helper, mode.value)

    def get_mode(self) -> Mode:
        return  Mode(self.get_state(helper))

