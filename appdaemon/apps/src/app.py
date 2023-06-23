from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, Callable, Any, Dict

import appdaemon.plugins.hass.hassapi as hass

import entities
import helpers
import services
import states
from alarmclock import AlarmClock
from blinds_handler import BlindsHandler
from button_handler import ButtonHandler
from entities import Entity
from flick import FlickHandler
from helpers import Helper
from modes import Mode
from music import MusicHandler
from rooms import RoomHandlers
from select_handler import SelectHandler


class Handler():
    handlers: SelectHandler[Mode]
    rooms: RoomHandlers
    music: MusicHandler
    blinds: BlindsHandler
    alarmclock: AlarmClock
    flick: FlickHandler
    buttons: ButtonHandler

    def __init__(self, app: hass.Hass, speakers: Optional[Entity], blinds: Optional[Entity]) -> None:
        self.mode = SelectHandler[Mode](app, helpers.HOMEASSISTANT_MODE)
        self.rooms = RoomHandlers(app)
        self.music = MusicHandler(app, speakers)
        self.blinds = BlindsHandler(app, blinds)
        self.alarmclock = AlarmClock(app)
        self.flick = FlickHandler(app)
        self.buttons = ButtonHandler(app)


class App(hass.Hass):
    handlers: Handler

    def __init__(self, ad, name, logging, args, config, app_config, global_vars) -> None:  # type: ignore
        super().__init__(ad, name, logging, args, config, app_config, global_vars)
        self.handlers = Handler(super(), speakers=self.speakers, blinds=self.blinds)
        self.timers: Dict = {}

    @property
    def speakers(self) -> Optional[entities.Entity]:
        return None

    @property
    def blinds(self) -> Optional[entities.Entity]:
        return None

    def helper_to_datetime(self, helper: Helper) -> datetime:
        """
        Given a datetime helper, it returns a ready to use datetime
        :param helper:
        :return: a datetime object
        """
        return datetime.strptime(str(self.get_state(helper)), helpers.HELPER_DATETIME_FORMAT)

    def set_helper_to_now(self, helper: helpers.Helper) -> None:
        self.call_service(
            services.INPUT_DATETIME_SET_DATETIME,
            entity_id=helper,
            datetime=helpers.datetime_to_helper(datetime.now())
        )

    def is_consuming_at_least(self, device: Entity, watts: int) -> bool:
        return self.get_watt_consumption(device) >= watts

    def get_watt_consumption(self, device: Entity) -> int:
        return int(self.get_state_as_number(device))

    def is_on(self, device: Entity) -> bool:
        state = self.get_state(device)
        on: bool = state == states.ON or state == states.PLAYING
        return on

    def is_off(self, device: Entity) -> bool:
        return self.has_state(device, states.OFF)

    def get_state_as_number(
            self,
            device: Entity,
    ) -> Any:
        state = self.get_state(device)
        if state == states.UNAVAILABLE:
            error = f'Unavailable state [number] for {device}'
            self.log(error, level="ERROR")
            self.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23, message=error, title="Automation error")
            return 0
        try:
            return float(state)
        except ValueError:
            error = f'Cannot convert value "{state}" to number for {device}'
            self.log(error, level="ERROR")
            self.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23, message=error, title="Automation error")
            return 0

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
        self.turn_off(entities.SWITCH_DRUMKIT)
        self.turn_off(entities.SWITCH_MONITOR)
        self.turn_off(entities.SWITCH_DYSON)

    def run_for(self, minutes: int, every_minute: Callable[[int], None],
                afterwards: Optional[Callable[[], None]]) -> None:
        """

        :param minutes: For how long this callback should run for, with a minutely frequency
        :param every_minute: Callback to execute every minute, if throws, the timer gets aborted
        :param afterwards: Callback to execute when the loop is over
        :return:
        """
        timer = uuid.uuid4()

        def every_minute_callback(*_: Any) -> None:
            minutes_left = self.timers[timer] - 1
            self.log(f'Running scheduled minutely callback. Remaining time: {minutes_left}', level="INFO")

            self.timers[timer] = minutes_left

            if minutes_left <= 0 and afterwards:
                afterwards()
                return

            try:
                every_minute(minutes_left)
            except Exception as exc:
                self.log(f'Aborting run_for loop due to exception: {exc}', level="INFO")
                return

            self.run_in(every_minute_callback, 60)
            self.timers[timer] = minutes_left

        self.run_in(every_minute_callback, 60)
        self.timers[timer] = minutes
