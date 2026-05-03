import asyncio
from datetime import datetime
from typing import List
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from openai import AsyncOpenAI
from config import settings
from memory.repository import MemoryRepository
from world.models import MemoryEntry

class QdrantMemoryRepository(MemoryRepository):
    def __init__(self):
        self.client = AsyncQdrantClient(url=settings.QDRANT_URL)
        self.collection_name = settings.QDRANT_COLLECTION
        self.vector_size = 768  # Assuming nomic-embed-text or similar
        self.embeddings_client = AsyncOpenAI(
            base_url=settings.OLLAMA_URL,
            api_key="ollama"  # Required but ignored by Ollama
        )

    async def setup(self):
        """Initialize the collection."""
        collections = await self.client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)
        
        if not exists:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.COSINE),
            )

    async def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding using Ollama."""
        response = await self.embeddings_client.embeddings.create(
            model=settings.OLLAMA_MODEL,
            input=text
        )
        return response.data[0].embedding

    async def store(self, entry: MemoryEntry) -> None:
        """Store a new memory entry with embedding."""
        embedding = await self._get_embedding(entry.content)
        
        await self.client.upsert(
            collection_name=self._collection_name_fix(),
            points=[
                models.PointStruct(
                    id=str(datetime.now().timestamp()), # Using timestamp as ID for simplicity
                    vector=embedding,
                    payload={
                        "content": entry.content,
                        "role": entry.role,
                        "room": entry.room,
                        "timestamp": entry.timestamp.isoformat(),
                        "is_summary": entry.is_summary
                    }
                )
            ]
        )

    def _collection_name_fix(self):
        return self.collection_name

    async def retrieve(self, query: str, limit: int = 3) -> List[MemoryEntry]:
        """Retrieve relevant memories based on a query."""
        query_embedding = await self._get_embedding(query)
        
        search_result = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        
        memories = []
        for hit in search_result:
            payload = hit.payload
            memories.append(MemoryEntry(
                timestamp=datetime.fromisoformat(payload["timestamp"]),
                role=payload["role"],
                content=payload["content"],
                room=payload["room"],
                is_summary=payload["is_summary"]
            ))
        return memories

    async def get_recent(self, limit: int = 3) -> List[MemoryEntry]:
        """Retrieve the most recent memory entries."""
        # For prototype, we'll just use the search with a dummy query to get recent ones.
        return await self.retrieve("recent", limit=limit)
