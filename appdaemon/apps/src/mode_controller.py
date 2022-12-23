from datetime import timedelta
from typing import Any

import entities
import helpers
import services
from app import App
from modes import Mode
from music import Playlist, Tune


class ModeController(App):

    def initialize(self) -> None:
        self.log(f'Initializing mode controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            helpers.HOMEASSISTANT_MODE
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        match new:
            case Mode.BEDTIME:
                self.turn_off(entities.MEDIA_PLAYER_TV)
                self.turn_off(entities.MEDIA_PLAYER_SONY_KD_49XF8096)
                self.turn_on(entities.SCENE_HOME_CORRIDOR)
                self.turn_on(entities.SCENE_BEDROOM_BRIGHT)
                self.turn_on(entities.SWITCH_PREPARE_ME_TO_GO_TO_SLEEP_HUE_LABS_FORMULA)
                self.call_service("cover/close_cover",
                                  entity_id=entities.COVER_BEDROOM_BLINDS)
                self.music.play(Playlist.DISCOVER_WEEKLY, entities.MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS)
                self.run_in(lambda *_: self.turn_off(entities.LIGHT_FULL_LIVING_ROOM), 120)
                self.run_in(lambda *_: self.mode.set(Mode.SLEEPING), 30 * 60)

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
                self.turn_off(entities.MEDIA_PLAYER_TV)
                self.turn_off(entities.SWITCH_DRUMS_PLUG)
                self.turn_off(entities.SWITCH_MONITOR_PLUG)
                self.call_service(services.LIGHT_TURN_OFF, entity_id="all")
                self.music.play(Tune.RAIN, entities.MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS, volume_level=0.2)

            case Mode.AWAY:
                self.call_service(services.LIGHT_TURN_OFF, entity_id="all")
                self.turn_off(entities.MEDIA_PLAYER_HOME)
                self.turn_off(entities.MEDIA_PLAYER_TV)
                self.turn_off(entities.SWITCH_DRUMS_PLUG)
                self.turn_off(entities.SWITCH_MONITOR_PLUG)
