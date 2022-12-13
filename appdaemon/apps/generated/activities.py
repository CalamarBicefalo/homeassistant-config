from helpers import Helper
from strenum import StrEnum
from select_handler import SelectHandler


class Activity(StrEnum):
    pass


class Common(Activity):
    PRESENT = "Present"
    EMPTY = "Empty"


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


class Ensuite(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"
    SHOWERING = "Showering"


class Hallway(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"


class Wardrobe(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"


class Bedroom(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"


class StorageRoom(Activity):
    EMPTY = "Empty"
    PRESENT = "Present"

kitchen_helper = Helper("input_select.kitchen_activity")
livingroom_helper = Helper("input_select.living_room_activity")
studio_helper = Helper("input_select.studio_activity")
ensuite_helper = Helper("input_select.ensuite_activity")
hallway_helper = Helper("input_select.hallway_activity")
wardrobe_helper = Helper("input_select.wardrobe_activity")
bedroom_helper = Helper("input_select.bedroom_activity")
storageroom_helper = Helper("input_select.storage_room_activity")
all_activity_helpers = [kitchen_helper, livingroom_helper, studio_helper, ensuite_helper, hallway_helper, wardrobe_helper, bedroom_helper, storageroom_helper,]
class ActivityHandlers:
    kitchen: SelectHandler[Kitchen]
    livingroom: SelectHandler[LivingRoom]
    studio: SelectHandler[Studio]
    ensuite: SelectHandler[Ensuite]
    hallway: SelectHandler[Hallway]
    wardrobe: SelectHandler[Wardrobe]
    bedroom: SelectHandler[Bedroom]
    storageroom: SelectHandler[StorageRoom]
    def __init__(self, app) -> None:
        self.kitchen = SelectHandler[Kitchen](app, kitchen_helper)
        self.livingroom = SelectHandler[LivingRoom](app, livingroom_helper)
        self.studio = SelectHandler[Studio](app, studio_helper)
        self.ensuite = SelectHandler[Ensuite](app, ensuite_helper)
        self.hallway = SelectHandler[Hallway](app, hallway_helper)
        self.wardrobe = SelectHandler[Wardrobe](app, wardrobe_helper)
        self.bedroom = SelectHandler[Bedroom](app, bedroom_helper)
        self.storageroom = SelectHandler[StorageRoom](app, storageroom_helper)
