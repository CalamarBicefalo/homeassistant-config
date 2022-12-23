import activities
import entities
import scenes
from modes import Mode
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

        return scene.off()

    def on_activity_change(self, activity: activities.Activity) -> None:
        match activity:
            case activities.LivingRoom.DINNING:
                self.music.play("Just Jazz", entities.MEDIA_PLAYER_MASS_COOKING_AREA)

            case activities.LivingRoom.READING:
                self.music.play("Fresh: Jazz Weekly", entities.MEDIA_PLAYER_MASS_COOKING_AREA)

            case activities.LivingRoom.WATCHING_TV:
                self.music.pause(entities.MEDIA_PLAYER_MASS_COOKING_AREA)

        mode = self.mode.get()
        if mode == Mode.NIGHT or mode == Mode.SLEEPING:
            self.call_service("cover/close_cover",
                              entity_id=entities.COVER_BLINDS)
        else:
            self.call_service("cover/open_cover",
                              entity_id=entities.COVER_BLINDS)
