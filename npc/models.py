from pydantic import BaseModel, Field
from typing import Dict

class NPCState(BaseModel):
    name: str
    personality: str
    current_room: str
    mood: str = "neutral"
    schedule: Dict[str, str]  # hour:room_name

class ConversationInput(BaseModel):
    player_message: str
    player_room: str
    npc_room: str
    current_time: str
    recent_memories: list[str]

class ConversationOutput(BaseModel):
    response: str
    mood_delta: float = 0.0
    new_memory_summary: str | None = None
