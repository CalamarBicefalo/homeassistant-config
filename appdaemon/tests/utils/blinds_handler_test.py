from typing import Any

import pytest
from appdaemontestframework import automation_fixture

import entities
import matchers
import services
import states
from app import App
from blinds_handler import BlindsHandler
from temperature_handler import COMFORT_INDOOR_MAX_TEMPERATURE, COMFORT_INDOOR_MIN_TEMPERATURE, INDOOR_THERMOMETER

BLINDS = entities.COVER_LIVING_ROOM_BLINDS
WINDOW = entities.BINARY_SENSOR_LIVING_ROOM_WINDOW_CS_OPENING


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
