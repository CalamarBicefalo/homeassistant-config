from abc import abstractmethod
from typing import Optional, Dict, TypeVar

import entities
from modes import Mode


class Scene:

    @abstractmethod
    def get_scene(self, mode: Mode) -> Optional[entities.Entity]:
        pass


def by_mode(by_mode: Dict[Mode, entities.Entity]) -> Scene:
    return ByModeScene(by_mode)


def of(scene: entities.Entity) -> Scene:
    return SingleScene(scene)


def none() -> Scene:
    return EmptyScene()


class EmptyScene(Scene):
    def get_scene(self, mode: Mode) -> Optional[entities.Entity]:
        return None


class ByModeScene(Scene):

    def get_scene(self, mode: Mode) -> Optional[entities.Entity]:
        if not self.dict:
            return None
        return self.dict[mode]

    def __init__(self, dict: Dict[Mode, entities.Entity]):
        self.dict = dict


class SingleScene(Scene):
    def get_scene(self, mode: Mode) -> Optional[entities.Entity]:
        return self.scene

    def __init__(self, scene: entities.Entity):
        self.scene = scene
