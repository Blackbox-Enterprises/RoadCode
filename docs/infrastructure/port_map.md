# Port Map — Every Port on Every Node

## Alice (192.168.4.49)
| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 53 | Pi-hole DNS | UDP/TCP |
| 80 | nginx | TCP |
| 443 | nginx (TLS) | TCP |
| 5432 | PostgreSQL | TCP |
| 6333 | Qdrant | TCP |
| 6379 | Redis | TCP |
| 8080 | Pi-hole Admin | TCP |
| 51820 | WireGuard | UDP |

## Cecilia (192.168.4.96)
| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 9000 | MinIO | TCP |
| 9001 | MinIO Console | TCP |
| 5432 | PostgreSQL | TCP |
| 8086 | InfluxDB | TCP |
| 11434 | Ollama | TCP |
| 51820 | WireGuard | UDP |

## Octavia (192.168.4.101)
| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 3100 | Gitea | TCP |
| 4222 | NATS | TCP |
| 8222 | NATS Monitor | TCP |
| 9001-9015 | Workers | TCP |
| 3500 | PaaS Deploy API | TCP |
| 51820 | WireGuard | UDP |

## Aria (192.168.4.98)
| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 80 | nginx | TCP |
| 443 | nginx (TLS) | TCP |
| 8080 | Headscale | TCP |
| 8086 | InfluxDB | TCP |
| 51820 | WireGuard | UDP |

## Lucidia (192.168.4.38)
| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 53 | PowerDNS | UDP/TCP |
| 80 | nginx (334 apps) | TCP |
| 443 | nginx (TLS) | TCP |
| 8081 | PowerDNS API | TCP |
| 11434 | Ollama | TCP |
| 51820 | WireGuard | UDP |

## Gematria (DO NYC3)
| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 80 | Caddy | TCP |
| 443 | Caddy (151 domains) | TCP |
| 53 | PowerDNS (ns1) | UDP/TCP |
| 11434 | Ollama | TCP |
| 51820 | WireGuard | UDP |

## Anastasia (DO NYC1)
| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 80 | Docker services | TCP |
| 443 | Docker services | TCP |
| 51820 | WireGuard | UDP |
