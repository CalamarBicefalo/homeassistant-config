from datetime import time

import pytest
from appdaemontestframework import automation_fixture

import entities
import matchers
from app import App
from state_handler import StateHandler


class StateHandlerApp(App):
    def initialize(self) -> None:
        self.state_handler = StateHandler(self)


@automation_fixture(StateHandlerApp)
def app() -> None:
    matchers.init()
    pass


def test_get_as_time_with_hh_mm_format(given_that, app):
    given_that.state_of(entities.INPUT_DATETIME_IOS_ALARM_TIME).is_set_to("09:30")
    
    result = app.state_handler.get_as_time(entities.INPUT_DATETIME_IOS_ALARM_TIME)
    
    assert result == time(hour=9, minute=30)


def test_get_as_time_with_hh_mm_ss_format(given_that, app):
    given_that.state_of(entities.INPUT_DATETIME_IOS_ALARM_TIME).is_set_to("07:55:00")
    
    result = app.state_handler.get_as_time(entities.INPUT_DATETIME_IOS_ALARM_TIME)
    
    assert result == time(hour=7, minute=55)


def test_get_as_time_with_unknown_state(given_that, app):
    given_that.state_of(entities.INPUT_DATETIME_IOS_ALARM_TIME).is_set_to("unknown")
    
    result = app.state_handler.get_as_time(entities.INPUT_DATETIME_IOS_ALARM_TIME)
    
    assert result is None


def test_get_as_time_with_invalid_format(given_that, app):
    given_that.state_of(entities.INPUT_DATETIME_IOS_ALARM_TIME).is_set_to("invalid")
    
    result = app.state_handler.get_as_time(entities.INPUT_DATETIME_IOS_ALARM_TIME)
    
    assert result is None


def test_is_home_when_home(given_that, app):
    given_that.state_of(entities.DEVICE_TRACKER_JC_IPHONE).is_set_to("home")
    
    result = app.state_handler.is_home(entities.DEVICE_TRACKER_JC_IPHONE)
    
    assert result is True


def test_is_home_when_away(given_that, app):
    given_that.state_of(entities.DEVICE_TRACKER_JC_IPHONE).is_set_to("away")
    
    result = app.state_handler.is_home(entities.DEVICE_TRACKER_JC_IPHONE)
    
    assert result is False


def test_is_on_with_on_state(given_that, app):
    given_that.state_of(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED).is_set_to("on")
    
    result = app.state_handler.is_on(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED)
    
    assert result is True


def test_is_on_with_playing_state(given_that, app):
    given_that.state_of("media_player.test").is_set_to("playing")
    
    result = app.state_handler.is_on("media_player.test")
    
    assert result is True


def test_is_on_with_off_state(given_that, app):
    given_that.state_of(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED).is_set_to("off")
    
    result = app.state_handler.is_on(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED)
    
    assert result is False


def test_is_off_with_off_state(given_that, app):
    given_that.state_of(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED).is_set_to("off")
    
    result = app.state_handler.is_off(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED)
    
    assert result is True


def test_is_off_with_on_state(given_that, app):
    given_that.state_of(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED).is_set_to("on")
    
    result = app.state_handler.is_off(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED)
    
    assert result is False


def test_is_value_matches(given_that, app):
    given_that.state_of("sensor.test").is_set_to("idle")
    
    result = app.state_handler.is_value("sensor.test", "idle")
    
    assert result is True


def test_is_value_does_not_match(given_that, app):
    given_that.state_of("sensor.test").is_set_to("active")
    
    result = app.state_handler.is_value("sensor.test", "idle")
    
    assert result is False


def test_get_as_number_with_valid_number(given_that, app):
    given_that.state_of("sensor.temperature").is_set_to("23.5")
    
    result = app.state_handler.get_as_number("sensor.temperature")
    
    assert result == 23.5


def test_get_as_number_with_integer(given_that, app):
    given_that.state_of("sensor.count").is_set_to("42")
    
    result = app.state_handler.get_as_number("sensor.count")
    
    assert result == 42.0
