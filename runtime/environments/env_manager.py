"""Environment manager — virtualenv and dependency management."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Environment:
    name: str
    path: str
    python_version: str
    packages: list[str]

class EnvManager:
    def __init__(self, base_path: str = ".venvs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def create(self, name: str) -> Environment:
        env_path = self.base_path / name
        subprocess.run([sys.executable, "-m", "venv", str(env_path)], check=True)
        return Environment(name=name, path=str(env_path),
                           python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
                           packages=[])

    def install(self, name: str, packages: list[str]) -> bool:
        pip = self.base_path / name / "bin" / "pip"
        if not pip.exists():
            return False
        result = subprocess.run([str(pip), "install"] + packages, capture_output=True)
        return result.returncode == 0

    def list_envs(self) -> list[str]:
        return [d.name for d in self.base_path.iterdir() if d.is_dir() and (d / "bin" / "python").exists()]

    def remove(self, name: str) -> bool:
        import shutil
        env_path = self.base_path / name
        if env_path.exists():
            shutil.rmtree(env_path)
            return True
        return False
