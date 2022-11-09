from typing import List, Optional

import activities
import entities
import helpers
from activity_controllers.controller_app import ControllerApp
from app import App


class LivingRoomActivity(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION
    activity_helper = helpers.LIVING_ROOM_ACTIVITY
    additional_triggers = [entities.MEDIA_PLAYER_TV, entities.BINARY_SENSOR_SOFA_PS_WATER]

    async def get_custom_activity(self, entity, attribute, old, new) -> Optional[activities.Activity]:
        if await self.is_on(entities.MEDIA_PLAYER_TV):
            return activities.LivingRoom.WATCHING_TV

        if await self.is_on(entities.BINARY_SENSOR_SOFA_PS_WATER):
            return activities.LivingRoom.READING
