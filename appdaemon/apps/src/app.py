from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import services
import states
from activities import Activity

HELPER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_to_helper(d: datetime):
    return d.strftime(HELPER_DATETIME_FORMAT)


class App(hass.Hass):
    async def helper_to_datetime(self, helper: str):
        """
        Given a datetime helper, it returns a ready to use datetime
        :param helper:
        :return: a datetime object
        """
        return datetime.strptime(str(await self.get_state(helper)), HELPER_DATETIME_FORMAT)

    def datetime_to_helper(self, d: datetime):
        return datetime_to_helper(d)

    async def is_consuming_at_least(self, device: str, watts: int) -> bool:
        return await self.get_watt_consumption(device) >= watts

    async def get_watt_consumption(self, device: str) -> int:
        return int(float(await self.get_state(device)))

    async def is_on(self, device):
        state = await self.get_state(device)
        return state == states.ON or state == "playing"

    async def is_off(self, device):
        return await self.has_state(device, states.OFF)

    async def has_state(self, device, desired_state: str) -> bool:
        state = self.get_state(device)
        return (await state) == desired_state

    async def is_activity(self, helper, activity: Activity):
        return await self.has_state(helper, activity.value)

    async def get_activity_value(self, helper) -> str:
        return await self.get_state(helper)

    def set_activity(self, helper, activity: Activity):
        self.log(f'Setting activity {activity.value} in {helper}', level="INFO")
        self.call_service(
            services.INPUT_SELECT_SELECT_OPTION,
            entity_id=helper,
            option=activity.value
        )
