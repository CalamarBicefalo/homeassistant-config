from typing import Any

import alarmclock
import entities
import mode_controller
import modes
from activity_controllers.generic_controller import MotionController
from ieee_addresses import BEDSIDE_BUTTON_IEEE_ID
from rooms import *
from select_handler import SelectHandler


class BedroomController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MOTION
    _waking_up_schedule = None

    @property
    def activity(self) -> SelectHandler:
        return self.rooms.bedroom.activity

    @property
    def max_inactive_activity_seconds(self) -> int:
        return 90 * 60

    def initialize(self) -> None:
        self.log(f'Initializing {self.controller} motion based activity controller.', level="DEBUG")
        self.listen_state(
            self.controller_handler,
            self.motion_sensor
        )
        self.alarmclock.listen(self.on_1_hour_to_wake_up, alarmclock.Event.ONE_HOUR_BEFORE_ALARM)
        self.buttons.on(BEDSIDE_BUTTON_IEEE_ID,
                        click=self.on_click,
                        double_click=self.on_double_click,
                        long_press=self.on_long_press
                        )

    def on_double_click(self) -> None:
        if self._waking_up_schedule and self.timer_running(self._waking_up_schedule):
            self.cancel_timer(self._waking_up_schedule)

        self.activity.set(Bedroom.Activity.RELAXING)
        self.fire_event(mode_controller.EVENT_MODE_RECOMPUTE_NEEDED)

    def on_long_press(self) -> None:
        if self._waking_up_schedule and self.timer_running(self._waking_up_schedule):
            self.cancel_timer(self._waking_up_schedule)

        self.activity.set(CommonActivities.PRESENT)
        self.fire_event(mode_controller.EVENT_MODE_RECOMPUTE_NEEDED)

    def on_click(self) -> None:
        if self._waking_up_schedule and self.timer_running(self._waking_up_schedule):
            self.cancel_timer(self._waking_up_schedule)

        if self.activity.is_value(Bedroom.Activity.BEDTIME):
            self.mode.set(modes.Mode.SLEEPING)
        else:
            self.activity.set(Bedroom.Activity.BEDTIME)
            self.fire_event(mode_controller.EVENT_MODE_RECOMPUTE_NEEDED)

    def on_1_hour_to_wake_up(self) -> None:
        self.log(
            f'Triggering bedroom activity controller: 1 hour to wake up',
            level="DEBUG")
        self.cancel_empty_timer()
        self._waking_up_schedule = self.run_in(lambda *_: self.activity.set(Bedroom.Activity.WAKING_UP), 1800)

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering bedroom activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")
        self.cancel_empty_timer()

        if self.activity.get() == Bedroom.Activity.BEDTIME:
            return

        if self._waking_up_schedule and self.timer_running(self._waking_up_schedule):
            self.cancel_timer(self._waking_up_schedule)

        if self.activity.get() == Bedroom.Activity.WAKING_UP:
            return

        # Relaxing Handling
        if self.activity.get() == Bedroom.Activity.RELAXING:
            if self.is_off(self.motion_sensor):
                self.set_as_empty_in(minutes=30)

        # Presence Handling
        elif self.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(minutes=1)
