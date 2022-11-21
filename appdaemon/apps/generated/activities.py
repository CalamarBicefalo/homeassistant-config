from typing import NewType
from helpers import Helper
from abc import abstractmethod
Activity = NewType('Activity', str)
class RoomActivity:
    @property
    @abstractmethod
    def helper(self) -> Helper:
        pass
    EMPTY : Activity = Activity("Empty")
    PRESENT : Activity = Activity("Present")


class Kitchen(RoomActivity):
    helper = Helper("input_select.kitchen_activity")
    COOKING: Activity = Activity("Cooking")


class LivingRoom(RoomActivity):
    helper = Helper("input_select.living_room_activity")
    WATCHING_TV: Activity = Activity("Watching TV")
    READING: Activity = Activity("Reading")


class Studio(RoomActivity):
    helper = Helper("input_select.studio_activity")
    WORKING: Activity = Activity("Working")
    DRUMMING: Activity = Activity("Drumming")


class Ensuite(RoomActivity):
    helper = Helper("input_select.ensuite_activity")
    SHOWERING: Activity = Activity("Showering")


class Hallway(RoomActivity):
    helper = Helper("input_select.hallway_activity")
    pass

class Wardrobe(RoomActivity):
    helper = Helper("input_select.wardrobe_activity")
    pass

class Bedroom(RoomActivity):
    helper = Helper("input_select.bedroom_activity")
    pass

class StorageRoom(RoomActivity):
    helper = Helper("input_select.storage_room_activity")
    pass