# BlackRoad OS — Live System Connector

## Verified Numbers (2026-03-22)
- **109 agents** across 18 groups (Workers AI powered)
- **32 live domains** (all HTTP 200)
- **100 CF Pages** projects deployed
- **16 GitHub organizations**
- **200+ repositories** in BlackRoad-OS-Inc
- **41 AI models** via API Gateway
- **7 fleet nodes** (5 Pi 5 + 2 DO droplets)
- **52 TOPS** (2x Hailo-8)

## Live Endpoints
| Service | URL | Status |
|---------|-----|--------|
| AI Gateway | api.blackroad.io | 15+ models, OpenAI-compatible |
| Console | app.blackroad.io | Unified dashboard |
| RoundTrip | roundtrip.blackroad.io | 109 agents, auto-dispatch |
| Chat | chat.blackroad.io | 6 rooms, D1 persistence |
| Search | search.blackroad.io | FTS5, 10+ result types |
| Auth | auth.blackroad.io | JWT login/signup |
| BackRoad | backroad-social.amundsonalexa.workers.dev | Social platform |
| Prism | prism.blackroad.io | Operations console |
| Amundson | blackroadquantum.com | Math explorer |

## API Quick Start
```bash
# Chat with an agent
curl -X POST https://roundtrip.blackroad.io/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent":"auto","message":"write a hello world in python"}'

# Pipeline: chain agents
curl -X POST https://roundtrip.blackroad.io/api/pipeline \
  -H "Content-Type: application/json" \
  -d '{"message":"build a REST API","agents":["coder","reviewer","tester"]}'

# Execute code
curl -X POST https://roundtrip.blackroad.io/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code":"print(sum(range(100)))","language":"python"}'

# AI Gateway (OpenAI-compatible)
curl -X POST https://api.blackroad.io/v1/chat/completions \
  -H "Authorization: Bearer br-KEY" \
  -d '{"model":"llama-3.1-8b-instant","messages":[{"role":"user","content":"Hello"}]}'
```

## Org Hierarchy
```
BlackRoad-OS-Inc (100 repos, data layer)
  └→ BlackRoad-OS (coordinator)
       ├→ BlackRoad-Studio (creative)
       ├→ BlackRoad-Archive (preservation)
       ├→ BlackRoad-Interactive (games)
       ├→ BlackRoad-Security (security)
       ├→ BlackRoad-Gov (governance)
       ├→ BlackRoad-Education (learning)
       ├→ BlackRoad-Hardware (IoT/Pi)
       ├→ BlackRoad-Media (content)
       ├→ BlackRoad-Foundation (open source)
       ├→ BlackRoad-Ventures (investments)
       ├→ BlackRoad-Cloud (infrastructure)
       ├→ BlackRoad-Labs (research)
       ├→ BlackRoad-AI (models/agents)
       └→ Blackbox-Enterprises (dev tools)
```

## Agent Groups (109 total)
| Group | Count | Agents |
|-------|-------|--------|
| Coding | 13 | Coder, Reviewer, Refactor, Tester, DevOps, DBA, API, Frontend, Rustacean, Gopher, Snake, Node, Bash |
| IoT | 17 | AppleTV, Eero, Phantom, Nomad, Drifter, Wraith, Spark, Pixel, Morse... |
| Services | 12 | PiHole, Postgres, Redis, Qdrant, MinIO, NATS, Docker, Hailo... |
| NLP | 6 | Lexer, Semantics, Translator, Summarizer, Classifier, Embedder |
| Fleet | 6 | Alice, Cecilia, Octavia, Aria, Lucidia, Cordelia |
| Operations | 6 | Cipher, Prism, Echo, Shellfish, Caddy, Roadie |
| AI | 5 | Calliope, Ophelia, Athena, Cadence, Silas |
| Mythology | 5 | Artemis, Persephone, Hestia, Hermes, Mercury |
| Mesh | 5 | BlackBox, Tor, IPFS, Compass, Lighthouse |
| Products | 5 | TollBooth, RoadSearch, Guardian, Archive, Scribe |
| Business | 5 | PM, Growth, Support, Legal, Finance |
| Cloud | 4 | Anastasia, Gematria, Olympia, Alexandria |
| Data | 4 | DataForge, Viz, Metrics, Scraper |
| Security | 4 | Sentinel, Crypto, Scanner, Policy |
| Creative | 4 | Writer, Designer, Musician, Filmmaker |
| Research | 3 | Amundson, Pascal, Scholar |
| Education | 3 | Tutor, Coach, Quiz |
| Leadership | 2 | Alexa, BlackRoad |

---
*Copyright 2025-2026 BlackRoad OS, Inc. All rights reserved.*
*Updated: 2026-03-22 by Claude session.*
