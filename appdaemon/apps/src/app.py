from __future__ import annotations

from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import helpers
from activities import ActivityHandlers
from entities import Entity
from helpers import Helper
import states
from modes import Mode
from select_handler import SelectHandler

HELPER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_to_helper(d: datetime) -> str:
    return d.strftime(HELPER_DATETIME_FORMAT)


class App(hass.Hass):
    mode: SelectHandler[Mode]
    activities: ActivityHandlers

    def __init__(self, ad, name, logging, args, config, app_config, global_vars) -> None:  # type: ignore
        super().__init__(ad, name, logging, args, config, app_config, global_vars)
        self.mode = SelectHandler[Mode](super(), helpers.HOMEASSISTANT_MODE)
        self.activities = ActivityHandlers(super())

    def helper_to_datetime(self, helper: Helper) -> datetime:
        """
        Given a datetime helper, it returns a ready to use datetime
        :param helper:
        :return: a datetime object
        """
        return datetime.strptime(str(self.get_state(helper)), HELPER_DATETIME_FORMAT)

    def datetime_to_helper(self, d: datetime) -> str:
        return datetime_to_helper(d)

    def is_consuming_at_least(self, device: Entity, watts: int) -> bool:
        return self.get_watt_consumption(device) >= watts

    def get_watt_consumption(self, device: Entity) -> int:
        return int(float(self.get_state(device)))

    def is_on(self, device: Entity) -> bool:
        state = self.get_state(device)
        on: bool = state == states.ON or state == "playing"
        return on

    def is_off(self, device: Entity) -> bool:
        return self.has_state(device, states.OFF)

    def has_state(self, device: Entity | Helper, desired_state: str) -> bool:
        state = self.get_state(device)
        b: bool = state == desired_state
        return b
