import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *
from select_handler import SelectHandler


class StorageRoomController(ActivityController):
    @property
    def activity(self) -> SelectHandler:
        return self.rooms.storage_room.activity

    def initialize(self) -> None:
        self.log(f'Initializing storage room controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [entities.BINARY_SENSOR_STORAGE_ROOM_CS_CONTACT]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs):  # type: ignore
        self.cancel_empty_timer()

        if new == states.OPEN:
            self.activity.set(StorageRoom.Activity.PRESENT)
            self.set_as_empty_in(minutes=10)
        else:
            self.cancel_empty_timer()
            self.activity.set(StorageRoom.Activity.EMPTY)
