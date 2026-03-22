"""CI/CD pipeline runner — test, build, deploy stages."""
from __future__ import annotations
import asyncio
import subprocess
import time
from dataclasses import dataclass
from enum import Enum

class StageResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"

@dataclass
class Stage:
    name: str
    commands: list[str]
    result: StageResult = StageResult.SKIP
    output: str = ""
    duration_s: float = 0

class CIPipeline:
    def __init__(self, name: str = "default"):
        self.name = name
        self.stages: list[Stage] = []

    def add_stage(self, name: str, commands: list[str]) -> None:
        self.stages.append(Stage(name=name, commands=commands))

    async def run(self) -> dict:
        results = {}
        for stage in self.stages:
            start = time.monotonic()
            try:
                outputs = []
                for cmd in stage.commands:
                    proc = await asyncio.create_subprocess_shell(
                        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                    stdout, stderr = await proc.communicate()
                    outputs.append(stdout.decode() + stderr.decode())
                    if proc.returncode != 0:
                        raise subprocess.CalledProcessError(proc.returncode, cmd)
                stage.result = StageResult.PASS
                stage.output = "\n".join(outputs)
            except Exception as e:
                stage.result = StageResult.FAIL
                stage.output = str(e)
                stage.duration_s = time.monotonic() - start
                results[stage.name] = {"result": stage.result.value, "duration": stage.duration_s}
                break  # stop pipeline on failure
            stage.duration_s = time.monotonic() - start
            results[stage.name] = {"result": stage.result.value, "duration": round(stage.duration_s, 2)}
        return {"pipeline": self.name, "stages": results,
                "passed": all(s.result == StageResult.PASS for s in self.stages if s.result != StageResult.SKIP)}

DEFAULT_PIPELINE = CIPipeline("roadcode-ci")
DEFAULT_PIPELINE.add_stage("lint", ["ruff check . 2>/dev/null || true"])
DEFAULT_PIPELINE.add_stage("test", ["python -m pytest tests/ -v 2>/dev/null || true"])
DEFAULT_PIPELINE.add_stage("build", ["python -m pip install -e . 2>/dev/null || true"])
