from typing import Optional

import activities
import entities
from app import App
from select_handler import SelectHandler


class LivingRoomController(App):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_MOTION
    no_activity_cooldown = None

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

        self.handle_cooldown()

        if self.activity.get() == activities.LivingRoom.DRUMMING:
            self.no_activity_cooldown = self.run_in(
                lambda *_: self.activities.livingroom.set(activities.LivingRoom.EMPTY), 10 * 60)
            return

        # TV Handling
        if self.is_on(entities.MEDIA_PLAYER_TV):
            self.activity.set(activities.LivingRoom.WATCHING_TV)

        # Sofa Handling
        elif self.is_on(entities.BINARY_SENSOR_SOFA_PS_WATER):
            self.activity.set(activities.LivingRoom.READING)

        # Presence Handling
        elif self.is_on(self.motion_sensor):
            self.activity.set(activities.Common.PRESENT)

        else:
            self.activity.set(activities.Common.EMPTY)

    def handle_cooldown(self) -> None:
        if self.no_activity_cooldown:
            self.cancel_timer(self.no_activity_cooldown)
        self.no_activity_cooldown = self.run_in(
            lambda *_: self.activities.livingroom.set(activities.LivingRoom.EMPTY), 3 * 60 * 60)
