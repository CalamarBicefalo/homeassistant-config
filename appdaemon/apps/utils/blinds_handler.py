from __future__ import annotations

from typing import Optional

from appdaemon.plugins.hass import hassapi as hass

import helpers
import states
from brightness_handler import BrightnessHandler
from entities import Entity
from select_handler import SelectHandler
from selects import Mode
from state_handler import StateHandler
from status_handler import StatusHandler
from temperature_handler import TemperatureHandler


class BlindsHandler:
    def __init__(self, app: hass.Hass, blinds: Optional[Entity], main_source_of_light: bool = False,
                 window: Optional[Entity] = None, brightness: Optional[BrightnessHandler] = None,
                 status: Optional[StatusHandler] = None) -> None:
        self.app = app
        self._blinds = blinds
        self._window = window
        self.state = StateHandler(app)
        self.temperature = TemperatureHandler(app)
        self.mode = SelectHandler[Mode](app, helpers.MODE)
        self.main_source_of_light = main_source_of_light
        self.brightness = brightness
        self.status = status

    def open_all(self) -> None:
        self.app.call_service("cover/open_cover",
                              entity_id="all")

    def close_all(self) -> None:
        self.app.call_service("cover/close_cover",
                              entity_id="all")

    def close(self, reason: str = "the current scene calls for them closed") -> None:
        if self.is_open():
            self.app.call_service("cover/close_cover",
                                  entity_id=self._blinds)
        self._publish_status("Closed", reason)

    def open(self, reason: str = "the current scene calls for them open") -> None:
        if self.is_closed():
            self.app.call_service("cover/open_cover",
                                  entity_id=self._blinds)
        self._publish_status("Open", reason)

    def best_for_temperature(self) -> None:
        if self.is_day():
            if self.temperature.should_cooldown():
                if self._should_shade():
                    self._shade(self._shade_reason())
                else:
                    self._open(self._open_despite_cooldown_reason())
            else:
                self._open("the room doesn't need cooling")
        else:
            if self.window_is_open() and self.temperature.should_cooldown():
                self._open("the night breeze is cooling the room")
            else:
                self._close("it's night and there's no breeze to catch")

    def protect_from_sun_if_needed(self) -> None:
        """Lower the blinds when the sun comes up on a hot day.

        best_for_temperature() can leave the blinds open overnight so an open
        window lets the breeze in. Nothing re-evaluates them at sunrise (the
        mode stays NIGHT/SLEEPING until someone is around), so this is run at
        sunrise to keep the sun out of a hot room. It only ever lowers the
        blinds — it never opens them. The empty room needs no daylight, so the
        weak-sun leniency of best_for_temperature() deliberately does not apply.
        """
        if self.temperature.should_cooldown():
            self._shade("the sun is up and the empty room needs to stay cool")

    def _should_shade(self) -> bool:
        """On a cooldown day, is shading actually worth losing daylight over?"""
        if self.temperature.is_heatwave():
            return True  # heatwave: ignore the leniency, shade as we always did
        if self.brightness is None:
            return True  # no lux reading: be conservative and shade
        return self.brightness.has_strong_sun()

    def _shade_reason(self) -> str:
        if self.temperature.is_heatwave():
            return "there's a heatwave and it shades no matter the sun"
        if self.brightness is None:
            return "there's no light reading and it shades to be safe"
        return "the sun is strong enough to be worth shading against"

    def _open_despite_cooldown_reason(self) -> str:
        # Only reached when it is not a heatwave and the sun is weak, so
        # brightness is always present; guard anyway to keep the type checker happy.
        if self.brightness is None:
            return "there's no light reading, so it lets daylight in"
        return "the sun is too weak to be worth shading against"

    def _shade(self, reason: str) -> None:
        """Lower for shade, honouring the 30% plant floor."""
        if self.main_source_of_light:
            moving = abs(self.get_position() - 30) >= 1
            self.app.log(f'Blinds: shading to 30% for plants - {reason}.',
                         level="INFO" if moving else "DEBUG")
            self.set_position(30, reason)
        else:
            self._close(reason)

    def _open(self, reason: str) -> None:
        self.app.log(f'Blinds: opening - {reason}.',
                     level="INFO" if self.is_closed() else "DEBUG")
        self.open(reason)

    def _close(self, reason: str) -> None:
        self.app.log(f'Blinds: closing - {reason}.',
                     level="INFO" if self.is_open() else "DEBUG")
        self.close(reason)

    def is_day(self):
        return self.app.sunset() < self.app.sunrise()

    def set_position(self, open_percentage: int | float,
                     reason: str = "the current scene set them there") -> None:
        self.app.call_service("cover/set_cover_position",
                              entity_id=self._blinds, position=open_percentage)
        self._publish_status(self._position_word(open_percentage), reason)

    @staticmethod
    def _position_word(open_percentage: int | float) -> str:
        if open_percentage <= 0:
            return "Closed"
        if open_percentage >= 95:
            return "Open"
        return "Partially closed"

    def _publish_status(self, state: str, reason: str) -> None:
        if self.status is not None:
            self.status.publish_blinds(state, reason)

    def report_current(self) -> None:
        """Seed the status sensor from the current position (e.g. at startup),
        so the card isn't empty until the first open/close/shade."""
        self._publish_status(self._position_word(self.get_position()),
                             "that's how they're currently set")

    def get_position(self) -> float:
        position: float = self.state.get_attr_as_number(self._blinds, "current_position")
        return position

    def is_closed(self) -> bool:
        return self.get_position() <= 0

    def is_open(self) -> bool:
        return self.get_position() >= 1

    def window_is_open(self):
        return self._window and self.state.is_value(self._window, states.OPEN)
