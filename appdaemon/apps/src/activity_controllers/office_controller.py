from typing import Any

import entities
from activity_controllers.generic_controller import ActivityController
from rooms import *


class OfficeController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_OFFICE_MOTION
    home_display_id = "388CDA68-6885-B1E3-0857-D6964E3302DB"

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.office.activity

    def initialize(self) -> None:
        super().initialize_lock()
        self.log(f'Initializing office activity controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [
                self.motion_sensor,
                entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_PRIMARY_DISPLAY_ID,
                entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_ACTIVE,
                entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_ACTIVE_AUDIO_INPUT
            ]
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(
            f'Triggering office activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()


        # Work handling
        if self.laptop_at_home() and self.connected_to_monitor():
            self.set_working_or_meeting()
            self.set_as_empty_in(minutes=180)

        # Presence
        elif self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(seconds=10)

    def laptop_at_home(self) -> bool:
        return (self.state.is_value(entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_SSID, 'SETE-2SE-5G')
                and self.state.is_on(entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_ACTIVE))

    def connected_to_monitor(self) -> bool:
        return self.state.is_value(entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_PRIMARY_DISPLAY_ID, self.home_display_id)

    def set_working_or_meeting(self) -> None:
        if (self.state.is_on(entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_AUDIO_INPUT_IN_USE)
            or self.state.is_on(entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_AUDIO_OUTPUT_IN_USE)):
            self.activity.set(Office.Activity.MEETING)
        else:
            self.activity.set(Office.Activity.WORKING)

    def is_working_or_meeting(self) -> bool:
        working: bool = self.activity.is_value(Office.Activity.WORKING)
        meeting: bool = self.activity.is_value(Office.Activity.MEETING)
        return working or meeting
