# RoadCode

> Canonical RoadCode workspace and automation hub for Blackbox-Enterprises.

Part of the [BlackRoad OS](https://blackroad.io) ecosystem — [Blackbox-Enterprises](https://github.com/Blackbox-Enterprises)

---

# Blackbox-Enterprises — RoadCode

> Developer Tools & Enterprise division of [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc)

Developer tools, IDE integrations, and enterprise-grade automation. Home of BlackBox IDE and the programming tools that power the BlackRoad development workflow.

**Domain**: [blackboxprogramming.io](https://blackboxprogramming.io)

## Products

| Product | What It Does |
|---------|-------------|
| **BlackBox IDE** | Code editor with local AI completion — no cloud round-trips |
| **Workflow Engine** | Task automation across the 7-node fleet (n8n-based) |
| **Enterprise Integrations** | Connectors for CI/CD, monitoring, deployment pipelines |
| **CLI Toolkit** | `br` command — unified interface to the entire BlackRoad stack |

## Org Hierarchy

```
BlackRoad-OS-Inc (Parent — 254 repos, 67 agents, 7 nodes)
  └── Blackbox-Enterprises (Developer Tools & Enterprise)
      ├── RoadCode          ← this repo (workspace + automation)
      ├── operator           ← CLI tools + enterprise scripts
      └── source             ← BlackBox IDE + integrations
```

## Repos in This Org

- [`RoadCode`](https://github.com/Blackbox-Enterprises/RoadCode) — Workspace hub (this repo)
- [`operator`](https://github.com/Blackbox-Enterprises/operator) — CLI + automation
- [`source`](https://github.com/Blackbox-Enterprises/source) — Source tree

## Developer Experience

- **Local AI completion**: Ollama models on the fleet power code suggestions — no data leaves the device
- **67 agents** available for code review, debugging, refactoring, and deployment
- **Unified search**: `br search-all` queries 1,383 entries from 23 indexers
- **Gitea primary**: 239 repos on Octavia, GitHub is the mirror

## How It Connects

- **Parent**: [BlackRoad-OS-Inc](https://github.com/BlackRoad-OS-Inc) — central coordination
- **AI**: [BlackRoad-AI](https://github.com/BlackRoad-AI) — models power IDE completion + code review
- **Cloud**: [BlackRoad-Cloud](https://github.com/BlackRoad-Cloud) — deployment targets for enterprise workflows
- **Security**: [BlackRoad-Security](https://github.com/BlackRoad-Security) — secret scanning + dependency audits
- **Labs**: [BlackRoad-Labs](https://github.com/BlackRoad-Labs) — experimental dev tools tested before promotion

## License

Proprietary — BlackRoad OS, Inc. See [LICENSE](./LICENSE).

---

*Remember the Road. Pave Tomorrow.*
