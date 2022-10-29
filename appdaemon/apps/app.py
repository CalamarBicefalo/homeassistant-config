import inspect
import numbers
from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import services
import states

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
        current_consumption = await self.get_state(device)
        return int(current_consumption) >= watts

    async def is_on(self, device):
        return await self.has_state(device, states.ON)

    async def is_off(self, device):
        return await self.has_state(device, states.OFF)

    async def has_state(self, device, desired_state: str) -> bool:
        state = self.get_state(device)
        return (await state) == desired_state

    async def is_activity(self, helper, activity):
        return await self.has_state(helper, activity)

    def set_activity(self, helper, activity):
        self.log(f'Setting activity {activity} in {helper}', level="INFO")
        self.call_service(
            services.HELPER_SELECT_SET,
            entity_id=helper,
            option=activity
        )
