"""Security scanner — open ports, weak keys, exposed secrets."""
from __future__ import annotations
import asyncio
import re
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Finding:
    severity: str  # critical, high, medium, low, info
    category: str
    title: str
    details: str
    node: str = ""
    file: str = ""

class SecurityScanner:
    SECRET_PATTERNS = [
        (r'(?:password|passwd|pwd)\s*[=:]\s*["\']?[\w!@#$%]+', "Hardcoded password"),
        (r'(?:api[_-]?key|apikey)\s*[=:]\s*["\']?[\w-]{20,}', "API key in code"),
        (r'(?:secret|token)\s*[=:]\s*["\']?[\w-]{20,}', "Secret/token in code"),
        (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----', "Private key in code"),
        (r'ghp_[A-Za-z0-9]{36}', "GitHub PAT"),
        (r'sk-[A-Za-z0-9]{48}', "OpenAI API key"),
    ]

    async def scan_files(self, path: str, extensions: list[str] | None = None) -> list[Finding]:
        extensions = extensions or [".py", ".js", ".sh", ".yaml", ".yml", ".toml", ".env", ".json"]
        findings = []
        for filepath in Path(path).rglob("*"):
            if filepath.suffix not in extensions or ".git" in filepath.parts:
                continue
            try:
                content = filepath.read_text(errors="ignore")
                for pattern, title in self.SECRET_PATTERNS:
                    if re.search(pattern, content, re.IGNORECASE):
                        findings.append(Finding("high", "secrets", title, f"Found in {filepath}", file=str(filepath)))
            except Exception:
                continue
        return findings

    async def scan_ports(self, host: str, ports: list[int] | None = None) -> list[Finding]:
        ports = ports or [22, 80, 443, 3000, 3100, 5432, 6333, 6379, 8080, 8443, 9090, 11434]
        findings = []
        for port in ports:
            try:
                _, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=2)
                writer.close()
                await writer.wait_closed()
                findings.append(Finding("info", "ports", f"Port {port} open", f"{host}:{port}", node=host))
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                pass
        return findings

    async def full_audit(self, code_path: str = ".", hosts: list[str] | None = None) -> dict:
        hosts = hosts or ["192.168.4.49", "192.168.4.96", "192.168.4.101", "192.168.4.98", "192.168.4.38"]
        file_findings = await self.scan_files(code_path)
        port_findings = []
        for host in hosts:
            port_findings.extend(await self.scan_ports(host))
        all_findings = file_findings + port_findings
        return {
            "total": len(all_findings),
            "by_severity": {s: sum(1 for f in all_findings if f.severity == s) for s in ["critical", "high", "medium", "low", "info"]},
            "findings": [{"severity": f.severity, "category": f.category, "title": f.title, "details": f.details} for f in all_findings],
        }
