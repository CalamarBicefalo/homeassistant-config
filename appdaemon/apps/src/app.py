from __future__ import annotations

from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import helpers
import services
from activities import Activity
from entities import Entity
from helpers import Helper
import states
from modes import Mode
from select_handler import SelectHandler

HELPER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_to_helper(d: datetime):
    return d.strftime(HELPER_DATETIME_FORMAT)


class App(hass.Hass):

    mode: SelectHandler[Mode]
    def __init__(self, ad, name, logging, args, config, app_config, global_vars):
        super().__init__(ad, name, logging, args, config, app_config, global_vars)
        self.mode = SelectHandler[Mode](super(), helpers.HOMEASSISTANT_MODE)
    def helper_to_datetime(self, helper: Helper):
        """
        Given a datetime helper, it returns a ready to use datetime
        :param helper:
        :return: a datetime object
        """
        return datetime.strptime(str(self.get_state(helper)), HELPER_DATETIME_FORMAT)

    def datetime_to_helper(self, d: datetime):
        return datetime_to_helper(d)

    def is_consuming_at_least(self, device: Entity, watts: int) -> bool:
        return self.get_watt_consumption(device) >= watts

    def get_watt_consumption(self, device: Entity) -> int:
        return int(float(self.get_state(device)))

    def is_on(self, device: Entity) -> bool:
        state = self.get_state(device)
        return state == states.ON or state == "playing"

    def is_off(self, device: Entity) -> bool:
        return self.has_state(device, states.OFF)

    def has_state(self, device: Entity | Helper, desired_state: str) -> bool:
        state = self.get_state(device)
        return state == desired_state

    def is_activity(self, helper: Helper, activity: Activity) -> bool:
        return self.has_state(helper, activity)

    def get_activity_value(self, helper: Helper) -> Activity:
        return Activity(self.get_state(helper))

    def set_activity(self, helper: Helper, activity: Activity) -> None:
        self.log(f'Setting activity {activity} in {helper}', level="DEBUG")
        self.call_service(
            services.INPUT_SELECT_SELECT_OPTION,
            entity_id=helper,
            option=activity
    )
