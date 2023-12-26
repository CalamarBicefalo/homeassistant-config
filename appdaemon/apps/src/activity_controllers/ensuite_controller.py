import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *
from select_handler import SelectHandler


class EnsuiteController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    contact_sensor = entities.BINARY_SENSOR_ENSUITE_DOOR_CS
    turnoff_time = 60
    present_cooldown = 1500
    shower_cooldown = 2000

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.ensuite.activity

    def initialize(self) -> None:
        self.listen_state(
            self.on_motion,
            self.motion_sensor
        )

        self.listen_state(
            self.on_door,
            self.contact_sensor
        )

    def on_motion(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering ensuite motion activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(Ensuite.Activity.SHOWERING):
            self.set_as_empty_in(self.shower_cooldown)
            return

        if new == states.DETECTED:
            if self.state.is_value(self.contact_sensor, states.CLOSED):
                self.activity.set(Ensuite.Activity.SHOWERING)
                self.set_as_empty_in(self.shower_cooldown)
            else:
                self.activity.set(Ensuite.Activity.PRESENT)
                self.set_as_empty_in(self.present_cooldown)
        else:
            self.set_as_empty_in(self.turnoff_time)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering ensuite door controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(Ensuite.Activity.EMPTY) and new == states.OPEN:
            self.activity.set(CommonActivities.PRESENT)
            self.set_as_empty_in(self.present_cooldown)

        if self.activity.is_value(Ensuite.Activity.SHOWERING):
            self.activity.set(CommonActivities.PRESENT)
            self.set_as_empty_in(self.present_cooldown)

