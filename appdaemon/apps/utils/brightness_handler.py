from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Optional

import appdaemon.plugins.hass.hassapi as hass

from entities import Entity
from state_handler import StateHandler


class Brightness(enum.IntEnum):
    """How much natural light a room is getting, coarsely bucketed.

    Ordered so comparisons work: ``Brightness.CLOUDY < Brightness.BRIGHT``.
    """

    DARK = 0
    CLOUDY = 1
    BRIGHT = 2
    DIRECT_SUNLIGHT = 3


@dataclass(frozen=True)
class BrightnessCalibration:
    """Every illuminance threshold for one class of sensor, in lux.

    ``cloudy`` / ``bright`` / ``direct_sunlight`` are the lower bounds of each
    :class:`Brightness` bucket (anything below ``cloudy`` is ``DARK``).

    ``turn_on_below`` / ``allow_off_at`` drive the "do we still need the lamps?"
    decision as a hysteresis dead-band (see
    :meth:`BrightnessHandler.needs_artificial_light`):

    * below ``turn_on_below`` -> too dim, the room wants its lamps on;
    * at/above ``allow_off_at`` -> plenty of daylight, the lamps may go off;
    * in between (the "upper cloudy" band) -> keep whatever the lamps are
      already doing, so a passing cloud can't make them flap on and off.
    """

    cloudy: float
    bright: float
    direct_sunlight: float
    turn_on_below: float
    allow_off_at: float


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
                    "— too dim, lamps wanted")
        return (f"{self.brightness.name} ({self.lux:.0f}lx >= {self.threshold:.0f}lx) "
                "— enough daylight")


# Aqara T1 window brightness sensors (device named "<Room> BR",
# lumi.sen_ill.agl01). They point at the sky through the glass, so they read
# true outdoor-ish lux and are NOT polluted by the room's own lamps: ~0 at
# night, single-digit-thousands under heavy overcast, tens of thousands in
# plain daylight, and 50k-150k in direct sun (observed over 24h).
#
# Because they can't be fooled by the lamps, the hysteresis is purely about not
# flapping as clouds pass: keep the lamps on until there is clearly ample
# daylight (allow_off_at), and only bring them back on once it is genuinely dim
# (turn_on_below) -- biasing toward comfort while still saving power on bright
# days.
WINDOW_T1 = BrightnessCalibration(
    cloudy=1_000,
    bright=15_000,
    direct_sunlight=50_000,
    turn_on_below=3_000,
    allow_off_at=10_000,
)

# Philips Hue and Everything Presence motion sensors reporting room-level
# ambient light. Much lower scale, and crucially polluted by the room's own
# lamps (turning the lamps on raises the reading), hence the asymmetric
# hysteresis: only decide it is dark enough for lamps when quite dim, but keep
# them on until clearly bright. These values reproduce the pre-handler
# behaviour (turn on below 60 lx, stay on until 200 lx).
AMBIENT = BrightnessCalibration(
    cloudy=60,
    bright=200,
    direct_sunlight=1_000,
    turn_on_below=60,
    allow_off_at=200,
)

# Aqara T1 window sensors are named "<room>_br"; everything else is ambient.
_WINDOW_SENSOR_SUFFIX = "_br"


def calibration_for(sensor: Entity) -> BrightnessCalibration:
    """Pick the calibration a sensor should use from its entity id."""
    if str(sensor).endswith(_WINDOW_SENSOR_SUFFIX):
        return WINDOW_T1
    return AMBIENT


class BrightnessHandler:
    """Reads one illuminance sensor and answers questions about the light.

    Constructed with the sensor to read; the calibration is inferred from the
    sensor (Aqara T1 window vs. ambient motion sensor) unless one is passed
    explicitly. All magic numbers live in the :class:`BrightnessCalibration`.
    """

    def __init__(
        self,
        app: hass.Hass,
        sensor: Entity,
        calibration: Optional[BrightnessCalibration] = None,
    ) -> None:
        self.app = app
        self.state = StateHandler(app)
        self.sensor = sensor
        self.calibration = calibration or calibration_for(sensor)

    def lux(self) -> float:
        # Fail safe: a missing/unparseable reading reads as 0 (DARK), so a bad
        # sensor never leaves a room dark by making us think it's bright.
        reading = self.state.get_as_number(self.sensor)
        return reading if reading is not None else 0.0

    def _bucket(self, lux: float) -> Brightness:
        calibration = self.calibration
        if lux >= calibration.direct_sunlight:
            return Brightness.DIRECT_SUNLIGHT
        if lux >= calibration.bright:
            return Brightness.BRIGHT
        if lux >= calibration.cloudy:
            return Brightness.CLOUDY
        return Brightness.DARK

    def get(self) -> Brightness:
        return self._bucket(self.lux())

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
        threshold = (
            self.calibration.allow_off_at
            if lights_currently_on
            else self.calibration.turn_on_below
        )
        return LightDecision(
            needs_light=lux < threshold,
            brightness=self._bucket(lux),
            lux=lux,
            threshold=threshold,
        )

    def needs_artificial_light(self, lights_currently_on: bool) -> bool:
        return self.evaluate(lights_currently_on).needs_light
