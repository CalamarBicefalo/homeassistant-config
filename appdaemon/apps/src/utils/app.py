from __future__ import annotations

from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import services
from activities import Activity
from entities import Entity
from helpers import Helper
from utils import states

HELPER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_to_helper(d: datetime):
    return d.strftime(HELPER_DATETIME_FORMAT)


class App(hass.Hass):
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

    def is_on(self, device: Entity):
        state = self.get_state(device)
        return state == states.ON or state == "playing"

    def is_off(self, device: Entity):
        return self.has_state(device, states.OFF)

    def has_state(self, device: Entity | Helper, desired_state: str) -> bool:
        state = self.get_state(device)
        return state == desired_state

    def is_activity(self, helper: Helper, activity: Activity):
        return self.has_state(helper, activity)

    def get_activity_value(self, helper: Helper) -> Activity:
        return self.get_state(helper)

    def set_activity(self, helper: Helper, activity: Activity):
        self.log(f'Setting activity {activity} in {helper}', level="DEBUG")
        self.call_service(
            services.INPUT_SELECT_SELECT_OPTION,
            entity_id=helper,
            option=activity
    )
