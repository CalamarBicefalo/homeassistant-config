from __future__ import annotations

from datetime import datetime
from typing import Optional

import appdaemon.plugins.hass.hassapi as hass

import entities
import helpers
import services
import states
from alarmclock import AlarmClock
from blinds import BlindsHandler
from entities import Entity
from flick import FlickHandler
from helpers import Helper
from modes import Mode
from music import MusicHandler
from rooms import RoomHandlers
from select_handler import SelectHandler


class App(hass.Hass):
    mode: SelectHandler[Mode]
    rooms: RoomHandlers
    music: MusicHandler
    blinds: BlindsHandler
    alarmclock: AlarmClock
    flick: FlickHandler

    def __init__(self, ad, name, logging, args, config, app_config, global_vars) -> None:  # type: ignore
        super().__init__(ad, name, logging, args, config, app_config, global_vars)
        self.mode = SelectHandler[Mode](super(), helpers.HOMEASSISTANT_MODE)
        self.rooms = RoomHandlers(super())
        self.music = MusicHandler(super(), self.speakers)
        self.blinds = BlindsHandler(super())
        self.alarmclock = AlarmClock(super())
        self.flick = FlickHandler(super())

    @property
    def speakers(self) -> Optional[entities.Entity]:
        return None

    def helper_to_datetime(self, helper: Helper) -> datetime:
        """
        Given a datetime helper, it returns a ready to use datetime
        :param helper:
        :return: a datetime object
        """
        return datetime.strptime(str(self.get_state(helper)), helpers.HELPER_DATETIME_FORMAT)

    def is_consuming_at_least(self, device: Entity, watts: int) -> bool:
        return self.get_watt_consumption(device) >= watts

    def get_watt_consumption(self, device: Entity) -> int:
        return int(float(self.get_state(device)))

    def is_on(self, device: Entity) -> bool:
        state = self.get_state(device)
        on: bool = state == states.ON or state == states.PLAYING
        return on

    def is_off(self, device: Entity) -> bool:
        return self.has_state(device, states.OFF)

    def has_state(self, device: Entity | Helper, desired_state: str) -> bool:
        state = self.get_state(device)
        b: bool = state == desired_state
        return b

    def has_state_attr(self, device: Entity | Helper, attr: str, desired_state: str) -> bool:
        state = self.get_state(device, attribute=attr)
        b: bool = state == desired_state
        return b

    def turn_off_media(self) -> None:
        self.call_service(services.MEDIA_PLAYER_TURN_OFF, entity_id="all")

    def turn_off_lights(self) -> None:
        self.call_service(services.LIGHT_TURN_OFF, entity_id="all")

    def turn_off_plugs(self) -> None:
        self.turn_off(entities.SWITCH_DRUMS_PLUG)
        self.turn_off(entities.SWITCH_MONITOR_PLUG)
