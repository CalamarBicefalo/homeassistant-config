from datetime import datetime

import alarmclock
import entities
import mode_controller
import selects
from activity_controllers.generic_controller import MotionController
from ieee_addresses import BEDSIDE_BUTTON_IEEE_ID
from rooms import *


class BedroomController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MOTION
    _waking_up_schedule = None
    _enable_bedtime_timer = None

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.bedroom.activity

    @property
    def max_seconds_until_empty(self) -> int:
        return 10 * 60 * 60

    @property
    def max_seconds_without_presence_until_empty(self) -> int:
        return 10 * 60

    def initialize(self) -> None:
        super().initialize_lock()
        self.log(f'Initializing {self.controller} motion based activity controller.', level="DEBUG")
        self.listen_state(
            self.controller_handler,
            self.motion_sensor
        )
        self.handlers.alarmclock.listen(self.on_1_hour_to_wake_up, alarmclock.Event.ONE_HOUR_BEFORE_ALARM)
        self.handlers.alarmclock.listen(self.on_alarm_dismissed, alarmclock.Event.ALARM_DISMISSED)
        self.handlers.buttons.on(BEDSIDE_BUTTON_IEEE_ID,
                        click=self.on_click,
                        double_click=self.on_double_click,
                        long_press=self.on_long_press
                        )

    def on_double_click(self) -> None:
        self.cancel_empty_timer()
        self.cancel_wakeup_timer()

        self.activity.set(Bedroom.Activity.RELAXING)
        self.fire_event(mode_controller.EVENT_MODE_RECOMPUTE_NEEDED)

    def on_long_press(self) -> None:
        self.cancel_empty_timer()
        self.cancel_wakeup_timer()

        self.activity.set(CommonActivities.PRESENT)
        self.fire_event(mode_controller.EVENT_MODE_RECOMPUTE_NEEDED)

    def on_click(self) -> None:
        self.cancel_empty_timer()
        self.cancel_wakeup_timer()

        if self.activity.is_value(Bedroom.Activity.BEDTIME):
            self.handlers.mode.set(selects.Mode.SLEEPING)
        else:
            self.activity.set(Bedroom.Activity.BEDTIME)
            self.fire_event(mode_controller.EVENT_MODE_RECOMPUTE_NEEDED)

    def on_1_hour_to_wake_up(self) -> None:
        self.log(
            f'Triggering bedroom activity controller: 1 hour to wake up',
            level="INFO")
        self.cancel_empty_timer()
        self._waking_up_schedule = self.run_in(lambda *_: self.activity.set(Bedroom.Activity.WAKING_UP), 1800)
        self._waking_up_schedule = self.run_in(lambda *_: self.on_alarm_buzzing(), 3600)

    def on_alarm_dismissed(self) -> None:
        pass

    def on_alarm_buzzing(self) -> None:
        self.cancel_empty_timer()
        self.cancel_wakeup_timer()

        self.fire_event(mode_controller.EVENT_MODE_RECOMPUTE_NEEDED)
        self.run_in(lambda *_: self.handle_presence(),1)

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering bedroom activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")
        self.cancel_empty_timer()

        if self.activity.get() in [Bedroom.Activity.BEDTIME, Bedroom.Activity.WAKING_UP]:
            return

        # Relaxing Handling
        if self.activity.get() == Bedroom.Activity.RELAXING:
            return

        if self.should_enable_bedtime():
            if not self._enable_bedtime_timer or not self.timer_running(self._enable_bedtime_timer):
                self._enable_bedtime_timer = self.run_in(lambda *_: self.enable_bedtime_if_in_bed(),30)
        elif self._enable_bedtime_timer:
            self.cancel_timer(self._enable_bedtime_timer, True)

        self.handle_presence()

    def should_enable_bedtime(self) -> bool:
        return self.state.is_on(entities.BINARY_SENSOR_BED_OCCUPANCY) and (
                    datetime.now().time().hour >= 22 or datetime.now().time().hour <= 2)

    def handle_presence(self) -> None:
        if self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(minutes=1)

    def enable_bedtime_if_in_bed(self) -> None:
        if self.should_enable_bedtime():
            self.activity.set(Bedroom.Activity.BEDTIME)


    def cancel_wakeup_timer(self) -> None:
        if self._waking_up_schedule and self.timer_running(self._waking_up_schedule):
            self.cancel_timer(self._waking_up_schedule)
