from __future__ import annotations

import enum
from dataclasses import dataclass

import appdaemon.plugins.hass.hassapi as hass

from entities import Entity
from state_handler import StateHandler

# Attribute names on the generated `sensor.<room>_brightness` wrapper sensors
# (see devices/templates/brightness_generated.yaml, generated from windows.yaml).
ILLUMINANCE = "illuminance"
SENSOR_TYPE = "sensor_type"
LIGHTS_ON_BELOW = "lights_on_below"
LIGHTS_OFF_ABOVE = "lights_off_above"
BLINDS_SHADE_ABOVE = "blinds_shade_above"


class Brightness(enum.IntEnum):
    """How much natural light a room is getting, coarsely bucketed.

    Ordered so comparisons work: ``Brightness.CLOUDY < Brightness.BRIGHT``.
    The values mirror the states of the ``sensor.<room>_brightness`` template
    sensors, which are the source of truth for the thresholds.
    """

    DARK = 0
    CLOUDY = 1
    BRIGHT = 2
    DIRECT_SUNLIGHT = 3

    @classmethod
    def from_state(cls, state: str) -> "Brightness":
        try:
            return cls[state.strip().upper()]
        except (KeyError, AttributeError):
            return cls.DARK  # fail safe: unknown/unavailable reads as dark


@dataclass(frozen=True)
class LightDecision:
    """Whether a room needs its lamps, plus the numbers that decided it.

    ``reason`` is a short, log-friendly explanation of the WHY so that a lamp
    turning on/off leaves a breadcrumb ("it got cloudy") rather than looking
    spontaneous.
    """

    needs_light: bool
    brightness: Brightness
    lux: float
    threshold: float

    @property
    def reason(self) -> str:
        if self.needs_light:
            return (f"{self.brightness.name} ({self.lux:.0f}lx < {self.threshold:.0f}lx) "
                    "- too dim, lamps wanted")
        return (f"{self.brightness.name} ({self.lux:.0f}lx >= {self.threshold:.0f}lx) "
                "- enough daylight")


class BrightnessHandler:
    """Reads one ``sensor.<room>_brightness`` wrapper sensor.

    The wrapper (generated from windows.yaml) already classifies the light and
    carries the raw lux, the sensor type and the lamp-hysteresis thresholds as
    attributes, so this handler holds no magic numbers of its own — the
    thresholds live in the DSL.
    """

    def __init__(self, app: hass.Hass, sensor: Entity) -> None:
        self.app = app
        self.state = StateHandler(app)
        self.sensor = sensor

    def get(self) -> Brightness:
        return Brightness.from_state(self.state.get_as_str(self.sensor))

    def lux(self) -> float:
        return self.state.get_attr_as_number(self.sensor, ILLUMINANCE)

    def sensor_type(self) -> str:
        return self.state.get_attr_as_str(self.sensor, SENSOR_TYPE)

    def blinds_shade_above(self) -> float:
        """Lux at/above which the sun is strong enough to shade against."""
        return self.state.get_attr_as_number(self.sensor, BLINDS_SHADE_ABOVE)

    def has_strong_sun(self) -> bool:
        """Is the sun strong enough that shading meaningfully keeps heat out?"""
        return self.lux() >= self.blinds_shade_above()

    def has_direct_sunlight(self) -> bool:
        return self.get() is Brightness.DIRECT_SUNLIGHT

    def is_bright(self) -> bool:
        return self.get() >= Brightness.BRIGHT

    def is_cloudy(self) -> bool:
        return self.get() is Brightness.CLOUDY

    def is_dark(self) -> bool:
        return self.get() is Brightness.DARK

    def evaluate(self, lights_currently_on: bool) -> LightDecision:
        """Decide whether the room needs its lamps, with a legible reason.

        Comfort-first with a hysteresis dead-band to avoid flapping: keep the
        lamps on through ``DARK`` and dim ``CLOUDY``, only letting them off once
        there is ample daylight. ``lights_currently_on`` selects which edge of
        the dead-band applies so the lamps don't toggle on a marginal reading.
        """
        lux = self.lux()
        threshold = self.state.get_attr_as_number(
            self.sensor, LIGHTS_OFF_ABOVE if lights_currently_on else LIGHTS_ON_BELOW)
        return LightDecision(
            needs_light=lux < threshold,
            brightness=self.get(),
            lux=lux,
            threshold=threshold,
        )

    def needs_artificial_light(self, lights_currently_on: bool) -> bool:
        return self.evaluate(lights_currently_on).needs_light
