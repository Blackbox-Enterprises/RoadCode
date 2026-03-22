"""WireGuard mesh config generator and peer management."""
from __future__ import annotations
from dataclasses import dataclass, field
import ipaddress

@dataclass
class WGPeer:
    name: str
    public_key: str
    endpoint: str
    allowed_ips: str
    wg_ip: str
    keepalive: int = 25

@dataclass
class WGInterface:
    name: str
    address: str
    listen_port: int
    private_key: str = "[PRIVATE_KEY]"
    peers: list[WGPeer] = field(default_factory=list)

MESH_PEERS = [
    WGPeer("alice", "[ALICE_PUB]", "192.168.4.49:51820", "10.8.0.1/32", "10.8.0.1"),
    WGPeer("cecilia", "[CECILIA_PUB]", "192.168.4.96:51820", "10.8.0.2/32", "10.8.0.2"),
    WGPeer("octavia", "[OCTAVIA_PUB]", "192.168.4.101:51820", "10.8.0.3/32", "10.8.0.3"),
    WGPeer("aria", "[ARIA_PUB]", "192.168.4.98:51820", "10.8.0.4/32", "10.8.0.4"),
    WGPeer("lucidia", "[LUCIDIA_PUB]", "192.168.4.38:51820", "10.8.0.5/32", "10.8.0.5"),
    WGPeer("gematria", "[GEMATRIA_PUB]", "gematria.nyc3:51820", "10.8.0.6/32", "10.8.0.6"),
    WGPeer("anastasia", "[ANASTASIA_PUB]", "anastasia.nyc1:51820", "10.8.0.7/32", "10.8.0.7"),
]

class WireGuardConfig:
    def __init__(self):
        self.peers = {p.name: p for p in MESH_PEERS}

    def generate_config(self, node_name: str, listen_port: int = 51820) -> str:
        node = self.peers.get(node_name)
        if not node:
            raise ValueError(f"Unknown node: {node_name}")
        lines = [
            "[Interface]",
            f"Address = {node.wg_ip}/24",
            f"ListenPort = {listen_port}",
            "PrivateKey = [PRIVATE_KEY]",
            "",
        ]
        for peer in self.peers.values():
            if peer.name == node_name:
                continue
            lines.extend([
                "[Peer]",
                f"# {peer.name}",
                f"PublicKey = {peer.public_key}",
                f"Endpoint = {peer.endpoint}",
                f"AllowedIPs = {peer.allowed_ips}",
                f"PersistentKeepalive = {peer.keepalive}",
                "",
            ])
        return "\n".join(lines)

    def generate_all(self) -> dict[str, str]:
        return {name: self.generate_config(name) for name in self.peers}

    def add_peer(self, name: str, public_key: str, endpoint: str, wg_ip: str) -> WGPeer:
        peer = WGPeer(name, public_key, endpoint, f"{wg_ip}/32", wg_ip)
        self.peers[name] = peer
        return peer

    def mesh_status(self) -> list[dict]:
        return [{"name": p.name, "endpoint": p.endpoint, "wg_ip": p.wg_ip} for p in self.peers.values()]
