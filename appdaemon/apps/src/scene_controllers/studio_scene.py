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
    speakers = entities.MEDIA_PLAYER_COOKING_AREA

    def get_light_scene(self, activity: Studio.Activity) -> Scene:
        match activity:
            case Studio.Activity.WORKING:
                return scenes.STUDIO_WORKING
            case Studio.Activity.DRUMMING:
                return scenes.STUDIO_DRUMMING
            case Studio.Activity.PRESENT:
                return scenes.STUDIO_CONCENTRATE
        return scene.off()

    def on_activity_change(self, activity: Studio.Activity) -> None:
        match activity:
            case Studio.Activity.WORKING:
                self.turn_on(entities.SWITCH_MONITOR)
                if not self.handlers.music.is_playing():
                    self.handlers.music.play(Playlist.random(), volume_level=0.3)
            case Studio.Activity.MEETING:
                self.turn_on(entities.SWITCH_MONITOR)
                self.handlers.music.pause()
            case Studio.Activity.DRUMMING:
                self.turn_off_media()
            case _:
                self.turn_off(entities.SWITCH_MONITOR)
