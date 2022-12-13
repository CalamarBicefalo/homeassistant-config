import activities
import entities
from app import App


class StorageRoomController(App):
    def initialize(self) -> None:
        self.log(f'Initializing storage room controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [entities.BINARY_SENSOR_STORAGE_ROOM_CS_CONTACT]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs):  # type: ignore
        if self.is_on(entities.BINARY_SENSOR_STORAGE_ROOM_CS_CONTACT):
            self.activities.storageroom.set(activities.StorageRoom.PRESENT)
        else:
            self.activities.storageroom.set(activities.StorageRoom.EMPTY)
