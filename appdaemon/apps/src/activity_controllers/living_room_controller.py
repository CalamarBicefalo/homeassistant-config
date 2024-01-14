from typing import Callable

import entities
from activity_controllers.generic_controller import ActivityController
from ieee_addresses import COFFEE_TABLE_BUTTON_IEEE_ADDRESS, DINING_TABLE_BUTTON_IEEE_ADDRESS
from rooms import *


class LivingRoomController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.living_room.activity

    def initialize(self) -> None:
        super().initialize_lock()
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
                                 double_click=self.lock_scene(LivingRoom.Activity.DRUMMING),
                                 long_press=self.set_present_scene)

        self.handlers.buttons.on(DINING_TABLE_BUTTON_IEEE_ADDRESS,
                                 double_click=self.lock_scene(LivingRoom.Activity.DINING),
                                 long_press=self.set_present_scene)

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering living room activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        if self.playing_ps5():
            self.activity.set(LivingRoom.Activity.GAMING)

        elif self.watching_tv():
            self.activity.set(LivingRoom.Activity.WATCHING_TV)

        elif (self.activity.is_value(LivingRoom.Activity.RELAXING)
              or self.activity.is_value(LivingRoom.Activity.DRUMMING)):
            return

        # unreliable PS commenting for now
        # elif self.sitting_on_sofa():
            # self.activity.set(LivingRoom.Activity.RELAXING)

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

    def set_present_scene(self) -> None:
        self.activity.set(CommonActivities.PRESENT, lock=False)

    def lock_scene(self, scene) -> Callable[[], None]:
        return lambda: self.activity.set(scene, lock=True)
