from datetime import datetime, timedelta
from typing import Any

import entities
import helpers
import selects
import states
from app import App
from select_handler import SelectHandler


class WashingMachine(App):
    THRESHOLD_HIGH = 10
    THRESHOLD_LOW = 2
    WAIT_S = 240
    HOURS_TO_DRY = 12
    POWER_SENSOR = entities.SENSOR_WASHING_MACHINE_SWITCH_INSTANTANEOUS_DEMAND
    DOOR_SENSOR = entities.BINARY_SENSOR_WASHING_MACHINE_CS


    def initialize(self) -> None:
        self.listen_state(self.update_state, self.POWER_SENSOR)
        self.listen_state(self.update_state, self.DOOR_SENSOR)
        self.listen_state(self.notify, helpers.WASHING_MACHINE)
        self._wait_timer = None
        self.washing_machine_state = SelectHandler[selects.WashingMachine](self, helpers.WASHING_MACHINE)

    def notify(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        match new:
            case selects.WashingMachine.MOLD_ALERT:
                self.handlers.notifications.chore("Washing machine door closed", "Please open the door to let it dry and prevent mold")
            case selects.WashingMachine.WET_CLOTHES_INSIDE:
                self.handlers.notifications.chore("Washing machine is done", "Please hang up the laundry 🙏🏿🧦")

    def update_state(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.is_open():
            self.washing_machine_state.set(selects.WashingMachine.DRYING)

        elif self.is_using_power():
            self.washing_machine_state.set(selects.WashingMachine.WASHING)
            if self._wait_timer:
                self.cancel_timer(self._wait_timer, silent=True)
            self._wait_timer = None

        elif self.is_off_but_was_washing_just_before():
            if self._wait_timer is None:
                self._wait_timer = self.run_in(self._on_current_stays_low, self.WAIT_S)

        elif self.has_dried():
            self.washing_machine_state.set(selects.WashingMachine.OFF)

        else:
            self.washing_machine_state.set(selects.WashingMachine.MOLD_ALERT)


    def _on_current_stays_low(self, kwargs: Any) -> None:
        self.washing_machine_state.set(selects.WashingMachine.WET_CLOTHES_INSIDE)
        self.set_helper_to_now(helpers.LAST_WASHED_CLOTHES)
        self._wait_timer = None
        self.handlers.notifications.chore("Washing machine is done", "Please hang up the laundry.")

    def last_washed(self) -> datetime:
        return self.state.get_as_datetime_or_default(helpers.LAST_WASHED_CLOTHES, '1970-01-01')

    def has_dried(self) -> bool:
        return self.last_washed() < datetime.now() - timedelta(hours=self.HOURS_TO_DRY)

    def is_off(self) -> bool:
        return self.state.get_as_number(self.POWER_SENSOR) < self.THRESHOLD_LOW

    def is_open(self) -> bool:
        return self.state.is_value(self.DOOR_SENSOR, states.OPEN)

    def is_using_power(self) -> bool:
        return self.state.get_as_number(self.POWER_SENSOR) > self.THRESHOLD_HIGH

    def is_off_but_was_washing_just_before(self) -> bool:
        return self.is_off() and self.washing_machine_state.is_value(selects.WashingMachine.WASHING)
