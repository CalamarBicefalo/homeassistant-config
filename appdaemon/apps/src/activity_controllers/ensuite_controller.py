import activities
import entities
import states
from app import App
from select_handler import SelectHandler


class EnsuiteController(App):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    contact_sensor = entities.BINARY_SENSOR_BATHROOM_CS_CONTACT
    turnoff_timer = None
    turnoff_time = 60
    present_cooldown = 1800
    shower_cooldown = 2000

    @property
    def activity(self) -> SelectHandler:
        return self.activities.ensuite

    def initialize(self) -> None:
        self.listen_state(
            self.on_motion,
            self.motion_sensor
        )

        self.listen_state(
            self.on_door,
            self.contact_sensor
        )

    def on_motion(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering ensuite motion activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(activities.Ensuite.SHOWERING):
            return

        self.cancel_timers()

        if new == states.DETECTED:
            if self.get_state(self.contact_sensor) == states.CLOSED:
                self.activity.set(activities.Ensuite.SHOWERING)
                self.set_as_empty_in(self.shower_cooldown)
            else:
                self.activity.set(activities.Ensuite.PRESENT)
                self.set_as_empty_in(self.present_cooldown)
        else:
            self.set_as_empty_in(self.turnoff_time)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering ensuite door controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(activities.Ensuite.EMPTY) and new == states.OPEN:
            self.cancel_timers()
            self.activity.set(activities.Common.PRESENT)
            self.set_as_empty_in(self.present_cooldown)

        if self.activity.is_value(activities.Ensuite.SHOWERING):
            self.cancel_timers()
            self.activity.set(activities.Common.PRESENT)
            self.set_as_empty_in(self.present_cooldown)

    def cancel_timers(self) -> None:
        if self.turnoff_timer:
            self.cancel_timer(self.turnoff_timer)
            self.turnoff_timer = None

    def set_as_empty_in(self, seconds: int) -> None:
        self.turnoff_timer = self.run_in(
            lambda *_: self.activities.ensuite.set(activities.Ensuite.EMPTY), seconds)
