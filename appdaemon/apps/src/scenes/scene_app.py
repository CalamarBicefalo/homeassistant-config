from abc import abstractmethod
from typing import Optional

import activities
import entities
from app import App


class SceneApp(App):

    def initialize(self):
        self.log(f'Initializing {self.scene} scene.', level="DEBUG")
        self.listen_state(
            self.handle_scene,
            self.activity_helper
        )
        self.listen_state(
            self.handle_scene,
            self.illuminance_sensor
        )

    @property
    @abstractmethod
    def activity_helper(self) -> str:
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
    def get_light_scene(self, activity: activities.Activity) -> entities.Entity:
        pass

    def on_activity_change(self, activity: activities.Activity):
        pass

    @property
    def scene(self):
        return self.__class__.__name__

    async def handle_scene(self, entity, attribute, old, new, kwargs):
        self.log(f'Changing {self.scene} scene {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        activity = await self.get_activity_value(self.activity_helper)

        self.on_activity_change(activity)

        if activity == activities.Common.EMPTY:
            self.turn_off(self.room_lights)
            return

        if (not self.illuminance_sensor) or \
                (await self.is_off(self.room_lights) and float(await self.get_state(self.illuminance_sensor)) < 40) or \
                (await self.is_on(self.room_lights) and float(await self.get_state(self.illuminance_sensor)) < 200):
            self.turn_on(self.get_light_scene(activity))
        else:
            self.turn_off(self.room_lights)