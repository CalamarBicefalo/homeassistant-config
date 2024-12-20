from abc import abstractmethod

import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *

class GenericBathroomController(ActivityController):

    @property
    @abstractmethod
    def motion_sensor(self) -> entities.Entity:
        pass

    @property
    @abstractmethod
    def contact_sensor(self) -> entities.Entity:
        pass

    @property
    @abstractmethod
    def showering_activity(self) -> StrEnum:
        pass

    @property
    @abstractmethod
    def room_name(self) -> str:
        pass

    turnoff_time = 60
    present_cooldown = 1500
    shower_cooldown = 2000

    def initialize(self) -> None:
        super().initialize_lock()
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
            f'Triggering {self.room_name} motion activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(self.showering_activity):
            self.set_as_empty_in(self.shower_cooldown)
            return

        if new == states.DETECTED:
            if self.state.is_value(self.contact_sensor, states.CLOSED):
                self.activity.set(self.showering_activity)
                self.set_as_empty_in(self.shower_cooldown)
            else:
                self.activity.set(CommonActivities.PRESENT)
                self.set_as_empty_in(self.present_cooldown)
        else:
            self.set_as_empty_in(self.turnoff_time)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering {self.room_name} door controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if self.activity.is_value(CommonActivities.EMPTY) and new == states.OPEN:
            self.activity.set(CommonActivities.PRESENT)
            self.set_as_empty_in(self.present_cooldown)

        if self.activity.is_value(self.showering_activity):
            self.activity.set(CommonActivities.PRESENT)
            self.set_as_empty_in(self.present_cooldown)


class EnsuiteController(GenericBathroomController):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    contact_sensor = entities.BINARY_SENSOR_ENSUITE_DOOR_CS
    showering_activity = Ensuite.Activity.SHOWERING
    room_name = "ensuite"

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.ensuite.activity

class BathroomController(GenericBathroomController):
    motion_sensor = entities.BINARY_SENSOR_BATHROOM_MS_MOTION
    contact_sensor = entities.BINARY_SENSOR_BATHROOM_DOOR_CS
    showering_activity = Bathroom.Activity.SHOWERING
    room_name = "bathroom"

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.bathroom.activity