import entities
import scenes
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class StudioScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.studio.activity

    illuminance_sensor = entities.SENSOR_STUDIO_MS_ILLUMINANCE
    room_lights = entities.LIGHT_STUDIO
    speakers = entities.MEDIA_PLAYER_COOKING_AREA_2

    def get_light_scene(self, activity: Studio.Activity) -> Scene:
        match activity:
            case Studio.Activity.WORKING:
                return scene.with_actions(
                    scenes.STUDIO_WORKING,
                    lambda: self.turn_on(entities.SWITCH_MONITOR),
                    lambda: self.play_music_if_appropriate(),
                )

            case Studio.Activity.MEETING:
                return scene.with_actions(
                    scenes.STUDIO_WORKING,
                    lambda: self.turn_on(entities.SWITCH_MONITOR),
                    lambda: self.handlers.music.pause(),
                )

            case Studio.Activity.DRUMMING:
                return scene.with_actions(
                    scenes.STUDIO_DRUMMING,
                    lambda: self.turn_off_media(),
                )

            case Studio.Activity.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scenes.STUDIO_CONCENTRATE,
                    Mode.NIGHT: scenes.STUDIO_CONCENTRATE,
                })

        return scene.with_actions(
            scene.off(),
            lambda: self.turn_off(entities.SWITCH_MONITOR)
        )


    def play_music_if_appropriate(self) -> None:
        if not self.handlers.music.is_playing():
            self.handlers.music.play(Playlist.random(), volume_level=0.3)
