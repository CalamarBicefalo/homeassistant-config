from enum import Enum


class Activity(Enum):
    pass


class Kitchen(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"
    COOKING = "Cooking"


class LivingRoom(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"
    WATCHING_TV = "Watching TV"
    READING = "Reading"


class Studio(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"
    WORKING = "Working"
    DRUMMING = "Drumming"
