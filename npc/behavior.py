from world.models import GameTime, WorldState
from npc.models import NPCState

class NPCBehavior:
    def __init__(self, npc_state: NPCState):
        self.npc_state = npc_state

    def update_location(self, current_time: GameTime):
        """Update NPC location based on schedule."""
        hour_str = f"{current_time.hour:02d}"
        
        # Schedule: 07:00 Kitchen, 2cap:00 Bedroom, otherwise random/default
        if hour_str == "07" or hour_str == "08":
            self.npc_state.current_room = "kitchen"
        elif current_time.hour >= 22 or current_time.hour < 7:
            self.npc_state.current_room = "bedroom"
        else:
            # For the prototype, let's just keep her in the kitchen or hallway
            # In a real implementation, this would be more dynamic
            pass

    def can_interact(self, player_room: str) -> bool:
        """Check if the player is in the same room as the NPC."""
        return self.npc_state.current_room == player_room
