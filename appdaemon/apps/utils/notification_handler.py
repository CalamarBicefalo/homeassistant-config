import appdaemon.plugins.hass.hassapi as hass

import entities
import helpers
import services
from music import MusicHandler
from select_handler import SelectHandler
from selects import Mode


class NotificationHandler:
    announcement_speaker = entities.MEDIA_PLAYER_ALL_SPEAKERS_GOOGLE_CAST

    def __init__(self, app: hass.Hass):
        self._app = app
        self.mode = SelectHandler[Mode](app, helpers.MODE)
        self.speaker = MusicHandler(app, self.announcement_speaker)

    def security_alert(self, title: str, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                          message=message,
                          title=title)

    def chore(self, title: str, message: str) -> None:
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                          message=message,
                          title=title)
        if not self.mode.is_value(Mode.SLEEPING):
            self.speaker.announce(message)

    def debug(self, message: str) -> None:
        self._app.log(f'App Debug: {message}', level="WARNING")
        self._app.call_service(services.NOTIFY_MOBILE_APP_GALAXY_S23,
                               message=message,
                               title="Debug")


