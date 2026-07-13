import enum
from abc import abstractmethod
from typing import Optional, Dict, Callable, Any, Tuple

import entities
from selects import Mode


class Facet(enum.Enum):
    BLINDS = enum.auto()
    MEDIA = enum.auto()
    LIGHTS = enum.auto()
    POWER = enum.auto()
    TRANSITION = enum.auto()  # gradual routines that run over a period (wake-up, bedtime)


Action = Callable[[], Optional[Any]]
TaggedAction = Tuple[Facet, Action]


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

    def execute_actions(self, only: Optional[set[Facet]] = None) -> None:
        for facet, action in self.actions:
            if only is None or facet in only:
                action()

    def __init__(self, scene: Optional[Scene], actions: Tuple[TaggedAction, ...]):
        for action in actions:
            if not (isinstance(action, tuple) and len(action) == 2
                    and isinstance(action[0], Facet) and callable(action[1])):
                raise TypeError(
                    f"Scene actions must be (Facet, callable) tuples; got {action!r}. "
                    "Every action must declare a Facet."
                )
        self.scene = scene
        self.actions: Tuple[TaggedAction, ...] = tuple(actions)


class OffScene(Scene):
    def get(self) -> _Off:
        return _Off()


def by_mode(scenes: Dict[Mode | str, Scene]) -> SceneByModeSelector:
    return SceneByModeSelector(scenes)


def from_entity(scene: entities.Entity) -> Scene:
    return SingleScene(scene)


def with_actions(scene: Optional[Scene], *args: TaggedAction) -> Scene:
    return SceneWithActions(scene, args)


def off() -> OffScene:
    return OffScene()
