import activities
import entities
from activity_controllers.generic_controller import ActivityController
from select_handler import SelectHandler


class LivingRoomController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.activities.livingroom

    def initialize(self) -> None:
        self.listen_state(
            self.controller_handler,
            [
                self.motion_sensor,
                entities.MEDIA_PLAYER_TV,
                entities.MEDIA_PLAYER_SONY_KD_49XF8096,
                entities.BINARY_SENSOR_SOFA_PS_WATER
            ]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering living room activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        if self.activity.is_value(activities.LivingRoom.DINNING):
            return

        elif self.playing_ps5():
            self.activity.set(activities.LivingRoom.GAMING)

        elif self.watching_tv():
            self.activity.set(activities.LivingRoom.WATCHING_TV)

        elif self.activity.is_value(activities.LivingRoom.DRUMMING):
            if self.is_on(self.motion_sensor) or self.sitting_on_sofa():
                self.set_as_empty_in(minutes=90)
            else:
                self.set_as_empty_in(minutes=10)

        elif self.sitting_on_sofa():
            self.activity.set(activities.LivingRoom.READING)

        elif self.is_on(self.motion_sensor):
            self.activity.set(activities.Common.PRESENT)

        else:
            self.activity.set(activities.Common.EMPTY)

    def playing_ps5(self) -> bool:
        return self.is_on(entities.MEDIA_PLAYER_SONY_KD_49XF8096) and self.has_state_attr(
            entities.MEDIA_PLAYER_SONY_KD_49XF8096,
            attr="source",
            desired_state="PlayStation 5"
        )

    def watching_tv(self) -> bool:
        return self.is_on(entities.MEDIA_PLAYER_TV) or self.is_on(entities.MEDIA_PLAYER_SONY_KD_49XF8096)

    def sitting_on_sofa(self) -> bool:
        return self.is_on(entities.BINARY_SENSOR_SOFA_PS_WATER)
