The design below assumes:
- **Ollama** runs on your host (accessible via `host.docker.internal:11434`)
- **SQLite** for now (needs persistent volume), with a clean upgrade path to Postgres/MySQL later via Docker Compose networks

### Hardened Dockerfile

```dockerfile
# -------- Build stage --------
FROM node:20-alpine AS builder
WORKDIR /build

# Copy only manifests first (better layer caching)
COPY package*.json ./

# Install WITHOUT running lifecycle scripts (prevents postinstall exploits)
# --only=production would skip devDependencies; omit if you need build tools
RUN npm ci --ignore-scripts

# Copy application code
COPY server.js ./

# -------- Runtime stage --------
FROM node:20-alpine AS runtime

# Security: Install dumb-init for proper signal handling (PID 1 problem)
RUN apk add --no-cache dumb-init

# Create non-root user (node user exists in Alpine image but let's be explicit)
RUN mkdir -p /app/data && chown -R node:node /app
WORKDIR /app

# Copy only what's needed from builder
COPY --from=builder --chown=node:node /build/node_modules ./node_modules
COPY --from=builder --chown=node:node /build/server.js ./

# Database will live here (SQLite for now). Separate volume mount recommended.
RUN mkdir -p /app/data && chown node:node /app/data

# Drop privileges
USER node

# Environment
ENV NODE_ENV=production
ENV OLLAMA_URL=http://host.docker.internal:11434
ENV DB_PATH=/app/data/app.db

EXPOSE 3000

# dumb-init handles signals properly; exec node replaces shell process
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```

### docker-compose.yml (production-ready)

```yaml
services:
  api:
    build: .
    container_name: chat_api
    restart: unless-stopped
    
    # Security hardening
    read_only: true  # Root filesystem read-only
    user: "1000:1000"  # node user UID:GID
    
    # Capabilities: Drop everything, add back only what's needed (none for pure Node)
    cap_drop:
      - ALL
    
    # Storage: RW volume for SQLite + tmpfs for any temp files
    volumes:
      - ./data:/app/data:rw  # SQLite persistence
      - /tmp:/tmp:noexec,nosuid,size=100m  # Ephemeral tmp
    
    # Networking
    ports:
      - "127.0.0.1:3000:3000"  # Bind to localhost only, not 0.0.0.0
    
    environment:
      - OLLAMA_URL=http://host.docker.internal:11434
      
    # Future: Add your DB container here, remove host.docker.internal above
    # networks:
    #   - backend
      
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

# Future database addition:
# networks:
#   backend:
#     driver: bridge
```

### Required additions

**.dockerignore** (prevents leaking host files):
```
node_modules
npm-debug.log
.env
.git
data/  # Don't bake DB into image
*.db
```

**.env.example**:
```
OLLAMA_URL=http://host.docker.internal:11434
DB_PATH=/app/data/app.db
PORT=3000
```

### Security choices explained

| Layer | What it does |
|-------|-------------|
| `--ignore-scripts` | Blocks supply-chain attacks via malicious `postinstall` hooks |
| Multi-stage | Build tools (gcc, python) don't ship in final image |
| `read_only: true` | Container can't modify its own code if compromised |
| `user: "1000:1000"` | Escaped container processes run as unprivileged user |
| `cap_drop: ALL` | Removes 40+ Linux capabilities (chown, net_admin, etc.) |
| `dumb-init` | Prevents zombie processes; handles SIGTERM for clean shutdown |
| `127.0.0.1:3000` | Container only accessible via localhost, not exposed to LAN |

### Migration path for "real" database

When you outgrow SQLite, swap the volume for a service:

```yaml
services:
  api:
    environment:
      - DATABASE_URL=postgres://chat_api:${DB_PASSWORD}@db:5432/app
    # Remove host.docker.internal, use internal Docker DNS instead
    
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: chat_api
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    # Postgres has its own security hardened options...

volumes:
  postgres_data:
```

The current SQLite setup keeps everything simple while the `read_only` + dedicated volume pattern translates directly to Postgres container networking later.
