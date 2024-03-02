import appdaemon.plugins.hass.hassapi as hass

import services


class NotificationHandler:

    def __init__(self, app: hass.Hass):
        self._app = app

    def notify(self, title: str, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                          message=f'Front door opened while away',
                          title="🚨Activity detected")

    def debug(self, message: str) -> None:
        self.notify("Debug", message)
