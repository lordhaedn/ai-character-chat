# NPC Memory Prototype - Stage 1

A prototype of an interactive NPC (Sarah) with long-term memory using **PydanticAI**, **Qdrant**, and **Ollama**.

## Features

- **Interactive CLI**: Navigate a 3-room house (Kitchen, Bedroom, Hallway) and interact with Sarah.
- **Long-term Memory**: Sarah remembers past conversations using vector embeddings stored in Qdrant.
- **Dynamic Personality**: Sarah's mood and behavior change based on the time of day and your interactions.
- **Spatial Awareness**: Sarah only responds if you are in the same room.
- **Structured Output**: Uses PydanticAI to ensure Sarah's responses follow a strict schema.

## Prerequisites

Before running the prototype, ensure you have the following running on your local machine:

1.  **Ollama**:
    - Install [Ollama](https://ollama.com/).
    - Pull the required model:
      ```bash
      ollama pull qwen3.6:27b
      ```
    - Ensure Ollama is running and accessible at `http://localhost:11434`.

2.		**Qdrant**:
    - Run Qdrant via Docker:
      ```bash
      docker run -p 6333:6333 qdrant/qdrant
      ```
    - Or ensure a Qdrant instance is running at `http://localhost:6333`.

3.  **Python 3.11+**

## Installation

1.  Clone the repository.
2.  Create a virtual environment and install dependencies:
    ```bash
    # Using pip
    pip install -e .
    
    # Or using uv
    uv pip install -e .
    ```
3.  Configure your environment:
    ```bash
    cp .env.example .env
    ```
    *(Optional: Edit `.env` to change model names or connection URLs.)*

## Running the Prototype

Launch the interactive CLI:

```bash
python main.py
```

## Available Commands

Once the game is running, you can use the following commands:

- `look`: Examine the current room and its contents.
- `go <room_name>`: Move to another room (e.g., `go kitchen`, `go bedroom`).
- `talk "<message>"`: Speak to Sarah (only works if she is in the same room).
- `where`: Check Sarah's current location.
- `time-info`: Check the current game time.
- `exit`: End the session.

### Example Session

```text
$ python main.py
You are in the hallway.
You see: a small rug, a coat rack.

$ go kitchen
You moved to the kitchen.
Sarah is in the kitchen.

$ talk "How are you doing today?"
You say: 'How are you doing today?'
Sarah: I'm feeling a bit grumpy, I haven't had my coffee yet.

$ talk "I brought you some coffee!"
You say: 'I brought you some coffee!'
Sarah: Oh, thank you! That's much better.
```

## Architecture

- **`main.py`**: Typer-based CLI entry point.
- **`world/`**: Man: Handles game state, room definitions, and time advancement.
- **`npc/`**: The "brain" of Sarah, using Pyd-anticAI for structured LLM interactions and behavior logic.
- **`memory/`**: An abstraction layer for the `MemoryRepository`, implemented with `Qdrant`.
- **`config.py`**: Centralized configuration using `pydantic-settings`.
