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
        self.handlers.buttons.on_click(COFFEE_TABLE_BUTTON_IEEE_ADDRESS, self.music_manual_override_toggle)
        self.handlers.buttons.on_long_press(COFFEE_TABLE_BUTTON_IEEE_ADDRESS, self.disable_music_manual_override)

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.living_room.activity

    illuminance_sensor = entities.SENSOR_STUDIO_MS_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM
    speakers = entities.MEDIA_PLAYER_COOKING_AREA
    blinds = entities.COVER_BLINDS_CURTAIN
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
                self.handlers.music.play(Playlist.COOL_JAZZ)

            case LivingRoom.Activity.READING:
                if not self.handlers.music.is_playing() and not self.handlers.rooms.studio.activity.is_value(Studio.Activity.WORKING):
                    self.handlers.music.play(Playlist.random())

            case LivingRoom.Activity.WATCHING_TV:
                self.handlers.music.pause()
                self.handlers.blinds.close()

            case LivingRoom.Activity.DRUMMING:
                self.handlers.music.pause()

            case LivingRoom.Activity.GAMING:
                self.handlers.music.pause()
                self.handlers.blinds.close()

            case LivingRoom.Activity.EMPTY:
                self.music_manual_override = False

        mode = self.handlers.mode.get()
        if mode == Mode.NIGHT or mode == Mode.SLEEPING:
            self.handlers.blinds.close()
        else:
            self.handlers.blinds.open()

    def disable_music_manual_override(self) -> None:
        self.music_manual_override = False

    def music_manual_override_toggle(self) -> None:
        self.music_manual_override = True
        self.handlers.music.toggle_play_pause()
