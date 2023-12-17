from app import App


class RoomCleaner(App):

    def initialize(self) -> None:
        for room in self.handlers.rooms.all:
            room.initialize()
