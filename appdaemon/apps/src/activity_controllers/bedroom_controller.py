import activities
import entities
from activity_controllers.generic_controller import MotionController
from utils.select_handler import SelectHandler


class BedroomController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom

    def initialize(self) -> None:
        self.listen_state(
            self.controller_handler,
            [self.motion_sensor]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering bedroom activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        if self.activity.get() == activities.Bedroom.BEDTIME:
            return

        # Relaxing Handling
        elif self.activity.get() == activities.Bedroom.RELAXING:
            if self.is_on(self.motion_sensor):
                self.set_as_empty_in(minutes=90)
            else:
                self.set_as_empty_in(minutes=30)

        # Presence Handling
        elif self.is_on(self.motion_sensor):
            self.activity.set(activities.Common.PRESENT)

        else:
            self.set_as_empty_in(minutes=1)
