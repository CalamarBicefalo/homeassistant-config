from abc import abstractmethod
from typing import Optional, Any

import entities
import helpers
import modes
from app import App
from modes import Mode
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene, OffScene
from select_handler import SelectHandler


class SceneApp(App):

    def initialize(self) -> None:
        self.log(f'Initializing {self.scene} scene.', level="DEBUG")
        if self.activity:
            self.listen_state(
                self.handle_scene,
                self.activity._helper
            )
        if self.illuminance_sensor:
            self.listen_state(
                self.handle_scene,
                self.illuminance_sensor
            )

        self.listen_state(
            self.mode_controller,
            helpers.HOMEASSISTANT_MODE
        )

    @property
    @abstractmethod
    def activity(self) -> SelectHandler:
        pass

    @property
    @abstractmethod
    def illuminance_sensor(self) -> Optional[entities.Entity]:
        pass

    @property
    @abstractmethod
    def room_lights(self) -> entities.Entity:
        pass

    @abstractmethod
    def get_light_scene(self, activity: StrEnum) -> Optional[Scene] | scene.SceneSelector:
        pass

    def on_activity_change(self, activity: StrEnum) -> None:
        pass

    @property
    def scene(self) -> str:
        return self.__class__.__name__

    def handle_scene(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(f'Changing {self.scene} scene {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        activity = self.activity.get()

        if entity == self.activity._helper:
            self.on_activity_change(activity)

        scene_resolver: Optional[Scene] | SceneSelector = self.get_light_scene(activity)
        desired_scene: Optional[Scene] = None
        current_mode = self.handlers.mode.get()
        if type(scene_resolver) == SceneSelector:
            desired_scene = scene_resolver.get_scene(current_mode)
        if isinstance(scene_resolver, Scene):
            desired_scene = scene_resolver

        if type(desired_scene) == OffScene:
            self.turn_off(self.room_lights)
            return

        if not desired_scene:
            if current_mode is Mode.AWAY:
                self.turn_off(self.room_lights)
            return

        if not self.illuminance_sensor:
            self.turn_on(desired_scene.get())
            return

        illuminance = self.get_state_as_number(self.illuminance_sensor)
        lights_on = self.is_on(self.room_lights)
        if current_mode == modes.Mode.NIGHT or ((not lights_on) and illuminance < 40) or (
                lights_on and illuminance < 200):
            self.turn_on(desired_scene.get())
        else:
            self.turn_off(self.room_lights)

    def mode_controller(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.on_mode_change(new, old)

    @abstractmethod
    def on_mode_change(self, new: Mode, old: Mode) -> None:
        pass
