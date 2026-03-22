# Getting Started with RoadCode

## Prerequisites

- Python 3.10+
- Node.js 18+ (optional, for web components)
- Git

## Quick Start

```bash
# Clone
git clone https://github.com/BlackRoad-OS-Inc/RoadCode.git
cd RoadCode

# Install Python deps
pip install -e .

# Run the gateway
uvicorn services.gateway.main:app --port 8000

# Or use the CLI
python -m cli.br.main status
python -m cli.br.main agents
python -m cli.br.main search "sovereign computing"
```

## Project Structure

- `agents/` — 10 named agents (Cece, Lucidia, Operator, Alice, Cecilia, Octavia, Aria, Gematria, Anastasia, Alexandria)
- `core/` — Execution engine, memory store, event bus, scheduler
- `services/` — API gateway, search, compute, analytics, inference
- `system/` — Auth, identity, monitoring, security, networking
- `cli/` — `br` command-line interface
- `infrastructure/` — Cloudflare, Terraform, K8s, CI/CD
- `models/` — LLM routing, embeddings, speech, vision
- `web/` — Dashboard, design system, components

## Running Tests

```bash
pytest tests/ -v
```

## Fleet Nodes

| Node | IP | Role |
|------|----|------|
| Alice | 192.168.4.49 | Gateway |
| Cecilia | 192.168.4.96 | Inference |
| Octavia | 192.168.4.101 | Platform |
| Aria | 192.168.4.98 | Edge |
| Lucidia | 192.168.4.38 | DNS/Apps |
| Gematria | DO NYC3 | TLS Edge |
| Anastasia | DO NYC1 | Compute |

## Next Steps

1. Read `docs/architecture/overview.md`
2. Explore `agents/` to understand the agent system
3. Try `python -m agents.tools.cli roster` to see all agents
4. Check `config/services/agents.yaml` for fleet configuration
