from abc import abstractmethod

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
    def illuminance_sensor(self) -> entities.Entity:
        pass

    @abstractmethod
    def set_light_scene(self, activity: activities.Activity):
        pass

    def on_activity_change(self, activity: activities.Activity):
        pass

    @abstractmethod
    def turn_off_lights(self):
        pass

    @property
    def scene(self):
        return self.__class__.__name__

    async def handle_scene(self, entity, attribute, old, new, kwargs):
        self.log(f'Changing {self.scene} scene {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        activity = await self.get_activity_value(self.activity_helper)

        self.on_activity_change(activity)

        if activity == activities.Common.EMPTY:
            self.turn_off_lights()
            return

        if float(await self.get_state(self.illuminance_sensor)) < 40:
            self.set_light_scene(activity)
        else:
            self.turn_off_lights()
