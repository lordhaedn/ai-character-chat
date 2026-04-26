# Ollama Backend Integration Scheme

Integration documentation for connecting Ollama AI models to a character chat application.

## Overview

This integration enables character-based conversations using Ollama's local LLM API, supporting custom personalities, context management, and configurable generation parameters.

---

## API Request Format

### Basic Request Structure

```json
{
  "model": "llama3",
  "prompt": "Character prompt with context",
  "stream": false,
  "options": {
    "temperature": 0.8,
    "top_p": 0.9,
    "repeat_penalty": 1.2
  }
}
```

### Request Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Ollama model name (e.g., `llama3`) |
| `prompt` | string | Full prompt including character context and message history |
| `stream` | boolean | Whether to stream response tokens |
| `options` | object | Generation parameters (see below) |

### Generation Options

- `temperature` (0.0-2.0): Controls creativity/randomness (default: 0.8)
- `top_p` (0.0-1.0): Nucleus sampling parameter (default: 0.9)
- `repeat_penalty` (1.0-2.0): Penalty for repetition (default: 1.2)

---

## API Response Format

```json
{
  "model": "llama3",
  "response": "Character's response text here",
  "done": true,
  "context": [1, 2, 3]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Model used for generation |
| `response` | string | Generated character response |
| `done` | boolean | Whether generation is complete |
| `context` | array | Token array for context persistence |

---

## Character Configuration

```json
{
  "personality": {
    "name": "Character Name",
    "background": "Character backstory and world context",
    "behavior": {
      "dialogue": "speech patterns and mannerisms",
      "example_1": "sample dialogue example",
      "example_2": "another dialogue example"
    }
  },
  "user": {
    "name": "User identifier for context"
  },
  "system": "Base instructions for the character"
}
```

### Configuration Components

- **Personality**: Defines character traits, speaking style, and background
- **Behavior Templates**: Example dialogues for few-shot prompting
- **User Context**: Tracks conversation participant identity

---

## Context Management

For maintaining conversation coherence:

- Store recent message history in memory
- Include last **5-10** message exchanges in prompts
- Implement context trimming for very long conversations
- Save context per character and per session
- Persist `context` array from API responses for token-level continuity

### Message History Format

```
Recent conversation history:
User: {user_message}
Assistant: {character_response}
...
```

---

## Configuration Options

Environment variables for Ollama integration:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint |
| `DEFAULT_MODEL` | `llama3` | Default model for requests |
| `TEMPERATURE` | `0.8` | Creativity parameter |
| `MAX_TOKENS` | `500` | Maximum response length |
| `REQUEST_TIMEOUT` | `30` | API timeout in seconds |

---

## Error Handling

Handle various Ollama API scenarios:

| Scenario | HTTP Status | Handling Strategy |
|----------|-------------|-------------------|
| Service unavailable | Connection refused | Retry with exponential backoff |
| Model not found | 404 | Fall back to default model |
| Request timeout | Timeout | Abort and notify user |
| Invalid response | 500 | Log error, show generic message |
| Rate limiting | 429 | Implement request queuing |

---

## Performance Considerations

- **Request Timeout**: Implement 30-second default timeout
- **Retry Logic**: Add 3 retries with exponential backoff for failed requests
- **Model Caching**: Cache model information to avoid repeated `/api/tags` calls
- **Response Monitoring**: Track API response times for performance metrics
- **Context Optimization**: Trim context to essential messages when approaching token limits

---

## Implementation Example

```python
import requests
import json
import os

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

def chat_with_character(character_config, user_message, history):
    # Build context prompt
    prompt = f"""
{character_config['system']}

{character_config['personality']['background']}

{character_config['personality']['behavior']['dialogue']}

Recent conversation:
{format_history(history)}

User: {user_message}
Assistant:"""
    
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "repeat_penalty": 1.2
            }
        },
        timeout=30
    )
    
    return response.json()['response']
```

---

## Notes

- Ensure Ollama service is running before starting the application
- Character context should be loaded at application startup
- Consider implementing conversation summarization for very long sessions
