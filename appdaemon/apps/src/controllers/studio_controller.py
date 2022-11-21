import activities
import entities
import helpers
from controllers.controller_app import ControllerApp


class StudioController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_STUDIO_MOTION
    activity = activities.Studio
    additional_triggers = [entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER, entities.SENSOR_DRUMS_PLUG_POWER]

    def get_custom_activity(self, entity, attribute, old, new):
        # Work handling
        if self.is_on(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER):
            return activities.Studio.WORKING

        # Drum handling
        if self.is_consuming_at_least(entities.SENSOR_DRUMS_PLUG_POWER, watts=4):
            return activities.Studio.DRUMMING

    def should_trigger(self, entity, attribute, old, new) -> bool:
        return not (entity == entities.SENSOR_DRUMS_PLUG_POWER and abs(float(old) - float(new)) < 3)
