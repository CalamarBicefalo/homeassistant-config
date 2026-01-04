from datetime import datetime, time
from typing import Any, Optional

import appdaemon.plugins.hass.hassapi as hass

import helpers
import services
import states
from entities import Entity
from helpers import Helper


class StateHandler:
    def __init__(self, app: hass.Hass):
        self._app = app

    def is_consuming_at_least(self, device: Entity | Helper | str, watts: int) -> bool:
        return self.get_watt_consumption(device) >= watts

    def is_value(self, device: Entity | Helper | str, desired_state: str) -> bool:
        state = self._app.get_state(device)
        b: bool = state == desired_state
        return b

    def is_on(self, device: Entity | Helper | str) -> bool:
        state = self._app.get_state(device)
        on: bool = state == states.ON or state == states.PLAYING
        return on

    def is_off(self, device: Entity | Helper | str) -> bool:
        return self.is_value(device, states.OFF)

    def is_home(self, device_tracker: Entity | Helper | str) -> bool:
        return self.is_value(device_tracker, 'home')

    def get_as_str(self, device: Entity | Helper | str) -> str:
        state: str = self._app.get_state(device)
        return state

    def get_as_number(
            self,
            device: Entity | Helper | str,
    ) -> float | None:
        state = self.get_as_str(device)
        return self.to_float(state, device)

    def get_as_datetime(self, device: Entity | Helper | str) -> Optional[datetime]:
        state : str = self.get_as_str(device)
        if not state:
            return None
        return helpers.helper_to_datetime(state)

    def get_as_datetime_or_default(self, device: Entity | Helper | str, default: str) -> datetime:
        d: datetime | None = self.get_as_datetime(device)
        if not d:
            self._app.log(f'Date not set for {device}, returning default value',
                         level="WARNING")
            return datetime.fromisoformat(default)
        return d

    def get_as_time(self, device: Entity | Helper | str) -> Optional[time]:
        state: str = self.get_as_str(device)
        if not state or state == 'unknown':
            return None
        try:
            parts = state.split(':')
            if len(parts) >= 2:
                hour = int(parts[0])
                minute = int(parts[1])
                return time(hour=hour, minute=minute)
            else:
                raise ValueError(f"Invalid time format: {state}")
        except (ValueError, AttributeError) as e:
            self._app.log(f'Error parsing time from {device} state "{state}": {e}', level="ERROR")
            return None

    def get_watt_consumption(self, device: Entity | Helper | str) -> int:
        return int(self.get_as_number(device))

    def to_float(self, value: Any, device: Optional[Entity | Helper | str] = None) -> float | None:
        reading_error = f'Cannot convert value "{value}" to float'
        if device is None:
            error = reading_error
        else:
            error = f'{device} error: {reading_error}'
        try:
            return float(value)
        except (ValueError, TypeError):
            self._app.log(error, level="ERROR")
            self._app.call_service(services.NOTIFY_MOBILE_APP_JC_IPHONE,
                                   message=error,
                                   title="Debug")
            return 0

    def is_attr_value(self, device: Entity | Helper | str, attr: str, desired_state: str) -> bool:
        return self.get_attr_as_str(device, attr) == desired_state

    def get_attr_as_str(self, device: Entity | Helper | str, attr: str) -> str:
        state: str = self._app.get_state(device, attribute=attr)
        return state

    def get_attr_as_number(self, device: Entity | Helper | str, attr: str) -> float:
        state: str = self.get_attr_as_str(device, attr)
        return self.to_float(state, device)
