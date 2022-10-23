from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass

import services
import states

HELPER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_to_helper(d: datetime):
    return d.strftime(HELPER_DATETIME_FORMAT)


class App(hass.Hass):
    def helper_to_datetime(self, helper: str):
        """
        Given a datetime helper, it returns a ready to use datetime
        :param helper:
        :return: a datetime object
        """
        return datetime.strptime(str(self.get_state(helper)), HELPER_DATETIME_FORMAT)

    def datetime_to_helper(self, d: datetime):
        return datetime_to_helper(d)

    async def is_on(self, device):
        return (await self.get_state(device)) == states.ON

    async def is_off(self, device):
        return (await self.get_state(device)) == states.OFF

    def set_activity(self, helper, activity):
        self.call_service(
            services.HELPER_SELECT_SET,
            entity_id=helper,
            option=activity
        )

