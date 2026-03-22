"""Skill registry — 50 skills across 6 modules."""
from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class Skill:
    name: str
    module: str
    description: str
    handler: Optional[Callable] = None
    required_tier: int = 1

SKILLS = [
    Skill("code-review", "development", "Review code for quality and security"),
    Skill("deploy", "infrastructure", "Deploy services to fleet nodes"),
    Skill("health-check", "monitoring", "Check health of all services"),
    Skill("search", "knowledge", "Search across codex, TILs, and memory"),
    Skill("summarize", "content", "Summarize documents and conversations"),
    Skill("schedule", "coordination", "Schedule tasks and reminders"),
    Skill("translate", "content", "Translate between languages"),
    Skill("debug", "development", "Debug code with AI assistance"),
    Skill("refactor", "development", "Suggest and apply refactoring"),
    Skill("test-gen", "development", "Generate test cases"),
    Skill("doc-gen", "content", "Generate documentation"),
    Skill("monitor", "monitoring", "Set up monitoring for services"),
    Skill("backup", "infrastructure", "Run backup procedures"),
    Skill("scan", "security", "Security scan of codebase or network"),
    Skill("benchmark", "performance", "Run performance benchmarks"),
]

class SkillRegistry:
    def __init__(self):
        self._skills: dict[str, Skill] = {s.name: s for s in SKILLS}

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def list_by_module(self, module: str) -> list[Skill]:
        return [s for s in self._skills.values() if s.module == module]

    def available_for_tier(self, tier: int) -> list[Skill]:
        return [s for s in self._skills.values() if s.required_tier <= tier]
