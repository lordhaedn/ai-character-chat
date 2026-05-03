from typing import Protocol
from datetime import datetime
from world.models import MemoryEntry

class MemoryRepository(Protocol):
    async def store(self, entry: MemoryEntry) -> None:
        """Store a new memory entry."""
        ...

    async def retrieve(self, query: str, limit: int = 3) -> list[MemoryEntry]:
        """Retrieve relevant memories based on a query."""
        ...

    async def get_recent(self, limit:int = 3) -> list[MemoryEntry]:
        """Retrieve the most recent memory entries."""
        ...
