import entities
from activity_controllers.generic_controller import ActivityController
from ieee_addresses import COFFEE_TABLE_BUTTON_IEEE_ADDRESS
from rooms import *
from select_handler import SelectHandler


class LivingRoomController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.living_room.activity

    def initialize(self) -> None:
        self.listen_state(
            self.controller_handler,
            [
                self.motion_sensor,
                entities.MEDIA_PLAYER_TV_2,
                entities.MEDIA_PLAYER_SONY_KD_49XF8096,
                entities.BINARY_SENSOR_SOFA_PS
            ]
        )
        self.handlers.buttons.on(COFFEE_TABLE_BUTTON_IEEE_ADDRESS,
                        double_click=self.set_drumming,
                        long_press=self.clear_activity)

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering living room activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        if self.activity.is_value(LivingRoom.Activity.DINNING):
            return

        elif self.playing_ps5():
            self.activity.set(LivingRoom.Activity.GAMING)

        elif self.watching_tv():
            self.activity.set(LivingRoom.Activity.WATCHING_TV)

        elif self.activity.is_value(LivingRoom.Activity.DRUMMING):
            if self.is_on(self.motion_sensor) or self.sitting_on_sofa():
                self.set_as_empty_in(minutes=90)
            else:
                self.set_as_empty_in(minutes=10)

        elif self.sitting_on_sofa():
            self.activity.set(LivingRoom.Activity.READING)

        elif self.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.activity.set(CommonActivities.EMPTY)

    def playing_ps5(self) -> bool:
        return self.is_on(entities.MEDIA_PLAYER_SONY_KD_49XF8096) and self.has_state_attr(
            entities.MEDIA_PLAYER_SONY_KD_49XF8096,
            attr="source",
            desired_state="PlayStation 5"
        )

    def watching_tv(self) -> bool:
        return self.is_on(entities.MEDIA_PLAYER_TV_2) or self.is_on(entities.MEDIA_PLAYER_SONY_KD_49XF8096)

    def sitting_on_sofa(self) -> bool:
        return self.is_on(entities.BINARY_SENSOR_SOFA_PS)

    def clear_activity(self) -> None:
        self.activity.set(CommonActivities.EMPTY)

    def set_drumming(self) -> None:
        self.activity.set(LivingRoom.Activity.DRUMMING)
