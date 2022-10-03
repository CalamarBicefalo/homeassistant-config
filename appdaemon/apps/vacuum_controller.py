import appdaemon.plugins.hass.hassapi as hass


class VacuumController(hass.Hass):

    def initialize(self):
        time = "22:30:00"
        self.log(f'Initializing vacuum controller at {time}.', level="INFO")
        self.run_daily(
            self.clean_kitchen,
            time

        )

    def clean_kitchen(self, kwargs):
        self.log("Cleaning kitchen", level="INFO")
        self.call_service(
            "xiaomi_miio/vacuum_clean_segment",
            entity_id="vacuum.roborock_vacuum_a15",
            segments=16
        )
