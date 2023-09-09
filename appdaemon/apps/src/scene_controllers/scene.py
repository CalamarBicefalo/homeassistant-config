from abc import abstractmethod
from typing import Optional, Dict, Callable, Any

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


class SceneProvider(Scene):
    def get(self) -> Optional[entities.Entity | _Off]:
        p = self.scene_provider()
        if p:
            return p.get()
        return None

    def __init__(self, scene_provider: Callable[[], Optional[Scene]]):
        self.scene_provider = scene_provider


class OffScene(Scene):
    def get(self) -> _Off:
        return _Off()


def by_mode(scenes: Dict[Mode | str, Scene]) -> SceneByModeSelector:
    return SceneByModeSelector(scenes)


def from_entity(scene: entities.Entity) -> Scene:
    return SingleScene(scene)


def with_actions(scene: Optional[Scene], *args: Callable[[], Optional[Any]]) -> Scene:
    def execute_actions() -> Optional[Scene]:
        for action in args:
            action()
        return scene
    return SceneProvider(execute_actions)


def off() -> OffScene:
    return OffScene()
