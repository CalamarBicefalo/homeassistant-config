import appdaemon.plugins.hass.hassapi as hass

import services


class NotificationHandler:

    def __init__(self, app: hass.Hass):
        self._app = app

    def security_alert(self, title: str, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                          message=message,
                          title=title)

    def chore(self, title: str, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                          message=message,
                          title=title)

    def debug(self, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                               message=message,
                               title="Debug")
