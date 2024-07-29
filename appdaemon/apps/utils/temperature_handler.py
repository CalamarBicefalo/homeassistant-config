from __future__ import annotations

import enum

from appdaemon.plugins.hass import hassapi as hass

import entities
import helpers
from select_handler import SelectHandler
from selects import Mode
from state_handler import StateHandler

COMFORT_INDOOR_MAX_TEMPERATURE = 22
COMFORT_INDOOR_MIN_TEMPERATURE = 19
HOT_OUTSIDE = 25
INDOOR_THERMOMETER = entities.SENSOR_BEDROOM_AIR_QUALITY_TEMPERATURE


class IndoorTemperature(enum.Enum):
    HOT = 0
    COLD = 1
    COMFORTABLE = 2


class TemperatureHandler:
    def __init__(self, app: hass.Hass) -> None:
        self.app = app
        self.state = StateHandler(app)
        self.mode = SelectHandler[Mode](app, helpers.MODE)

    def should_cooldown(self) -> bool:
        match self.get_indoor():
            case IndoorTemperature.COLD:
                return False
            case IndoorTemperature.HOT:
                self.app.log('Should cooldown because it is hot indoors', level="DEBUG")
                return True
            case IndoorTemperature.COMFORTABLE:
                if self.will_be_hot_today():
                    self.app.log('Should cooldown because it will be hot today', level="INFO")
                    return True
                if self.will_be_hot_tomorrow():
                    self.app.log('Should cooldown because it will be hot tomorrow', level="INFO")
                    return True
        return False

    def will_be_hot_today(self) -> bool:
        temperature = self.state.get_as_number(entities.INPUT_NUMBER_MAX_TEMPERATURE_TODAY)
        return temperature and temperature >= HOT_OUTSIDE

    def will_be_hot_tomorrow(self) -> bool:
        temperature = self.state.get_as_number(entities.INPUT_NUMBER_MAX_TEMPERATURE_TOMORROW)
        return temperature and temperature >= HOT_OUTSIDE

    def get_indoor(self) -> IndoorTemperature:
        temperature = self.state.get_as_number(entities.SENSOR_BEDROOM_AIR_QUALITY_TEMPERATURE)
        if temperature and temperature > COMFORT_INDOOR_MAX_TEMPERATURE:
            return IndoorTemperature.HOT
        temperature = self.state.get_as_number(entities.SENSOR_BEDROOM_AIR_QUALITY_TEMPERATURE)
        if temperature and temperature < COMFORT_INDOOR_MIN_TEMPERATURE:
            return IndoorTemperature.COLD

        return IndoorTemperature.COMFORTABLE
