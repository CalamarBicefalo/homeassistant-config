from typing import Any

import entities
import helpers
from app import App
from modes import Mode
from music import Tune, MusicHandler
from rooms import *


class ModeScene(App):
    bedroom_music: MusicHandler

    def initialize(self) -> None:
        self.log(f'Initializing mode controller.', level="DEBUG")
        self.bedroom_music = MusicHandler(self, entities.MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS)

        self.listen_state(
            self.controller_handler,
            helpers.HOMEASSISTANT_MODE
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        match new:
            case Mode.NIGHT:
                self.blinds.close_all()
            case Mode.DAY:
                self.blinds.open_all()
            case Mode.SLEEPING:
                self.turn_off_media()
                self.turn_off_lights()
                self.turn_off_plugs()
                self.rooms.bedroom.activity.set(Bedroom.Activity.PRESENT)
                self.bedroom_music.play(Tune.RAIN, volume_level=0.2)

            case Mode.AWAY:
                self.blinds.open_all()
                self.turn_off_media()
                self.turn_off_lights()
                self.turn_off_plugs()
