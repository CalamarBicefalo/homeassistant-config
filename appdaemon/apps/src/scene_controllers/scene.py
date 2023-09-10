from abc import abstractmethod
from typing import Optional, Dict, Callable, Any, Tuple

import entities
from modes import Mode


class _Off:
    pass


class Scene:

    @abstractmethod
    def get(self) -> Optional[entities.Entity] | _Off:
        pass


class SceneByModeSelector:

    def get_scene(self, mode: Mode) -> Optional[Scene]:
        if not self.dict:
            return None
        if mode not in self.dict:
            return None
        return self.dict[mode]

    def __init__(self, dict: Dict[Mode | str, Scene]):
        self.dict = dict


class SingleScene(Scene):
    def get(self) -> Optional[entities.Entity]:
        return self.scene

    def __init__(self, scene: entities.Entity):
        self.scene = scene


class SceneWithActions(Scene):
    def get(self) -> Optional[entities.Entity | _Off]:
        if self.scene is None:
            return None
        return self.scene.get()

    def execute_actions(self) -> None:
        for action in self.actions:
            action()

    def __init__(self, scene: Optional[Scene], actions: Tuple[Callable[[], Optional[Any]]]):
        self.scene = scene
        self.actions = actions


class OffScene(Scene):
    def get(self) -> _Off:
        return _Off()


def by_mode(scenes: Dict[Mode | str, Scene]) -> SceneByModeSelector:
    return SceneByModeSelector(scenes)


def from_entity(scene: entities.Entity) -> Scene:
    return SingleScene(scene)


def with_actions(scene: Optional[Scene], *args: Callable[[], Optional[Any]]) -> Scene:
    return SceneWithActions(scene, args)


def off() -> OffScene:
    return OffScene()
