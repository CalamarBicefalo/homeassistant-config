import activities
import entities
from activity_controllers.generic_controller import ActivityController
from handlers.select_handler import SelectHandler


class LivingRoomController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.activities.livingroom

    def initialize(self) -> None:
        self.listen_state(
            self.controller_handler,
            [self.motion_sensor, entities.MEDIA_PLAYER_TV, entities.BINARY_SENSOR_SOFA_PS_WATER]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering living room activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        # TV Handling
        if self.is_on(entities.MEDIA_PLAYER_TV):
            self.activity.set(activities.LivingRoom.WATCHING_TV)

        # Drumming Handling
        elif self.activity.get() == activities.LivingRoom.DRUMMING:
            if self.is_on(self.motion_sensor) or self.sitting_on_sofa():
                self.set_as_empty_in(minutes=90)
            else:
                self.set_as_empty_in(minutes=10)

        # Sofa Handling
        elif self.sitting_on_sofa():
            self.activity.set(activities.LivingRoom.READING)

        # Presence Handling
        elif self.is_on(self.motion_sensor):
            self.activity.set(activities.Common.PRESENT)

        else:
            self.activity.set(activities.Common.EMPTY)

    def sitting_on_sofa(self) -> bool:
        return self.is_on(entities.BINARY_SENSOR_SOFA_PS_WATER)
