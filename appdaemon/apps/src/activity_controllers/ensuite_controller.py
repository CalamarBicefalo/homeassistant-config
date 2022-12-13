import activities
import entities
import states
from activity_controllers.controller_app import MotionController
from select_handler import SelectHandler


class EnsuiteController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    @property
    def activity(self) -> SelectHandler:
        return self.activities.ensuite


    def initialize(self) -> None:
        self.listen_state(
            self.controller_handler,
            [self.motion_sensor, entities.BINARY_SENSOR_BATHROOM_CS_CONTACT]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering {self.controller} motion based activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(activities.Ensuite.SHOWERING) and entity == self.motion_sensor:
            return

        if entity == self.motion_sensor and new == states.ON and self.is_on(entities.BINARY_SENSOR_BATHROOM_CS_CONTACT):
            self.activity.set(activities.Ensuite.SHOWERING)
            return

        self.handle_presence()
