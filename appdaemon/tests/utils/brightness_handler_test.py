import pytest
from appdaemontestframework import automation_fixture

import entities
import matchers
from app import App
from brightness_handler import (
    AMBIENT,
    WINDOW_T1,
    Brightness,
    BrightnessHandler,
    calibration_for,
)

WINDOW_SENSOR = entities.SENSOR_LIVING_ROOM_BR
AMBIENT_SENSOR = entities.SENSOR_KITCHEN_MS_ILLUMINANCE


class BrightnessApp(App):
    def initialize(self) -> None:
        pass


@automation_fixture(BrightnessApp)
def app() -> None:
    matchers.init()
    pass


def _window(app):
    return BrightnessHandler(app, WINDOW_SENSOR)


def _ambient(app):
    return BrightnessHandler(app, AMBIENT_SENSOR)


# --- calibration selection ------------------------------------------------

def test_window_sensor_uses_window_calibration(app):
    assert _window(app).calibration is WINDOW_T1


def test_ambient_sensor_uses_ambient_calibration(app):
    assert _ambient(app).calibration is AMBIENT


def test_calibration_for_matches_br_suffix():
    assert calibration_for(entities.Entity("sensor.anything_br")) is WINDOW_T1
    assert calibration_for(entities.Entity("sensor.some_motion_illuminance")) is AMBIENT


def test_explicit_calibration_overrides_inference(app):
    handler = BrightnessHandler(app, WINDOW_SENSOR, AMBIENT)
    assert handler.calibration is AMBIENT


# --- window categories ----------------------------------------------------

@pytest.mark.parametrize("lux,expected", [
    (0, Brightness.DARK),
    (999, Brightness.DARK),
    (1_000, Brightness.CLOUDY),
    (14_999, Brightness.CLOUDY),
    (15_000, Brightness.BRIGHT),
    (49_999, Brightness.BRIGHT),
    (50_000, Brightness.DIRECT_SUNLIGHT),
    (120_000, Brightness.DIRECT_SUNLIGHT),
])
def test_window_get_buckets(given_that, app, lux, expected):
    given_that.state_of(WINDOW_SENSOR).is_set_to(lux)
    assert _window(app).get() is expected


def test_window_semantic_helpers(given_that, app):
    given_that.state_of(WINDOW_SENSOR).is_set_to(70_000)
    handler = _window(app)
    assert handler.has_direct_sunlight()
    assert handler.is_bright()
    assert not handler.is_cloudy()
    assert not handler.is_dark()


# --- ambient categories (much lower scale) --------------------------------

@pytest.mark.parametrize("lux,expected", [
    (0, Brightness.DARK),
    (59, Brightness.DARK),
    (60, Brightness.CLOUDY),
    (199, Brightness.CLOUDY),
    (200, Brightness.BRIGHT),
    (5_000, Brightness.DIRECT_SUNLIGHT),
])
def test_ambient_get_buckets(given_that, app, lux, expected):
    given_that.state_of(AMBIENT_SENSOR).is_set_to(lux)
    assert _ambient(app).get() is expected


# --- lamp decision + hysteresis dead-band ---------------------------------

def test_window_dark_needs_light(given_that, app):
    given_that.state_of(WINDOW_SENSOR).is_set_to(500)
    assert _window(app).needs_artificial_light(lights_currently_on=False)


def test_window_direct_sun_does_not_need_light(given_that, app):
    given_that.state_of(WINDOW_SENSOR).is_set_to(60_000)
    assert not _window(app).needs_artificial_light(lights_currently_on=True)


def test_window_dead_band_keeps_lamps_off_when_off(given_that, app):
    # 5000 lx is between turn_on_below (3000) and allow_off_at (10000):
    # lamps that are off stay off, saving power on a merely-cloudy day.
    given_that.state_of(WINDOW_SENSOR).is_set_to(5_000)
    assert not _window(app).needs_artificial_light(lights_currently_on=False)


def test_window_dead_band_keeps_lamps_on_when_on(given_that, app):
    # Same 5000 lx but the lamps are already on: they stay on (no flapping)
    # until it is clearly bright (>= 10000).
    given_that.state_of(WINDOW_SENSOR).is_set_to(5_000)
    assert _window(app).needs_artificial_light(lights_currently_on=True)


def test_decision_reason_when_dim(given_that, app):
    given_that.state_of(WINDOW_SENSOR).is_set_to(800)
    decision = _window(app).evaluate(lights_currently_on=False)
    assert decision.needs_light
    assert decision.reason == "DARK (800lx < 3000lx) — too dim, lamps wanted"


def test_decision_reason_when_bright(given_that, app):
    given_that.state_of(WINDOW_SENSOR).is_set_to(27_441)
    decision = _window(app).evaluate(lights_currently_on=True)
    assert not decision.needs_light
    assert decision.reason == "BRIGHT (27441lx >= 10000lx) — enough daylight"


def test_ambient_hysteresis_matches_legacy_thresholds(given_that, app):
    handler = _ambient(app)

    given_that.state_of(AMBIENT_SENSOR).is_set_to(100)
    assert not handler.needs_artificial_light(lights_currently_on=False)  # 100 >= 60
    assert handler.needs_artificial_light(lights_currently_on=True)       # 100 < 200

    given_that.state_of(AMBIENT_SENSOR).is_set_to(50)
    assert handler.needs_artificial_light(lights_currently_on=False)      # 50 < 60
