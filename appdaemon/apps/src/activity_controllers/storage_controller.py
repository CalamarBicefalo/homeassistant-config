import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *


class StorageController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_STORAGE_MS_MOTION
    contact_sensor = entities.BINARY_SENSOR_STORAGE_DOOR_CS
    max_seconds_without_presence_until_empty = 60
    max_seconds_until_empty = 60 * 10

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.storage.activity

    def initialize(self) -> None:
        super().initialize_lock()
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
            f'Triggering storage motion activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")
        self.cancel_empty_timer()

        if self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(seconds=30)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering storage door controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")
        self.cancel_empty_timer()

        if self.activity.is_value(Storage.Activity.EMPTY) and new == states.OPEN:
            self.activity.set(CommonActivities.PRESENT)
