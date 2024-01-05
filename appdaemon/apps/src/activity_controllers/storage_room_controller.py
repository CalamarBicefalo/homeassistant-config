import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *
from select_handler import SelectHandler


class StorageRoomController(ActivityController):
    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.storage.activity

    def initialize(self) -> None:
        super().initialize_lock()
        self.log(f'Initializing storage room controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [entities.BINARY_SENSOR_STORAGE_DOOR_CS]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs):  # type: ignore
        self.cancel_empty_timer()

        if new == states.OPEN:
            self.activity.set(Storage.Activity.PRESENT)
        else:
            self.cancel_empty_timer()
            self.activity.set(Storage.Activity.EMPTY)
