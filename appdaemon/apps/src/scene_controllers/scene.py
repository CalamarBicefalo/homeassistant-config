from abc import abstractmethod
from typing import Optional, Dict

import entities
from modes import Mode


class _Off:
    pass


class Scene:

    @abstractmethod
    def get(self) -> Optional[entities.Entity] | _Off:
        pass


class SceneSelector:

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


class OffScene(Scene):
    def get(self) -> _Off:
        return _Off()


def by_mode(scenes: Dict[Mode | str, Scene]) -> SceneSelector:
    return SceneSelector(scenes)


def from_entity(scene: entities.Entity) -> Scene:
    return SingleScene(scene)


def off() -> OffScene:
    return OffScene()
