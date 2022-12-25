from datetime import timedelta
from typing import Any, Optional

import activities
import entities
import helpers
import services
from app import App
from modes import Mode
from music import Playlist, Tune, MusicHandler


class ModeController(App):
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
                self.call_service("cover/close_cover",
                                  entity_id=entities.COVER_BEDROOM_BLINDS)
                self.call_service("cover/close_cover",
                                  entity_id=entities.COVER_BLINDS)
            case Mode.DAY:
                self.call_service("cover/open_cover",
                                  entity_id=entities.COVER_BEDROOM_BLINDS)
                self.call_service("cover/open_cover",
                                  entity_id=entities.COVER_BLINDS)
            case Mode.SLEEPING:
                self.turn_off_media()
                self.turn_off_lights()
                self.turn_off_plugs()
                self.activities.bedroom.set(activities.Bedroom.PRESENT)
                self.bedroom_music.play(Tune.RAIN, volume_level=0.2)

            case Mode.AWAY:
                self.turn_off_media()
                self.turn_off_lights()
                self.turn_off_plugs()
