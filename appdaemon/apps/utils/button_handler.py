from typing import Callable

import appdaemon.plugins.hass.hassapi as hass


class ButtonHandler:

    def __init__(self, app: hass.Hass):
        self._app = app

    def on_click(self, device_ieee: str, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='toggle', device_ieee=device_ieee)

    def on_double_click(self, device_ieee: str, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='on', device_ieee=device_ieee)

    def on_long_press(self, device_ieee: str, callback: Callable[..., None]) -> None:
        self._app.listen_event(lambda *_: callback(), "zha_event", command='off', device_ieee=device_ieee)

    def on(self, device_ieee: str, **kwargs: Callable[..., None]) -> None:
        if 'click' in kwargs:
            self.on_click(device_ieee, kwargs['click'])
        if 'double_click' in kwargs:
            self.on_double_click(device_ieee, kwargs['double_click'])
        if 'long_press' in kwargs:
            self.on_long_press(device_ieee, kwargs['long_press'])
