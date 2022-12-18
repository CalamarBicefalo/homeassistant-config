import activities
import entities
import states
from app import App
from select_handler import SelectHandler


class EnsuiteController(App):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    contact_sensor = entities.BINARY_SENSOR_BATHROOM_CS_CONTACT
    disable_showering_timer = None
    disable_present_timer = None
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
                self.disable_showering_timer = self.run_in(lambda *_: self.activities.ensuite.set(activities.Ensuite.EMPTY), 1800)
            else:
                self.activity.set(activities.Ensuite.PRESENT)
                self.disable_present_timer = self.run_in(lambda *_: self.activities.ensuite.set(activities.Ensuite.EMPTY), 180)

    def cancel_timers(self):
        if self.disable_showering_timer:
            self.cancel_timer(self.disable_showering_timer)
        if self.disable_present_timer:
            self.cancel_timer(self.disable_present_timer)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering ensuite door controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_timers()

        if self.activity.is_value(activities.Ensuite.EMPTY) and new == states.CLOSED:
            self.activity.set(activities.Ensuite.EMPTY)
        else:
            self.activity.set(activities.Common.PRESENT)
