import entities
import scenes
from activity_controllers.living_room_controller import COFFEE_TABLE_BUTTON_IEEE_ADDRESS
from modes import Mode
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class LivingRoomScene(SceneApp):

    def initialize(self) -> None:
        super().initialize()
        self.buttons.on_click(COFFEE_TABLE_BUTTON_IEEE_ADDRESS, self.music_manual_override_toggle)

    @property
    def activity(self) -> SelectHandler:
        return self.rooms.living_room.activity

    illuminance_sensor = entities.SENSOR_STUDIO_MS_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM
    speakers = entities.MEDIA_PLAYER_MASS_COOKING_AREA
    music_manual_override = False

    def get_light_scene(self, activity: LivingRoom.Activity) -> Scene | SceneSelector:
        match activity:
            case LivingRoom.Activity.READING:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_READING,
                    Mode.NIGHT: scenes.LIVING_ROOM_READING,
                })
            case LivingRoom.Activity.WATCHING_TV:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_MOVIE,
                    Mode.NIGHT: scenes.LIVING_ROOM_MOVIE,
                })
            case LivingRoom.Activity.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_WELCOME,
                    Mode.NIGHT: scenes.LIVING_ROOM_WELCOME,
                })
            case LivingRoom.Activity.DINNING:
                return scenes.DINING_ROOM_DINNER_TIME
            case LivingRoom.Activity.DRUMMING:
                return scenes.LIVING_ROOM_DRUMMING
            case LivingRoom.Activity.GAMING:
                return scenes.LIVING_ROOM_GAMING

        return scene.off()

    def on_activity_change(self, activity: LivingRoom.Activity) -> None:
        match activity:
            case LivingRoom.Activity.DINNING:
                self.music.play(Playlist.COOL_JAZZ)

            case LivingRoom.Activity.READING:
                if not self.music.is_playing() and not self.rooms.studio.activity.is_value(Studio.Activity.WORKING):
                    self.music.play(Playlist.random())

            case LivingRoom.Activity.WATCHING_TV:
                self.music.pause()

            case LivingRoom.Activity.DRUMMING:
                self.music.pause()

            case LivingRoom.Activity.GAMING:
                self.music.pause()

            case LivingRoom.Activity.EMPTY:
                self.music_manual_override = False

        mode = self.mode.get()
        if mode == Mode.NIGHT or mode == Mode.SLEEPING:
            self.blinds.close(entities.COVER_BLINDS_CURTAIN)
        else:
            self.blinds.open(entities.COVER_BLINDS_CURTAIN)

    def music_manual_override_toggle(self) -> None:
        self.music_manual_override = True
        self.music.toggle_play_pause()
