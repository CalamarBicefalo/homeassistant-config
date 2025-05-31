from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, Callable, Any, Dict
from uuid import UUID

import appdaemon.plugins.hass.hassapi as hass
from appdaemon.appdaemon import AppDaemon

import entities
import helpers
import services
from alarmclock import AlarmClock
from blinds_handler import BlindsHandler
from button_handler import ButtonHandler
from entities import Entity
from flick import FlickHandler
from music import MusicHandler
from notification_handler import NotificationHandler
from rooms import RoomHandlers
from select_handler import SelectHandler
from selects import Mode
from state_handler import StateHandler
from temperature_handler import TemperatureHandler


class Handler():
    handlers: SelectHandler[Mode]
    rooms: RoomHandlers
    music: MusicHandler
    blinds: BlindsHandler
    alarmclock: AlarmClock
    flick: FlickHandler
    buttons: ButtonHandler
    notifications: NotificationHandler
    temperature: TemperatureHandler

    def __init__(self, app: hass.Hass, speakers: Optional[Entity], blinds: Optional[Entity],
                 room_has_plants: bool) -> None:
        self.mode = SelectHandler[Mode](app, helpers.MODE)
        self.rooms = RoomHandlers(app)
        self.music = MusicHandler(app, speakers)
        self.blinds = BlindsHandler(app, blinds, room_has_plants)
        self.alarmclock = AlarmClock(app)
        self.flick = FlickHandler(app)
        self.buttons = ButtonHandler(app)
        self.notifications = NotificationHandler(app)
        self.temperature = TemperatureHandler(app)

class Timer:
    minutes_left: int
    id: UUID

    def __init__(self):
        self.id = uuid.uuid4()

class App(hass.Hass):
    handlers: Handler

    def __init__(self, ad: AppDaemon, config_model: "AppConfig"):  # type: ignore
        super().__init__(ad, config_model)
        self.handlers = Handler(
            super(),
            speakers=self.speakers,
            blinds=self.blinds,
            room_has_plants=self.room_has_plants
        )
        self.state = StateHandler(super())
        self.timers: Dict[UUID, Timer] = {}

    @property
    def speakers(self) -> Optional[entities.Entity]:
        return None

    @property
    def room_has_plants(self) -> bool:
        return False

    @property
    def blinds(self) -> Optional[entities.Entity]:
        return None

    def is_dark(self) -> bool:
        number: int = self.state.get_as_number(entities.SENSOR_LIVING_ROOM_ILLUMINANCE)
        return number < 25

    def set_helper_to_now(self, helper: helpers.Helper) -> None:
        self.call_service(
            services.INPUT_DATETIME_SET_DATETIME,
            entity_id=helper,
            datetime=helpers.datetime_to_helper(datetime.now())
        )

    def turn_off_media(self) -> None:
        self.call_service(services.MEDIA_PLAYER_MEDIA_STOP, entity_id="all")
        self.call_service(services.MEDIA_PLAYER_TURN_OFF, entity_id="all")

    def turn_off_lights(self) -> None:
        self.call_service(services.LIGHT_TURN_OFF, entity_id="all")

    def turn_off_plugs(self) -> None:
        self.turn_off(entities.LIGHT_DRUM_POWER_STRIP_SPEAKERS)
        self.turn_off(entities.LIGHT_DRUM_POWER_STRIP_LIGHT)
        self.turn_off(entities.LIGHT_DRUM_POWER_STRIP_USB)
        self.turn_off(entities.LIGHT_DRUM_POWER_STRIP_FOCUSRITE)
        self.turn_off(entities.LIGHT_DRUM_POWER_STRIP_DRUMS)
        self.turn_off(entities.SWITCH_MONITOR)

    def run_for(self, minutes: int, every_minute: Callable[[int], None],
                afterwards: Optional[Callable[[], None]]=None, running_group: Optional[UUID]=None ) -> None:
        """

        :param minutes: For how long this callback should run for, with a minutely frequency
        :param every_minute: Callback to execute every minute, if throws, the timer gets aborted
        :param afterwards: Callback to execute when the loop is over
        :param running_group: If specified, only one job per running group will be executed at once.
               New jobs will make ongoing ones to terminate.
        :return:
        """
        timer = Timer()
        if not running_group:
            running_group = timer.id

        self.timers[running_group] = timer

        def every_minute_callback(*_: Any) -> None:
            if timer.id != self.timers[running_group].id:
                self.log(f'Aborting run_for loop due to newer run for running group', level="INFO")
                return

            minutes_left = self.timers[running_group].minutes_left - 1
            self.log(f'Running scheduled minutely callback. Remaining time: {minutes_left}', level="DEBUG")

            self.timers[running_group].minutes_left = minutes_left

            if minutes_left <= 0:
                del self.timers[running_group]
                if afterwards:
                    afterwards()
                return

            try:
                every_minute(minutes_left)
            except Exception as exc:
                self.log(f'Aborting run_for loop due to exception: {exc}', level="INFO")
                return

            self.run_in(every_minute_callback, 60)
            self.timers[running_group].minutes_left = minutes_left

        self.run_in(every_minute_callback, 60)
        self.timers[running_group].minutes_left = minutes
