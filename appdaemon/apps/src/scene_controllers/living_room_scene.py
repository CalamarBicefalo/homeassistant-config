
import activities
import entities
import scenes
from modes import Mode
from music import Playlist
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class LivingRoomScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.activities.livingroom

    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM
    speakers = entities.MEDIA_PLAYER_MASS_COOKING_AREA

    def get_light_scene(self, activity: activities.Activity) -> Scene | SceneSelector:
        match activity:
            case activities.LivingRoom.READING:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_READING,
                    Mode.NIGHT: scenes.LIVING_ROOM_READING,
                })
            case activities.LivingRoom.WATCHING_TV:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_MOVIE,
                    Mode.NIGHT: scenes.LIVING_ROOM_MOVIE,
                })
            case activities.LivingRoom.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_WELCOME,
                    Mode.NIGHT: scenes.LIVING_ROOM_WELCOME,
                })
            case activities.LivingRoom.DINNING:
                return scenes.DINING_ROOM_DINNER_TIME
            case activities.LivingRoom.DRUMMING:
                return scenes.LIVING_ROOM_DRUMMING
            case activities.LivingRoom.GAMING:
                return scenes.LIVING_ROOM_GAMING

        return scene.off()

    def on_activity_change(self, activity: activities.Activity) -> None:
        match activity:
            case activities.LivingRoom.DINNING:
                self.music.play(Playlist.COOL_JAZZ)

            case activities.LivingRoom.READING:
                if not self.is_on(self.speakers):
                    self.music.play(Playlist.random())

            case activities.LivingRoom.WATCHING_TV:
                self.music.pause()

            case activities.LivingRoom.DRUMMING:
                self.music.pause()

            case activities.LivingRoom.GAMING:
                self.music.pause()

        mode = self.mode.get()
        if mode == Mode.NIGHT or mode == Mode.SLEEPING:
            self.blinds.close(entities.COVER_BLINDS)
        else:
            self.blinds.open(entities.COVER_BLINDS)
