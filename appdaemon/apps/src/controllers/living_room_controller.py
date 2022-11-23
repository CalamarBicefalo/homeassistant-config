from typing import Optional

import activities
import entities
from controllers.controller_app import ControllerApp


class LivingRoomController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION
    activity = activities.LivingRoom
    additional_triggers = [entities.MEDIA_PLAYER_TV, entities.BINARY_SENSOR_SOFA_PS_WATER]

    def get_custom_activity(self, entity, attribute, old, new) -> Optional[activities.Activity]:
        if self.is_on(entities.MEDIA_PLAYER_TV):
            return activities.LivingRoom.WATCHING_TV

        if self.is_on(entities.BINARY_SENSOR_SOFA_PS_WATER):
            return activities.LivingRoom.READING

        return None
