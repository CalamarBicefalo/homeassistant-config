from room import Room
from helpers import Helper
from strenum import StrEnum
from select_handler import SelectHandler
from appdaemon.plugins.hass import hassapi as hass
from typing import List


class Kitchen(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        COOKING = "Cooking"
        TV_BREAK = "TV Break"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.kitchen_activity"
    name = "Kitchen"
    _room_cleaner_segment = 16
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_kitchen")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[Kitchen.Activity](app, Kitchen._activity_helper)


class LivingRoom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        WATCHING_TV = "Watching TV"
        GAMING = "Gaming"
        READING = "Reading"
        DINNING = "Dinning"
        DRUMMING = "Drumming"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.living_room_activity"
    name = "Living room"
    _room_cleaner_segment = 24
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_living_room")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[LivingRoom.Activity](app, LivingRoom._activity_helper)


class Studio(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        WORKING = "Working"
        DRUMMING = "Drumming"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.studio_activity"
    name = "Studio"
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_studio")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[Studio.Activity](app, Studio._activity_helper)


class Ensuite(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        SHOWERING = "Showering"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.ensuite_activity"
    name = "Ensuite"
    _room_cleaner_segment = 22
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_ensuite")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[Ensuite.Activity](app, Ensuite._activity_helper)


class Hallway(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.hallway_activity"
    name = "Hallway"
    _room_cleaner_segment = 20
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_hallway")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[Hallway.Activity](app, Hallway._activity_helper)


class Wardrobe(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        DRESSING = "Dressing"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.wardrobe_activity"
    name = "Wardrobe"
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_wardrobe")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[Wardrobe.Activity](app, Wardrobe._activity_helper)


class Bedroom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        RELAXING = "Relaxing"
        BEDTIME = "Bedtime"
        WAKING_UP = "Waking up"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.bedroom_activity"
    name = "Bedroom"
    _room_cleaner_segment = 21
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_bedroom")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[Bedroom.Activity](app, Bedroom._activity_helper)


class StorageRoom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"

    activity: SelectHandler[Activity]
    _activity_helper : Helper = "input_select.storage_room_activity"
    name = "Storage room"
    _room_cleaner_segment = 19
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_storage_room")

    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = SelectHandler[StorageRoom.Activity](app, StorageRoom._activity_helper)


class RoomHandlers:
    all: List[Room]
    kitchen: Kitchen
    living_room: LivingRoom
    studio: Studio
    ensuite: Ensuite
    hallway: Hallway
    wardrobe: Wardrobe
    bedroom: Bedroom
    storage_room: StorageRoom
    def __init__(self, app) -> None:
        self.kitchen = Kitchen(app)
        self.living_room = LivingRoom(app)
        self.studio = Studio(app)
        self.ensuite = Ensuite(app)
        self.hallway = Hallway(app)
        self.wardrobe = Wardrobe(app)
        self.bedroom = Bedroom(app)
        self.storage_room = StorageRoom(app)
        self.all = [self.kitchen, self.living_room, self.studio, self.ensuite, self.hallway, self.wardrobe, self.bedroom, self.storage_room]


class CommonActivities(StrEnum):
    EMPTY = "Empty"
    PRESENT = "Present"

