from abc import abstractmethod
from typing import Optional

from app import App

import activities
import entities


class SceneApp(App):

    def initialize(self):
        self.log(f'Initializing {self.scene} scene.', level="DEBUG")
        self.listen_state(
            self.handle_scene,
            self.activity.helper
        )
        self.listen_state(
            self.handle_scene,
            self.illuminance_sensor
        )

    @property
    @abstractmethod
    def activity(self) -> activities.RoomActivity:
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

    def handle_scene(self, entity, attribute, old, new, kwargs):
        self.log(f'Changing {self.scene} scene {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        activity = self.get_activity_value(self.activity.helper)

        self.on_activity_change(activity)

        if activity == activities.RoomActivity.EMPTY:
            self.turn_off(self.room_lights)
            return

        if not self.illuminance_sensor:
            self.turn_on(self.get_light_scene(activity))
            return

        illuminance = float(self.get_state(self.illuminance_sensor))
        lights_on = self.is_on(self.room_lights)
        if ((not lights_on) and illuminance < 40) or (lights_on and illuminance < 200):
            self.turn_on(self.get_light_scene(activity))
        else:
            self.turn_off(self.room_lights)
