from datetime import time

import appdaemon.plugins.hass.hassapi as hass


class VacuumController(hass.Hass):

    def initialize(self):
        self.log("Initializing vacuum controller now", level="WARNING")
        self.run_daily(self.clean_kitchen, time(hour=22))

    def clean_kitchen(self, entity, attribute, old, new, kwargs):
        self.log("Cleaning kitchen")
        self.call_service("xiaomi_miio.vacuum_clean_segment", entity_id = "roborock.vacuum.a15", targets = 16)

