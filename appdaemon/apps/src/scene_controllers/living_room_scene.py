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
                    Mode.SLEEPING: scenes.LIVING_ROOM_READING,
                })
            case activities.LivingRoom.WATCHING_TV:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_MOVIE,
                    Mode.NIGHT: scenes.LIVING_ROOM_MOVIE,
                    Mode.SLEEPING: scenes.LIVING_ROOM_MOVIE,
                })
            case activities.LivingRoom.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scenes.LIVING_ROOM_WELCOME,
                    Mode.NIGHT: scenes.LIVING_ROOM_WELCOME,
                    Mode.SLEEPING: scenes.LIVING_ROOM_WELCOME,
                })

        return scene.off()



