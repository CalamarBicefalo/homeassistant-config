from __future__ import annotations

import random
from typing import Optional

from appdaemon.plugins.hass import hassapi as hass
from strenum import StrEnum

import entities
import services
import states


class MusicHandler:

    def __init__(self, app: hass.Hass, speakers: Optional[entities.Entity]):
        self._app = app
        self._speakers = speakers

    def is_playing(self) -> bool:
        state = self._app.get_state(self._speakers)
        playing: bool = state == states.ON or state == states.PLAYING
        return playing

    def play(self, tune: Playlist | str, shuffle: bool = True,
             volume_level: float = 0.3) -> None:
        self._validate()

        self.volume(volume_level)
        self._app.call_service(services.MEDIA_PLAYER_SHUFFLE_SET,
                               entity_id=self._speakers, shuffle=shuffle)
        self._app.log(f'{"Shuffling" if shuffle else "Not shuffling"} queue of {self._speakers}.', level="DEBUG")
        self._app.call_service(services.MASS_QUEUE_COMMAND,
                               entity_id=self._speakers,
                               command="play_media",
                               uri=tune,
                               enqueue_mode="replace",
                               )
        self._app.log(f'Playing {tune} on {self._speakers} - replacing existing queue.', level="DEBUG")

    def pause(self) -> None:
        self._validate()
        self._app.call_service(services.MEDIA_PLAYER_MEDIA_PAUSE, entity_id=self._speakers)

    def toggle_play_pause(self) -> None:
        self._validate()
        self._app.call_service(services.MEDIA_PLAYER_TOGGLE, entity_id=self._speakers)

    def volume(self, volume_level: float) -> None:
        self._validate()
        self._app.call_service(services.MEDIA_PLAYER_VOLUME_SET,
                               entity_id=self._speakers, volume_level=volume_level),
        self._app.log(f'Configured volume of {self._speakers} to {volume_level}.', level="DEBUG")

    def _validate(self) -> None:
        if not self._speakers:
            raise Exception("cannot play music without speakers defined")


class Tune(StrEnum):
    RAIN = "/config/media/rain.mp3"


class Playlist(StrEnum):

    @staticmethod
    def random() -> Playlist:
        pl: Playlist = random.choice(list(Playlist))
        return pl

    CLASSIC_JAZZ = "https://open.spotify.com/playlist/37i9dQZF1DXe0UXHUfHinR?si=a0660f0a365d465a"
    COOL_JAZZ = "https://open.spotify.com/playlist/37i9dQZF1DX6fO1VvuMVL0?si=2455846fc8d1452a"
    LATIN_JAZZ = "https://open.spotify.com/playlist/49dpUtmWy89Sxiq5nxgp3s?si=72e6eb0f69f54266"

    WEEKLY_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/0tDQQrNJNbZwQH8vkkVZnU?si=26134a9e6b1d4a67"
    INDIE_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIgthTKx0giV9?si=4b099173068949bb"
    CONTEMPORARY_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIhfy05JSqnjl?si=d38778c58b0d4949"
    CHILL_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIdgqvd8Qfc5i?si=a2a4499440ca4ecb"
    FUNK_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIhOwuyQWgxIR?si=57569a48eba848b8"
    UPBEAT_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIh0zFaGO7KDE?si=d5010e7b065c4d54"
    MODERN_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIfD76SANX498?si=8fd78be8b8414e81"
    NU_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIeRjWbqxxyRE?si=b930250d02c34919"
    FUSION_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIgnYxCSnxPNW?si=2d26f96af97e4f2a"
    ETHIOPIAN_JAZZ_DYNAMIC = "https://open.spotify.com/playlist/37i9dQZF1EIeplPHHjgFR7?si=2817d69f221b4b29"

    DISCOVER_WEEKLY = "https://open.spotify.com/playlist/37i9dQZEVXcVC84EBt43Lx?si=fbea7a1fd9e04fb5"
    RELAXING = "https://open.spotify.com/playlist/4KfULjAkF7qPXlXFq170AR?si=f5103bd49709471f"
    NEO_CLASSICAL = "https://open.spotify.com/playlist/37i9dQZF1EIgEh8GW3jo4P?si=7bd5a57889964f8c"
