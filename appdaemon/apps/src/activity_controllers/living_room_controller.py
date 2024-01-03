import entities
from activity_controllers.generic_controller import ActivityController
from ieee_addresses import COFFEE_TABLE_BUTTON_IEEE_ADDRESS
from rooms import *


class LivingRoomController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION

    @property
    def activity(self) -> ActivityHandler:
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
                                 double_click=self.on_double_click,
                                 long_press=self.on_long_press)

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering living room activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        if self.activity.is_value(LivingRoom.Activity.RELAXING):
            return

        elif self.playing_ps5():
            self.activity.set(LivingRoom.Activity.GAMING)

        elif self.watching_tv():
            self.activity.set(LivingRoom.Activity.WATCHING_TV)

        elif self.activity.is_value(LivingRoom.Activity.DRUMMING):
            if self.state.is_on(self.motion_sensor) or self.sitting_on_sofa():
                self.set_as_empty_in(minutes=90)
            else:
                self.set_as_empty_in(minutes=10)

        elif self.sitting_on_sofa():
            self.activity.set(LivingRoom.Activity.READING)

        elif self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.activity.set(CommonActivities.EMPTY)

    def playing_ps5(self) -> bool:
        return (
                self.state.is_on(entities.MEDIA_PLAYER_SONY_KD_49XF8096)
                and self.state.is_attr_value(
            entities.MEDIA_PLAYER_SONY_KD_49XF8096,
            attr="source",
            desired_state="PlayStation 5"
        )
        )

    def watching_tv(self) -> bool:
        return self.state.is_on(entities.MEDIA_PLAYER_TV_2) or self.state.is_on(
            entities.MEDIA_PLAYER_SONY_KD_49XF8096)

    def sitting_on_sofa(self) -> bool:
        return self.state.is_on(entities.BINARY_SENSOR_SOFA_PS)

    def on_long_press(self) -> None:
        self.activity.set(CommonActivities.EMPTY, manual=True)

    def on_double_click(self) -> None:
        self.activity.set(LivingRoom.Activity.DRUMMING, manual=True)
