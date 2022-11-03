import activities
import entities
import helpers
from app import App


class StudioScene(App):

    def initialize(self):
        self.log(f'Initializing studio scene.', level="DEBUG")
        self.listen_state(
            self.set_studio_scene,
            helpers.STUDIO_ACTIVITY
        )
        self.listen_state(
            self.set_studio_scene,
            entities.SENSOR_DESK_MS_ILLUMINANCE
        )

    async def set_studio_scene(self, entity, attribute, old, new, kwargs):
        self.log(f'Changing studio scene {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        activity = await self.get_activity_value(helpers.STUDIO_ACTIVITY)
        if activity == activities.Studio.EMPTY.value:
            self.turn_off(entities.LIGHT_STUDIO)

        if float(await self.get_state(entities.SENSOR_DESK_MS_ILLUMINANCE)) < 40:
            if activity == activities.Studio.WORKING.value:
                self.turn_on(entities.SCENE_STUDIO_WORKING)
            if activity == activities.Studio.DRUMMING.value:
                self.turn_on(entities.SCENE_STUDIO_DRUMMING)
            if activity == activities.Studio.PRESENT.value:
                self.turn_on(entities.SCENE_STUDIO_CONCENTRATE)
        else:
            self.turn_off(entities.LIGHT_STUDIO)
