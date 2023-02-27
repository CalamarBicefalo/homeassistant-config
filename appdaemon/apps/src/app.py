from __future__ import annotations

from datetime import datetime
from typing import Optional

import appdaemon.plugins.hass.hassapi as hass

import entities
import helpers
import services
import states
from activities import ActivityHandlers
from blinds import BlindsHandler
from entities import Entity
from helpers import Helper
from modes import Mode
from music import MusicHandler
from select_handler import SelectHandler

HELPER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_to_helper(d: datetime) -> str:
    return d.strftime(HELPER_DATETIME_FORMAT)


class App(hass.Hass):
    mode: SelectHandler[Mode]
    activities: ActivityHandlers
    music: MusicHandler
    blinds: BlindsHandler

    def __init__(self, ad, name, logging, args, config, app_config, global_vars) -> None:  # type: ignore
        super().__init__(ad, name, logging, args, config, app_config, global_vars)
        self.mode = SelectHandler[Mode](super(), helpers.HOMEASSISTANT_MODE)
        self.activities = ActivityHandlers(super())
        self.music = MusicHandler(super(), self.speakers)
        self.blinds = BlindsHandler(super())

    @property
    def speakers(self) -> Optional[entities.Entity]:
        return None

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

    def turn_off_media(self) -> None:
        self.call_service(services.MEDIA_PLAYER_TURN_OFF, entity_id="all")

    def turn_off_lights(self) -> None:
        self.call_service(services.LIGHT_TURN_OFF, entity_id="all")

    def turn_off_plugs(self) -> None:
        self.turn_off(entities.SWITCH_DRUMS_PLUG)
        self.turn_off(entities.SWITCH_MONITOR_PLUG)
