from __future__ import annotations

from typing import Optional

from appdaemon.plugins.hass import hassapi as hass

import entities
import helpers
from selects import Mode
from select_handler import SelectHandler
from state_handler import StateHandler
from entities import Entity

COMFORT_TEMPERATURE = 22

class TemperatureHandler:
    def __init__(self, app: hass.Hass) -> None:
        self.app = app
        self.state = StateHandler(app)
        self.mode = SelectHandler[Mode](app, helpers.MODE)

    def should_cooldown(self) -> bool:
        return self.is_hot_indoors()

    def is_hot_indoors(self) -> bool:
        temperature = self.state.get_as_number(entities.SENSOR_BEDROOM_AIR_QUALITY_TEMPERATURE)
        temperature_higher_than_comfort: bool = temperature and temperature > COMFORT_TEMPERATURE
        return temperature_higher_than_comfort

    def is_cold_indoors(self) -> bool:
        return not self.is_hot_indoors()
