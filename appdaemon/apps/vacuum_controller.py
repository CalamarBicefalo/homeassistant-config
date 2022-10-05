from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

from apps import entities


class VacuumController(hass.Hass):

    def initialize(self):
        time = "22:30:00"
        self.log(f'Initializing vacuum controller at {time}.', level="INFO")
        self.run_daily(
            self.clean_kitchen,
            time

        )

    def clean_kitchen(self, kwargs):
        self.log("Triggering kitchen clean task", level="INFO")
        last_cooked = datetime.strptime(str(self.get_state(entities.HELPER_LAST_COOKED)), "%Y-%m-%d %H:%M:%S")
        days_since_kitchen_got_dirty = datetime.now() - last_cooked
        if days_since_kitchen_got_dirty.days == 0:
            self.log('Cleaning kitchen', level="INFO")
            self.call_service(
                "xiaomi_miio/vacuum_clean_segment",
                entity_id=entities.DEVICE_VACUUM_CLEANER,
                segments=16
            )
        else:
            self.log(f'Ignoring kitchen clean because we have not cooked for {days_since_kitchen_got_dirty} days.',
                     level="INFO")
