import appdaemon.plugins.hass.hassapi as hass

import entities
import helpers
import services
from select_handler import SelectHandler
from selects import Mode


class NotificationHandler:

    def __init__(self, app: hass.Hass):
        self._app = app
        self.mode = SelectHandler[Mode](app, helpers.MODE)

    def security_alert(self, title: str, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                          message=message,
                          title=title)

    def chore(self, title: str, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                          message=message,
                          title=title)
        if not self.mode.is_value(Mode.SLEEPING):
            self._app.call_service(
                services.TTS_SPEAK,
                entity_id=entities.TTS_PIPER,
                media_player_entity_id= entities.MEDIA_PLAYER_ALL_SPEAKERS_GOOGLE_CAST,
                message=message)

    def debug(self, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                               message=message,
                               title="Debug")
