from typing import NewType
Activity = NewType('Activity', str)
class Common:
    EMPTY : Activity = Activity("Empty")
    PRESENT : Activity = Activity("Present")


class Kitchen(Common):
    COOKING: Activity = Activity("Cooking")


class LivingRoom(Common):
    WATCHING_TV: Activity = Activity("Watching TV")
    READING: Activity = Activity("Reading")


class Studio(Common):
    WORKING: Activity = Activity("Working")
    DRUMMING: Activity = Activity("Drumming")


class Ensuite(Common):
    SHOWERING: Activity = Activity("Showering")
