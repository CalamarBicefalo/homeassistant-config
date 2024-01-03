from room import Room
from helpers import Helper
from enum import StrEnum
from activity_handler import ActivityHandler
from select_handler import SelectHandler
from appdaemon.plugins.hass import hassapi as hass
from typing import List


class Office(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.office_activity"
    name = "Office"
    _room_cleaner_segment = 17
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_office")
    _last_present_helper = Helper("input_datetime.last_present_office")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Office.Activity](app, Office._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class Bathroom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.bathroom_activity"
    name = "Bathroom"
    _room_cleaner_segment = 18
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_bathroom")
    _last_present_helper = Helper("input_datetime.last_present_bathroom")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Bathroom.Activity](app, Bathroom._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class Kitchen(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        COOKING = "Cooking"
        TV_BREAK = "TV Break"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 1
    clean_after: int = 21

    _activity_helper : Helper = "input_select.kitchen_activity"
    name = "Kitchen"
    _room_cleaner_segment = 16
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_kitchen")
    _last_present_helper = Helper("input_datetime.last_present_kitchen")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Kitchen.Activity](app, Kitchen._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class DiningRoom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        DINNING = "Dinning"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.dining_room_activity"
    name = "Dining room"
    _room_cleaner_segment = 25
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_dining_room")
    _last_present_helper = Helper("input_datetime.last_present_dining_room")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[DiningRoom.Activity](app, DiningRoom._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class LivingRoom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        WATCHING_TV = "Watching TV"
        GAMING = "Gaming"
        READING = "Reading"
        RELAXING = "Relaxing"
        DRUMMING = "Drumming"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.living_room_activity"
    name = "Living room"
    _room_cleaner_segment = 24
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_living_room")
    _last_present_helper = Helper("input_datetime.last_present_living_room")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[LivingRoom.Activity](app, LivingRoom._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class Studio(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        WORKING = "Working"
        MEETING = "Meeting"
        DRUMMING = "Drumming"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 2
    clean_after: int = -1

    _activity_helper : Helper = "input_select.studio_activity"
    name = "Studio"
    _room_cleaner_segment = 23
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_studio")
    _last_present_helper = Helper("input_datetime.last_present_studio")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Studio.Activity](app, Studio._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class Ensuite(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        SHOWERING = "Showering"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.ensuite_activity"
    name = "Ensuite"
    _room_cleaner_segment = 22
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_ensuite")
    _last_present_helper = Helper("input_datetime.last_present_ensuite")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Ensuite.Activity](app, Ensuite._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class Hallway(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.hallway_activity"
    name = "Hallway"
    _room_cleaner_segment = 20
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_hallway")
    _last_present_helper = Helper("input_datetime.last_present_hallway")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Hallway.Activity](app, Hallway._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class Wardrobe(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        DRESSING = "Dressing"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.wardrobe_activity"
    name = "Wardrobe"
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_wardrobe")
    _last_present_helper = Helper("input_datetime.last_present_wardrobe")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Wardrobe.Activity](app, Wardrobe._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class Bedroom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"
        RELAXING = "Relaxing"
        BEDTIME = "Bedtime"
        WAKING_UP = "Waking up"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.bedroom_activity"
    name = "Bedroom"
    _room_cleaner_segment = 21
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_bedroom")
    _last_present_helper = Helper("input_datetime.last_present_bedroom")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[Bedroom.Activity](app, Bedroom._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity

class StorageRoom(Room):
    class Activity(StrEnum):
        EMPTY = "Empty"
        PRESENT = "Present"

    activity: SelectHandler[Activity]
    days_between_cleaning: int = 0
    clean_after: int = -1

    _activity_helper : Helper = "input_select.storage_room_activity"
    name = "Storage room"
    _room_cleaner_segment = 19
    _last_cleaned_helper = Helper("input_datetime.last_cleaned_storage_room")
    _last_present_helper = Helper("input_datetime.last_present_storage_room")
    def __init__(self, app: hass.Hass) -> None:
        super().__init__(app)
        self.activity = ActivityHandler[StorageRoom.Activity](app, StorageRoom._activity_helper)

    def get_activity(self) -> SelectHandler[Activity]:
        return self.activity


class RoomHandlers:
    all: List[Room]
    office: Office
    bathroom: Bathroom
    kitchen: Kitchen
    dining_room: DiningRoom
    living_room: LivingRoom
    studio: Studio
    ensuite: Ensuite
    hallway: Hallway
    wardrobe: Wardrobe
    bedroom: Bedroom
    storage_room: StorageRoom
    def __init__(self, app) -> None:
        self.office = Office(app)
        self.bathroom = Bathroom(app)
        self.kitchen = Kitchen(app)
        self.dining_room = DiningRoom(app)
        self.living_room = LivingRoom(app)
        self.studio = Studio(app)
        self.ensuite = Ensuite(app)
        self.hallway = Hallway(app)
        self.wardrobe = Wardrobe(app)
        self.bedroom = Bedroom(app)
        self.storage_room = StorageRoom(app)
        
        self.kitchen.open_floor_rooms = [
            self.dining_room,
            self.living_room,
            self.studio,
        ]
        self.dining_room.open_floor_rooms = [
            self.kitchen,
            self.living_room,
            self.studio,
        ]
        self.living_room.open_floor_rooms = [
            self.kitchen,
            self.dining_room,
            self.studio,
        ]
        self.studio.open_floor_rooms = [
            self.kitchen,
            self.dining_room,
            self.living_room,
        ]
        self.wardrobe.open_floor_rooms = [
            self.bedroom,
        ]
        self.bedroom.open_floor_rooms = [
            self.wardrobe,
        ]

        self.all = [
            self.office,
            self.bathroom,
            self.kitchen,
            self.dining_room,
            self.living_room,
            self.studio,
            self.ensuite,
            self.hallway,
            self.wardrobe,
            self.bedroom,
            self.storage_room,
        ]



class CommonActivities(StrEnum):
        PRESENT = "Present"
        EMPTY = "Empty"
