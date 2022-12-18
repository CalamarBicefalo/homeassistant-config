import activities
import entities
import states
from activity_controllers.controller_app import MotionController
from select_handler import SelectHandler


class EnsuiteController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    contact_sensor = entities.BINARY_SENSOR_BATHROOM_CS_CONTACT

    @property
    def activity(self) -> SelectHandler:
        return self.activities.ensuite

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
            f'Triggering {self.controller} motion based activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(activities.Ensuite.SHOWERING):
            return

        if new == states.DETECTED:
            if self.get_state(self.contact_sensor) == states.CLOSED:
                self.activity.set(activities.Ensuite.SHOWERING)
            else:
                self.activity.set(activities.Ensuite.PRESENT)
        else:
            self.activity.set(activities.Ensuite.EMPTY)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering {self.controller} door based activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(activities.Ensuite.EMPTY) and new == states.CLOSED:
            self.activity.set(activities.Ensuite.EMPTY)
        else:
            self.activity.set(activities.Common.PRESENT)
