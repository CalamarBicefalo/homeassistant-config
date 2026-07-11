import pytest
from appdaemontestframework import automation_fixture

import entities
import matchers
from app import App
from brightness_handler import Brightness, BrightnessHandler

SENSOR = entities.SENSOR_OFFICE_BRIGHTNESS


class BrightnessApp(App):
    def initialize(self) -> None:
        pass


@automation_fixture(BrightnessApp)
def app() -> None:
    matchers.init()
    pass


def _handler(app):
    return BrightnessHandler(app, SENSOR)


def _set(given_that, state, illuminance, turn_on_below=1500, allow_off_at=4000):
    given_that.state_of(SENSOR).is_set_to(state, {
        "illuminance": illuminance,
        "sensor_type": "window",
        "turn_on_below": turn_on_below,
        "allow_off_at": allow_off_at,
    })


# --- reading state / attributes ------------------------------------------

@pytest.mark.parametrize("state,expected", [
    ("dark", Brightness.DARK),
    ("cloudy", Brightness.CLOUDY),
    ("bright", Brightness.BRIGHT),
    ("direct_sunlight", Brightness.DIRECT_SUNLIGHT),
])
def test_get_reads_category_from_state(given_that, app, state, expected):
    _set(given_that, state, 5000)
    assert _handler(app).get() is expected


def test_unknown_state_fails_safe_to_dark(given_that, app):
    _set(given_that, "unavailable", 0)
    assert _handler(app).get() is Brightness.DARK


def test_lux_and_type_read_from_attributes(given_that, app):
    _set(given_that, "bright", 27441)
    handler = _handler(app)
    assert handler.lux() == 27441
    assert handler.sensor_type() == "window"


def test_semantic_helpers(given_that, app):
    _set(given_that, "direct_sunlight", 60000)
    handler = _handler(app)
    assert handler.has_direct_sunlight()
    assert handler.is_bright()
    assert not handler.is_cloudy()
    assert not handler.is_dark()


# --- lamp decision + hysteresis dead-band ---------------------------------

def test_dim_needs_light(given_that, app):
    _set(given_that, "dark", 500)
    assert _handler(app).needs_artificial_light(lights_currently_on=False)


def test_direct_sun_does_not_need_light(given_that, app):
    _set(given_that, "direct_sunlight", 60000)
    assert not _handler(app).needs_artificial_light(lights_currently_on=True)


def test_dead_band_keeps_lamps_off_when_off(given_that, app):
    # 2500 lx is between turn_on_below (1500) and allow_off_at (4000):
    # lamps that are off stay off.
    _set(given_that, "cloudy", 2500)
    assert not _handler(app).needs_artificial_light(lights_currently_on=False)


def test_dead_band_keeps_lamps_on_when_on(given_that, app):
    # Same 2500 lx, lamps already on: they stay on until clearly bright.
    _set(given_that, "cloudy", 2500)
    assert _handler(app).needs_artificial_light(lights_currently_on=True)


# --- decision reason (the WHY logs) ---------------------------------------

def test_decision_reason_when_dim(given_that, app):
    _set(given_that, "dark", 800)
    decision = _handler(app).evaluate(lights_currently_on=False)
    assert decision.needs_light
    assert decision.reason == "DARK (800lx < 1500lx) — too dim, lamps wanted"


def test_decision_reason_when_bright(given_that, app):
    _set(given_that, "bright", 27441)
    decision = _handler(app).evaluate(lights_currently_on=True)
    assert not decision.needs_light
    assert decision.reason == "BRIGHT (27441lx >= 4000lx) — enough daylight"
