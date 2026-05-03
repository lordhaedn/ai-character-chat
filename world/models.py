from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict

class GameTime(BaseModel):
    hour: int = Field(ge=0, le=23)
    minute: int = Field(ge=0, le=59)
    day: int = Field(default=1)

    def __str__(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d} (Day {self.day})"

class Room(BaseModel):
    name: str
    description: str
    contents: List[str] = []

class WorldState(BaseModel):
    player_room: str
    npc_location: str
    current_time: GameTime
    rooms: Dict[str, Room]

class NPCState(BaseModel):
    name: str
    personality: str
    current_room: str
    mood: str = "neutral"
    schedule: Dict[str, str]  # hour:room_name

class MemoryEntry(BaseModel):
    timestamp: datetime
    role: str  # 'user' or 'assistant'
    content: str
    room: str
    is_summary: bool = False
