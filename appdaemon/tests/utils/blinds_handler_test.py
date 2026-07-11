from typing import Any

import pytest
from appdaemontestframework import automation_fixture

import entities
import matchers
import services
import states
from app import App
from blinds_handler import BlindsHandler
from brightness_handler import BrightnessHandler
from brightness_helpers import set_brightness
from temperature_handler import COMFORT_INDOOR_MAX_TEMPERATURE, COMFORT_INDOOR_MIN_TEMPERATURE, \
    HEATWAVE_MIN_OUTSIDE, INDOOR_THERMOMETER

BLINDS = entities.COVER_LIVING_ROOM_BLINDS
WINDOW = entities.BINARY_SENSOR_LIVING_ROOM_WINDOW_CS_OPENING
BRIGHTNESS_SENSOR = entities.SENSOR_LIVING_ROOM_BRIGHTNESS
SHADE_ABOVE = 5000


class BlindsApp(App):
    def initialize(self) -> None:
        pass


@automation_fixture(BlindsApp)
def app() -> None:
    matchers.init()
    pass


@pytest.fixture
def blinds(app):
    handler = BlindsHandler(app, BLINDS, window=WINDOW)
    handler.is_day = lambda: False  # exercise the night branch deterministically
    return handler


def _given_blinds_at(given_that, position: int) -> None:
    given_that.state_of(BLINDS).is_set_to(
        states.OPEN if position > 0 else states.CLOSED,
        attributes={"current_position": position},
    )


def _day_blinds(app, main_source_of_light: bool = False) -> BlindsHandler:
    handler = BlindsHandler(app, BLINDS, main_source_of_light, WINDOW,
                            BrightnessHandler(app, BRIGHTNESS_SENSOR))
    handler.is_day = lambda: True  # exercise the day branch deterministically
    return handler


def _given_cooldown_day(given_that, lux: int, heatwave: bool = False) -> None:
    """Hot indoors (so we want to cool down), plus a lux reading and heatwave."""
    given_that.state_of(INDOOR_THERMOMETER).is_set_to(COMFORT_INDOOR_MAX_TEMPERATURE + 1)
    min_temp = HEATWAVE_MIN_OUTSIDE if heatwave else HEATWAVE_MIN_OUTSIDE - 1
    given_that.state_of(entities.INPUT_NUMBER_MIN_TEMPERATURE_TODAY).is_set_to(min_temp)
    given_that.state_of(entities.INPUT_NUMBER_MIN_TEMPERATURE_TOMORROW).is_set_to(min_temp)
    set_brightness(given_that, BRIGHTNESS_SENSOR, lux)


@pytest.mark.asyncio
def test_at_night_open_window_keeps_blinds_open_to_let_breeze_in(
        given_that, assert_that: Any, blinds: BlindsHandler) -> None:
    # Nobody in the room, window open at night, indoors too warm -> we want the
    # breeze, so the open blinds must stay open.
    _given_blinds_at(given_that, 100)
    given_that.state_of(WINDOW).is_set_to(states.ON)
    given_that.state_of(INDOOR_THERMOMETER).is_set_to(COMFORT_INDOOR_MAX_TEMPERATURE + 1)

    blinds.best_for_temperature()

    assert_that(services.COVER_CLOSE_COVER).was_not.called_with(entity_id=BLINDS)


@pytest.mark.asyncio
def test_at_night_closed_window_closes_blinds(
        given_that, assert_that: Any, blinds: BlindsHandler) -> None:
    # No breeze to be had with the window shut -> blinds should close at night.
    _given_blinds_at(given_that, 100)
    given_that.state_of(WINDOW).is_set_to(states.OFF)
    given_that.state_of(INDOOR_THERMOMETER).is_set_to(COMFORT_INDOOR_MAX_TEMPERATURE + 1)

    blinds.best_for_temperature()

    assert_that(services.COVER_CLOSE_COVER).was.called_with(entity_id=BLINDS)


@pytest.mark.asyncio
def test_at_sunrise_on_hot_day_lowers_blinds_even_with_open_window(
        given_that, assert_that: Any, blinds: BlindsHandler) -> None:
    # Blinds were left open overnight for the breeze; the sun is now up on a hot
    # day. Sun protection must win -> the blinds come down.
    _given_blinds_at(given_that, 100)
    given_that.state_of(WINDOW).is_set_to(states.ON)
    given_that.state_of(INDOOR_THERMOMETER).is_set_to(COMFORT_INDOOR_MAX_TEMPERATURE + 1)

    blinds.protect_from_sun_if_needed()

    assert_that(services.COVER_CLOSE_COVER).was.called_with(entity_id=BLINDS)


