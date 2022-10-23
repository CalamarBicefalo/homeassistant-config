from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import apps.helpers
from apps import devices, services, helpers, activities


class VacuumController(hass.Hass):

    def initialize(self):
        time = "22:30:00"
        self.log(f'Initializing vacuum controller at {time}.', level="INFO")
        self.run_daily(
            self.clean_kitchen,
            time

        )

    async def clean_kitchen(self, kwargs):
        self.log("Triggering kitchen clean task", level="INFO")
        last_cooked = datetime.strptime(str(self.get_state(apps.helpers.LAST_COOKED)), "%Y-%m-%d %H:%M:%S")
        days_since_kitchen_got_dirty = datetime.now() - last_cooked
        if days_since_kitchen_got_dirty.days == 0:
            attempts = 0
            while self.get_state(helpers.LIVING_ROOM_ACTIVITY) == activities.WATCHING_TV and attempts < 12:
                self.log('TV is on, waiting until it is off', level="INFO")
                attempts += 1
                await self.sleep(10*60)
            self.log('Cleaning kitchen', level="INFO")
            self.call_service(
                services.VACUUM_CLEAN_SEGMENT,
                entity_id=devices.VACUUM_CLEANER,
                segments=16
            )
        else:
            self.log(f'Ignoring kitchen clean because we have not cooked for {days_since_kitchen_got_dirty} days.',
                     level="INFO")
