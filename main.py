import asyncio
import typer
from typing import Optional
from config import settings
from world.state import GameState
from npc.brain import SarahBrain
from npc.models import ConversationInput
from memory.qdrant import QdrantMemoryRepository
from world.models import MemoryEntry
from datetime import datetime

app = typer.Typer()
game = GameState()
memory_repo = QdrantMemoryRepository()
brain = SarahBrain(memory_repo)

@app.command()
def look():
    """Examine the current room."""
    room = game.rooms[game.player_room]
    typer.echo(f"You are in the {room.name}.")
    typer.echo(room.description)
    if room.contents:
        typer.echo(f"You see: {', '.join(room.contents)}")
    game.advance_time_action("look")

@app.command()
def go(room_name: str):
    """Move to another room."""
    if game.move_player(room_name.lower()):
        typer.echo(f"You moved to the {room_name}.")
    else:
        typer.echo(f"You can't go to the {room_name}.")
    
    # Update NPC location based on new time
    schedule = {"07": "kitchen", "22": "bedroom"}
    game.update_npc_location("Sarah", schedule)
    game.advance_time_action("go")

@app.command()
def talk(message: str):
    """Talk to Sarah."""
    async def _talk():
        if game.npc_location != game.player_room:
            type_msg = f"Sarah is not here. She is in the {game.npc_location}."
            typer.echo(type_msg)
            return

        typer.echo(f"You say: '{message}'")
        
        recent_memories = []
        try:
            memories = await memory_repo.get_recent(limit=3)
            recent_memories = [m.content for m in memories]
        except Exception as e:
            typer.echo(f"(Memory error: {e})")

        conv_input = ConversationInput(
            player_message=message,
            player_room=game.player_room,
            npc_room=game.npc_location,
            current_time=str(game.current_time),
            recent_memories=recent_memories
        )

        try:
            response = await brain.converse(conv_input)
            typer.echo(f"Sarah: {response.response}")
            
            if response.new_memory_summary:
                entry = MemoryEntry(
                    timestamp=datetime.now(),
                    role="assistant",
                    content=response.new_memory_summary,
                    room=game.npc_location
                )
                await memory_repo.store(entry)
                
        except Exception as e:
            typer.echo(f"Error during conversation: {e}")

        game.advance_time_action("talk")

    asyncio.run(_talk())

@app.command()
def where():
    """Check Sarah's location."""
    typer.echo(f"Sarah is in the {game.npc_location}.")

@app.command()
def time_info():
    """Check the current game time."""
    typer.echo(f"Current time: {game.current_time}")

@app.command()
def exit():
    """Exit the game."""
    typer.echo("Goodbye!")
    raise typer.Exit()

if __name__ == "__main__":
    async def setup_and_run():
        await memory_repo.setup()
    
    asyncio.run(setup_and_run())
    app()
