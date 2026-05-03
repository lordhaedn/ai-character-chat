from world.models import GameTime, WorldState, Room
from world.rooms import get_initial_rooms
from typing import Optional

class GameState:
    def __init__(self):
        self.rooms = get_initial_rooms()
        self.player_room = "hallway"
        self.npc_location = "kitchen"
        self.current_time = GameTime(hour=7, minute=0, day=1)

    def get_world_state(self) -> WorldState:
        return WorldState(
            player_room=self.player_room,
            npc_location=self.npc_location,
            current_time=self.current_time,
            rooms=self.rooms
        )

    def move_player(self, room_name: str) -> bool:
        if room_name in self.rooms:
            self.player_room = room_name
            self.advance_time(5)  # Moving takes 5 minutes
            return True
        return False

    def advance_time(self, minutes: int):
        self.current_time.minute += minutes
        while self.current_time.minute >= 60:
            self.current_time.minute -= 60
            self.current_time.hour += 1
        
        if self.current_time.hour >= 24:
            self.current_time.hour -= 24
            self.current_time.day += 1

    def update_npc_location(self, npc_name: str, schedule: dict[str, str]):
        # Simple schedule check: hour:room_name
        hour_str = f"{self.current_time.hour:02d}"
        if hour_str in schedule:
            self.npc_location = schedule[hour_str]
        elif self.current_time.hour >= 22:
            self.npc_location = "bedroom"
        elif self.current_time.hour < 7:
            self.npc_location = "bedroom"
        else:
            # Random movement or stay in kitchen if not specified
            pass

    def advance_time_action(self, action_type: str):
        if action_type == "look":
            self.advance_time(1)
        elif action_type == "talk":
            self.advance_time(2)
