from typing import Callable

import appdaemon.plugins.hass.hassapi as hass


class MediaButtonsHandler:

    def __init__(self, app: hass.Hass, device_ieee: str):
        self._app = app
        self.device_ieee = device_ieee

    def on_play(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='toggle', device_ieee=self.device_ieee)

    def on_forwards(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='step', params=lambda x: x.step_mode == 0,
                               device_ieee=self.device_ieee)

    def on_backwards(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='step', params=lambda x: x.step_mode == 1,
                               device_ieee=self.device_ieee)

    def on_volume_up(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command=lambda x: x in ['step', 'move_with_on_off'],
                               params=lambda x: x.move_mode == 0,
                               device_ieee=self.device_ieee)

    def on_volume_down(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command=lambda x: x in ['step', 'move_with_on_off'],
                               params=lambda x: x.move_mode == 1,
                               device_ieee=self.device_ieee)

    def on_click_dot_1(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='short_release',
                               endpoint_id='2',
                               device_ieee=self.device_ieee)

    def on_double_click_dot_1(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='multi_press_complete',
                               endpoint_id='2',
                               device_ieee=self.device_ieee)

    def on_hold_dot_1(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='long_release',
                               endpoint_id='2',
                               device_ieee=self.device_ieee)

    def on_click_dot_2(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='short_release',
                               endpoint_id='3',
                               device_ieee=self.device_ieee)

    def on_double_click_dot_2(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='multi_press_complete',
                               endpoint_id='3',
                               device_ieee=self.device_ieee)

    def on_hold_dot_2(self, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='long_release',
                               endpoint_id='3',
                               device_ieee=self.device_ieee)
