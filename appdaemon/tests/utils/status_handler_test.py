from unittest.mock import MagicMock

import entities
from status_handler import StatusHandler, room_key


def test_room_key_strips_prefix_and_suffix():
    assert room_key(entities.SENSOR_OFFICE_BRIGHTNESS) == "office"
    assert room_key(entities.SENSOR_LIVING_ROOM_BRIGHTNESS) == "living_room"


def test_publish_lights_sets_state_and_explanation():
    app = MagicMock()
    StatusHandler(app, "office").publish_lights(
        "On", "there isn't enough daylight", detail="CLOUDY (500lx < 1500lx)")

    app.set_state.assert_called_once()
    args, kwargs = app.set_state.call_args
    assert args[0] == "sensor.office_lights_status"
    assert kwargs["state"] == "On"
    attrs = kwargs["attributes"]
    assert attrs["reason"] == "there isn't enough daylight"
    assert attrs["explanation"] == "On because there isn't enough daylight"
    assert attrs["detail"] == "CLOUDY (500lx < 1500lx)"
    assert attrs["friendly_name"] == "Office Lights"


def test_publish_blinds_sets_state_and_explanation():
    app = MagicMock()
    StatusHandler(app, "living_room").publish_blinds(
        "Partially closed", "the plants still want light")

    args, kwargs = app.set_state.call_args
    assert args[0] == "sensor.living_room_blinds_status"
    assert kwargs["state"] == "Partially closed"
    attrs = kwargs["attributes"]
    assert attrs["explanation"] == "Partially closed because the plants still want light"
    assert attrs["friendly_name"] == "Living Room Blinds"
