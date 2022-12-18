import activities
import entities
import states
from app import App


class StorageRoomController(App):
    set_to_away_in_10_minutes = None

    def initialize(self) -> None:
        self.log(f'Initializing storage room controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [entities.BINARY_SENSOR_STORAGE_ROOM_CS_CONTACT]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs):  # type: ignore
        if self.set_to_away_in_10_minutes:
            self.cancel_timer(self.set_to_away_in_10_minutes)
            self.set_to_away_in_10_minutes = None

        if new == states.OPEN:
            self.activities.storageroom.set(activities.StorageRoom.PRESENT)
            self.set_to_away_in_10_minutes = self.run_in(lambda *_: self.activities.storageroom.set(activities.StorageRoom.EMPTY), 600)
        else:
            self.activities.storageroom.set(activities.StorageRoom.EMPTY)
