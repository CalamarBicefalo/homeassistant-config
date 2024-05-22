from typing import Any

import pytest
from appdaemontestframework import automation_fixture, given_that as given

import entities
import matchers
from app import App
from temperature_handler import TemperatureHandler, INDOOR_THERMOMETER, IndoorTemperature, \
    COMFORT_INDOOR_MAX_TEMPERATURE, COMFORT_INDOOR_MIN_TEMPERATURE, HOT_OUTSIDE


class TemperatureApp(App):
    def initialize(self) -> None:
        pass


@automation_fixture(TemperatureApp)
def app() -> None:
    matchers.init()
    pass

@pytest.fixture
def temperature(app):
    return TemperatureHandler(app)

@pytest.mark.asyncio
def test_when_cold_should_not_cooldown(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MIN_TEMPERATURE-1)
    assert temperature.should_cooldown() is False

@pytest.mark.asyncio
def test_when_cold_should_not_cooldown_even_if_hot_outside_today_or_tomorrow(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MIN_TEMPERATURE-1, outdoors_today=HOT_OUTSIDE+1,  outdoors_tomorrow=HOT_OUTSIDE+1)
    assert temperature.should_cooldown() is False

@pytest.mark.asyncio
def test_when_hot_inside_should_cooldown(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MAX_TEMPERATURE+1)
    assert temperature.should_cooldown() is True

@pytest.mark.asyncio
def test_when_hot_should_cooldown_even_if_cold_outside_today_or_tomorrow(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MIN_TEMPERATURE-1, outdoors_today=0,  outdoors_tomorrow=0)
    assert temperature.should_cooldown() is False

@pytest.mark.asyncio
def test_when_comfortable_inside_and_cold_outside_should_not_cooldown(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MIN_TEMPERATURE+1)
    assert temperature.should_cooldown() is False

@pytest.mark.asyncio
def test_when_comfortable_inside_and_hot_today_should_cooldown(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MIN_TEMPERATURE+1, outdoors_today=HOT_OUTSIDE)
    assert temperature.should_cooldown() is True

@pytest.mark.asyncio
def test_when_comfortable_inside_and_hot_today_should_cooldown(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MIN_TEMPERATURE+1, outdoors_tomorrow=HOT_OUTSIDE)
    assert temperature.should_cooldown() is True

@pytest.mark.asyncio
def test_when_indoor_temperature_is_comfortable(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MAX_TEMPERATURE-1)
    assert temperature.get_indoor() is IndoorTemperature.COMFORTABLE

@pytest.mark.asyncio
def test_when_indoor_temperature_is_hot(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MAX_TEMPERATURE+1)
    assert temperature.get_indoor() is IndoorTemperature.HOT

@pytest.mark.asyncio
def test_when_indoor_temperature_is_cold(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(indoors=COMFORT_INDOOR_MIN_TEMPERATURE-1)
    assert temperature.get_indoor() is IndoorTemperature.COLD

@pytest.mark.asyncio
def test_when_will_be_hot_today(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(outdoors_today=HOT_OUTSIDE+1)
    assert temperature.will_be_hot_today() is True

@pytest.mark.asyncio
def test_when_wont_be_hot_today(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(outdoors_today=HOT_OUTSIDE - 1)
    assert temperature.will_be_hot_today() is False

@pytest.mark.asyncio
def test_when_will_be_hot_tomorrow(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(outdoors_tomorrow=HOT_OUTSIDE+1)
    assert temperature.will_be_hot_tomorrow() is True

@pytest.mark.asyncio
def test_when_wont_be_hot_tomorrow(given_that, assert_that: Any, temperature: TemperatureHandler) -> None:
    given_that.temperature_is(outdoors_tomorrow=HOT_OUTSIDE-1)
    assert temperature.will_be_hot_tomorrow() is False

def temperature_is(self, indoors=20, outdoors_today=20, outdoors_tomorrow=20):
    self.state_of(INDOOR_THERMOMETER).is_set_to(indoors)
    self.state_of(entities.INPUT_NUMBER_MAX_TEMPERATURE_TODAY).is_set_to(outdoors_today)
    self.state_of(entities.INPUT_NUMBER_MAX_TEMPERATURE_TOMORROW).is_set_to(outdoors_tomorrow)

given.GivenThatWrapper.temperature_is = temperature_is
