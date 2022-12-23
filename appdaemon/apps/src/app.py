from __future__ import annotations

from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import entities
import helpers
import services
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
    music: MusicHandler

    def __init__(self, ad, name, logging, args, config, app_config, global_vars) -> None:  # type: ignore
        super().__init__(ad, name, logging, args, config, app_config, global_vars)
        self.mode = SelectHandler[Mode](super(), helpers.HOMEASSISTANT_MODE)
        self.activities = ActivityHandlers(super())
        self.music = MusicHandler(super())

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


class MusicHandler:
    def __init__(self, app: hass.Hass):
        self._app = app

    def play(self, tune: str, speakers: entities.Entity, shuffle: bool = True, volume_level: float = 0.3) -> None:
        self._app.call_service(services.MEDIA_PLAYER_VOLUME_SET,
                               entity_id=speakers, volume_level=volume_level),
        self._app.log(f'Configured volume of {speakers} to {volume_level}.', level="DEBUG")
        self._app.call_service(services.MEDIA_PLAYER_SHUFFLE_SET,
                               entity_id=speakers, shuffle=shuffle)
        self._app.log(f'{"Shuffling" if shuffle else "Not shuffling"} queue of {speakers}.', level="DEBUG")
        self._app.call_service(services.MASS_QUEUE_COMMAND,
                               entity_id=speakers,
                               command="play_media",
                               uri=tune,
                               enqueue_mode="replace",
                               )
        self._app.log(f'Playing {tune} on {speakers} - replacing existing queue.', level="DEBUG")

    def pause(self, speakers: entities.Entity) -> None:
        self._app.call_service(services.MEDIA_PLAYER_MEDIA_PAUSE, entity_id=speakers)
