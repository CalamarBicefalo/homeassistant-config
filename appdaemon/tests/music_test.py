from typing import Any

import pytest
from appdaemontestframework import automation_fixture

import entities
import matchers
import services
from app import App

speakers = entities.MEDIA_PLAYER_MASS_COOKING_AREA


class MusicApp(App):
    speakers = speakers

    def initialize(self) -> None:
        pass


@automation_fixture(MusicApp)
def app() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_play_sets_volume(assert_that: Any, app: MusicApp) -> None:
    app.music.play("tune", volume_level=0.2)
    assert_that(services.MEDIA_PLAYER_VOLUME_SET).was.called_with(
        entity_id=speakers, volume_level=0.2)


@pytest.mark.asyncio
def test_play_sets_shuffling(assert_that: Any, app: MusicApp) -> None:
    app.music.play("tune", shuffle=True)
    assert_that(services.MEDIA_PLAYER_SHUFFLE_SET).was.called_with(
        entity_id=speakers, shuffle=True)


@pytest.mark.asyncio
def test_play_plays_tune(assert_that: Any, app: MusicApp) -> None:
    app.music.play("tune")
    assert_that(services.MASS_QUEUE_COMMAND).was.called_with(
        entity_id=speakers,
        command="play_media",
        uri="tune",
        enqueue_mode="replace")

@pytest.mark.asyncio
def test_pause(assert_that: Any, app: MusicApp) -> None:
    app.music.pause()
    assert_that(services.MEDIA_PLAYER_MEDIA_PAUSE).was.called_with(
        entity_id=speakers,
    )
