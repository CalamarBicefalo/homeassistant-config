from enum import StrEnum

class Mode(StrEnum):
    DAY = "Day"
    NIGHT = "Night"
    AWAY = "Away"
    SLEEPING = "Sleeping"


class WashingMachine(StrEnum):
    OFF = "Off"
    WASHING = "Washing"
    DRYING = "Drying"
    WET_CLOTHES_INSIDE = "Wet Clothes Inside"
    MOLD_ALERT = "Mold Alert"

