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
from temperature_handler import TemperatureHandler


class BlindsHandler:
    def __init__(self, app: hass.Hass, blinds: Optional[Entity], main_source_of_light: bool = False,
                 window: Optional[Entity] = None, brightness: Optional[BrightnessHandler] = None) -> None:
        self.app = app
        self._blinds = blinds
        self._window = window
        self.state = StateHandler(app)
        self.temperature = TemperatureHandler(app)
        self.mode = SelectHandler[Mode](app, helpers.MODE)
        self.main_source_of_light = main_source_of_light
        self.brightness = brightness

    def open_all(self) -> None:
        self.app.call_service("cover/open_cover",
                              entity_id="all")

    def close_all(self) -> None:
        self.app.call_service("cover/close_cover",
                              entity_id="all")

    def close(self) -> None:
        if self.is_open():
            self.app.call_service("cover/close_cover",
                                  entity_id=self._blinds)

    def open(self) -> None:
        if self.is_closed():
            self.app.call_service("cover/open_cover",
                                  entity_id=self._blinds)

    def best_for_temperature(self) -> None:
        if self.is_day():
            if self.temperature.should_cooldown():
                if self._should_shade():
                    self._shade(self._shade_reason())
                else:
                    self._open(self._open_despite_cooldown_reason())
            else:
                self._open("no cooldown needed")
        else:
            if self.window_is_open() and self.temperature.should_cooldown():
                self._open("night - open window lets the breeze cool the room")
            else:
                self._close("night - no breeze to be had")

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
            self._shade("sunrise on a hot day - keeping the empty room cool")

    def _should_shade(self) -> bool:
        """On a cooldown day, is shading actually worth losing daylight over?"""
        if self.temperature.is_heatwave():
            return True  # heatwave: ignore the leniency, shade as we always did
        if self.brightness is None:
            return True  # no lux reading: be conservative and shade
        return self.brightness.has_strong_sun()

    def _shade_reason(self) -> str:
        if self.temperature.is_heatwave():
            return "cooldown wanted and heatwave - shade regardless of the sun"
        if self.brightness is None:
            return "cooldown wanted and no light reading - shading to be safe"
        return (f"cooldown wanted and strong sun "
                f"({self.brightness.lux():.0f}lx >= "
                f"{self.brightness.blinds_shade_above():.0f}lx)")

    def _open_despite_cooldown_reason(self) -> str:
        # Only reached when it is not a heatwave and the sun is weak, so
        # brightness is always present; guard anyway to keep the type checker happy.
        if self.brightness is None:
            return "cooldown wanted but no light reading - letting daylight in"
        return (f"cooldown wanted but weak sun "
                f"({self.brightness.lux():.0f}lx < "
                f"{self.brightness.blinds_shade_above():.0f}lx) - letting daylight in")

    def _shade(self, reason: str) -> None:
        """Lower for shade, honouring the 30% plant floor."""
        if self.main_source_of_light:
            moving = abs(self.get_position() - 30) >= 1
            self.app.log(f'Blinds: shading to 30% for plants - {reason}.',
                         level="INFO" if moving else "DEBUG")
            self.set_position(30)
        else:
            self._close(reason)

    def _open(self, reason: str) -> None:
        self.app.log(f'Blinds: opening - {reason}.',
                     level="INFO" if self.is_closed() else "DEBUG")
        self.open()

    def _close(self, reason: str) -> None:
        self.app.log(f'Blinds: closing - {reason}.',
                     level="INFO" if self.is_open() else "DEBUG")
        self.close()

    def is_day(self):
        return self.app.sunset() < self.app.sunrise()

    def set_position(self, open_percentage: int | float) -> None:
        self.app.call_service("cover/set_cover_position",
                              entity_id=self._blinds, position=open_percentage)

    def get_position(self) -> float:
        position: float = self.state.get_attr_as_number(self._blinds, "current_position")
        return position

    def is_closed(self) -> bool:
        return self.get_position() <= 0

    def is_open(self) -> bool:
        return self.get_position() >= 1

    def window_is_open(self):
        return self._window and self.state.is_value(self._window, states.OPEN)
