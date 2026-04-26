# Backend Implementation Plan

## Server Structure
- Create Express.js server with proper middleware
- Implement CORS for frontend communication
- Set up routing for API endpoints
- Add error handling middleware

## API Endpoints
1. `GET /api/characters` - List all available characters
2. `GET /api/characters/:id` - Get specific character details
3. `POST /api/chat` - Send message to character and get response

## Ollama Integration
- Create service module to communicate with Ollama API
- Handle model selection and configuration
- Implement proper error handling for API failures
- Manage chat context/history for conversations

## Character System
- Create character loader to read markdown files
- Parse character data from markdown format
- Implement character validation
- Cache character data for performance

## File Structure
```
backend/
├── server.js
├── config/
│   └── ollama.js
├── controllers/
│   ├── characterController.js
│   └── chatController.js
├── routes/
│   └── api.js
├── services/
│   ├── ollamaService.js
│   └── characterService.js
├── characters/
│   └── sample-character.md
├── middleware/
│   └── errorHandling.js
└── utils/
    └── markdownParser.js
```

## Dependencies
- express: Web framework
- cors: Cross-origin resource sharing
- axios: HTTP client for Ollama API
- marked: Markdown parser
- dotenv: Environment variable management

## Environment Variables
- OLLAMA_HOST: URL for Ollama API (default: http://localhost:11434)
- PORT: Server port (default: 3001)
- MODEL: Default model to use (default: gemma4)