@pytest.mark.asyncio
def test_at_sunrise_on_cool_day_leaves_blinds_open(
        given_that, assert_that: Any, blinds: BlindsHandler) -> None:
    # No need to cool down -> sunrise must not touch the blinds (no surprise
    # opening or closing while the room is still empty / asleep).
    _given_blinds_at(given_that, 100)
    given_that.state_of(WINDOW).is_set_to(states.ON)
    given_that.state_of(INDOOR_THERMOMETER).is_set_to(COMFORT_INDOOR_MIN_TEMPERATURE - 1)

    blinds.protect_from_sun_if_needed()

    assert_that(services.COVER_CLOSE_COVER).was_not.called_with(entity_id=BLINDS)
    assert_that(services.COVER_OPEN_COVER).was_not.called_with(entity_id=BLINDS)


# --- day branch: sun strength vs. daylight --------------------------------

@pytest.mark.asyncio
def test_day_strong_sun_on_cooldown_day_shades(given_that, assert_that: Any, app) -> None:
    # The sun is strong enough that shading keeps real heat out -> close.
    _given_blinds_at(given_that, 100)
    _given_cooldown_day(given_that, lux=SHADE_ABOVE + 2000)

    _day_blinds(app).best_for_temperature()

    assert_that(services.COVER_CLOSE_COVER).was.called_with(entity_id=BLINDS)


@pytest.mark.asyncio
def test_day_weak_sun_on_cooldown_day_opens_for_daylight(given_that, assert_that: Any, app) -> None:
    # Cooldown wanted, but the sun is too weak for shading to help -> let light in.
    _given_blinds_at(given_that, 0)
    _given_cooldown_day(given_that, lux=SHADE_ABOVE - 3000)

    _day_blinds(app).best_for_temperature()

    assert_that(services.COVER_OPEN_COVER).was.called_with(entity_id=BLINDS)
    assert_that(services.COVER_CLOSE_COVER).was_not.called_with(entity_id=BLINDS)


@pytest.mark.asyncio
def test_day_heatwave_shades_even_with_weak_sun(given_that, assert_that: Any, app) -> None:
    # Heatwave disables the weak-sun leniency -> shade as we always did.
    _given_blinds_at(given_that, 100)
    _given_cooldown_day(given_that, lux=SHADE_ABOVE - 3000, heatwave=True)

    _day_blinds(app).best_for_temperature()

    assert_that(services.COVER_CLOSE_COVER).was.called_with(entity_id=BLINDS)


@pytest.mark.asyncio
def test_day_without_brightness_shades_conservatively(given_that, assert_that: Any, app) -> None:
    # No lux reading available -> fall back to the old temperature-only shade.
    _given_blinds_at(given_that, 100)
    given_that.state_of(INDOOR_THERMOMETER).is_set_to(COMFORT_INDOOR_MAX_TEMPERATURE + 1)
    given_that.state_of(entities.INPUT_NUMBER_MIN_TEMPERATURE_TODAY).is_set_to(HEATWAVE_MIN_OUTSIDE - 1)
    given_that.state_of(entities.INPUT_NUMBER_MIN_TEMPERATURE_TOMORROW).is_set_to(HEATWAVE_MIN_OUTSIDE - 1)

    handler = BlindsHandler(app, BLINDS, window=WINDOW)  # no brightness handler
    handler.is_day = lambda: True

    handler.best_for_temperature()

    assert_that(services.COVER_CLOSE_COVER).was.called_with(entity_id=BLINDS)


@pytest.mark.asyncio
def test_day_plant_room_strong_sun_shades_to_30(given_that, assert_that: Any, app) -> None:
    # Plant rooms keep the 30% floor when shading, never fully closing.
    _given_blinds_at(given_that, 100)
    _given_cooldown_day(given_that, lux=SHADE_ABOVE + 2000)

    _day_blinds(app, main_source_of_light=True).best_for_temperature()

    assert_that(services.COVER_SET_COVER_POSITION).was.called_with(entity_id=BLINDS, position=30)


@pytest.mark.asyncio
def test_day_no_cooldown_opens(given_that, assert_that: Any, app) -> None:
    # Comfortable indoors, nothing hot ahead -> open regardless of the sun.
    _given_blinds_at(given_that, 0)
    given_that.state_of(INDOOR_THERMOMETER).is_set_to(COMFORT_INDOOR_MIN_TEMPERATURE + 1)
    given_that.state_of(entities.INPUT_NUMBER_MAX_TEMPERATURE_TODAY).is_set_to(0)
    given_that.state_of(entities.INPUT_NUMBER_MAX_TEMPERATURE_TOMORROW).is_set_to(0)
    set_brightness(given_that, BRIGHTNESS_SENSOR, SHADE_ABOVE + 5000)

    _day_blinds(app).best_for_temperature()

    assert_that(services.COVER_OPEN_COVER).was.called_with(entity_id=BLINDS)
