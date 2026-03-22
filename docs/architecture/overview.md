# RoadCode Architecture

## Overview

RoadCode is the canonical monorepo workspace for all BlackRoad organizations. It provides:

- **Core**: Execution engine, memory, messaging, scheduling, state management
- **Agents**: 10 named agents across 7 hardware nodes
- **Services**: Gateway, search, compute, analytics, inference
- **Infrastructure**: Cloudflare Workers, Terraform, K8s, CI/CD
- **CLI**: `br` command-line interface for fleet management

## Directory Structure

```
RoadCode/
├── agents/          # Agent definitions and skills
├── api/             # REST, GraphQL, WebSocket endpoints
├── cli/             # br CLI tools
├── config/          # Environment and service configuration
├── core/            # Execution engine, memory, messaging
├── data/            # Runtime data (gitignored)
├── docs/            # Documentation
├── infrastructure/  # Deploy configs (CF, TF, K8s)
├── models/          # AI model routing and management
├── nodes/           # Fleet node configurations
├── runtime/         # Container and worker runtime
├── scripts/         # Bootstrap, deploy, maintenance
├── services/        # Microservices (gateway, search, etc.)
├── system/          # Auth, identity, monitoring, security
├── tests/           # Unit, integration, performance tests
└── web/             # Frontend apps and dashboards
```

## Fleet Nodes

| Node | Hardware | Role | Key Services |
|------|----------|------|-------------|
| Alice | Pi 4B 8GB | Gateway | nginx, Pi-hole, PostgreSQL, Qdrant |
| Cecilia | Pi 4B 8GB + Hailo-8 | Inference | Ollama (16 models), MinIO |
| Octavia | Pi 4B 8GB + Hailo-8 | Platform | Gitea, Docker, NATS |
| Aria | Pi 4B 4GB | Edge | Headscale, Cloudflared |
| Lucidia | Pi 4B 8GB | DNS/Apps | PowerDNS, Ollama, nginx |
| Gematria | DO Droplet | TLS Edge | Caddy, Ollama, PowerDNS |
| Anastasia | DO Droplet | Compute | Docker, workers |

## Principles

1. **Sovereign first** — every service runs on our hardware
2. **Zero external dependency** — except Stripe and GoDaddy
3. **Agent-native** — every operation can be performed by an agent
4. **Memory-persistent** — hash-chained, FTS5-indexed, never lost
