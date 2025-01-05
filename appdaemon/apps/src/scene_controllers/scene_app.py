import collections
from abc import abstractmethod
from typing import Optional, Any, cast, Deque, Callable

import entities
import helpers
import selects
from app import App
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneByModeSelector, Scene, SceneWithActions, _Off
from select_handler import SelectHandler
from selects import Mode


class SceneApp(App):
    _scheduled_tasks: Deque[str] = collections.deque()

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
            helpers.MODE
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
    def get_light_scene(self, activity: StrEnum, previous_activity: Optional[StrEnum]) -> Optional[Scene] | scene.SceneByModeSelector:
        pass

    @property
    def scene(self) -> str:
        return self.__class__.__name__

    def handle_scene(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(f'Changing {self.scene} scene {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        activity = self.activity.get()

        self.stop_scheduled_tasks_if_activity(entity)
        previous_activity = None
        if entity == self.activity._helper:
            previous_activity = old

        scene_resolver: Optional[Scene] | SceneByModeSelector = self.get_light_scene(activity, previous_activity)
        unwrapped_scene: Optional[Scene] = None
        desired_scene: Optional[entities.Entity] | _Off = None
        current_mode = self.handlers.mode.get()
        if type(scene_resolver) == SceneByModeSelector:
            unwrapped_scene = scene_resolver.get_scene(current_mode)

        if isinstance(scene_resolver, Scene):
            unwrapped_scene = scene_resolver

        if not unwrapped_scene:
            if current_mode is Mode.AWAY:
                self.turn_off(self.room_lights)
            return

        if entity == self.activity._helper and type(unwrapped_scene) == SceneWithActions:
            cast(SceneWithActions, unwrapped_scene).execute_actions()

        desired_scene = unwrapped_scene.get()

        if type(desired_scene) == _Off:
            self.turn_off(self.room_lights)
            return

        if not self.illuminance_sensor:
            self.turn_on(desired_scene)
            return

        illuminance = self.state.get_as_number(self.illuminance_sensor)
        lights_on = self.state.is_on(self.room_lights)
        if current_mode == selects.Mode.NIGHT or ((not lights_on) and illuminance < 60) or (
                lights_on and illuminance < 200):
            self.turn_on(desired_scene)
        else:
            self.turn_off(self.room_lights)

    def stop_scheduled_tasks_if_activity(self, entity: Helper | str) -> None:
        if entity == self.activity._helper:
            while len(self._scheduled_tasks) > 0:
                task = self._scheduled_tasks.pop()
                if self.timer_running(task):
                    self.cancel_timer(task)

    def run_if_activity_stays_in(self, task: Callable[[], Any], seconds: int = 0, minutes: int = 0) -> None:
        task_id: str = self.run_in(lambda *_: task, seconds + (minutes * 60))
        self._scheduled_tasks.append(task_id)

    def mode_controller(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.on_mode_change(new, old)

    @abstractmethod
    def on_mode_change(self, new: Mode, old: Mode) -> None:
        pass
