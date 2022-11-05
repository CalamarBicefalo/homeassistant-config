Activity = str
class Common:
    PRESENT : Activity = "Present"
    EMPTY : Activity = "Empty"


class Kitchen(Common):
    COOKING: Activity = "Cooking"


class LivingRoom(Common):
    WATCHING_TV: Activity = "Watching TV"
    READING: Activity = "Reading"


class Studio(Common):
    WORKING: Activity = "Working"
    DRUMMING: Activity = "Drumming"
