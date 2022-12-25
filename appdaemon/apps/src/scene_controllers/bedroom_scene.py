from typing import Optional

import activities
import entities
import scenes
import services
from modes import Mode
from music import Playlist
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class BedroomScene(SceneApp):
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM
    speakers = entities.MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS

    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom

    def get_light_scene(self, activity: activities.Activity) -> SceneSelector | Optional[Scene]:
        if activity == activities.Bedroom.RELAXING:
            return scenes.BEDROOM_RELAXING
        if activity == activities.Bedroom.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.BEDROOM_BRIGHT,
                Mode.NIGHT: scenes.BEDROOM_NIGHTLIGHT,
                Mode.SLEEPING: scene.off()
            })
        return scene.off()

    def on_activity_change(self, activity: activities.Activity) -> None:
        if activity == activities.Bedroom.RELAXING:
            self.music.play(Playlist.random(), volume_level=0.3)

        elif activity == activities.Bedroom.BEDTIME:
            # Home cleanup
            self.turn_off_media()
            self.turn_on(entities.SCENE_HOME_CORRIDOR)

            # Bedroom scene
            self.turn_on(entities.SCENE_BEDROOM_BRIGHT)
            self.turn_on(entities.SWITCH_PREPARE_ME_TO_GO_TO_SLEEP_HUE_LABS_FORMULA)
            self.call_service("cover/close_cover",
                              entity_id=entities.COVER_BEDROOM_BLINDS)
            self.music.play(Playlist.DISCOVER_WEEKLY)
            self.run_in(lambda *_: self.turn_off(entities.LIGHT_FULL_LIVING_ROOM), 120)
            self.run_in(lambda *_: self.mode.set(Mode.SLEEPING), 30 * 60)

