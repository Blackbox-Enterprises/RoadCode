"""PowerDNS record management for 20 BlackRoad domains."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DNSRecord:
    domain: str
    name: str
    record_type: str
    content: str
    ttl: int = 300

DOMAINS = [
    "blackroad.company", "blackroad.io", "blackroad.me", "blackroad.network",
    "blackroad.systems", "blackroadai.com", "blackroadinc.us", "blackroadqi.com",
    "blackroadquantum.com", "blackroadquantum.info", "blackroadquantum.net",
    "blackroadquantum.shop", "blackroadquantum.store", "lucidia.earth",
    "lucidia.studio", "lucidiaqi.com", "roadchain.io", "roadcoin.io",
    "blackboxprogramming.io",
]

SUBDOMAINS = [
    "chat", "search", "pay", "tutor", "social", "canvas", "cadence",
    "roadcode", "video", "live", "game", "book", "work", "radio",
    "auth", "api", "hq", "roundtrip", "images", "app",
]

class DNSManager:
    def __init__(self, api_url: str = "http://192.168.4.38:8081"):
        self.api_url = api_url
        self.records: list[DNSRecord] = []

    def generate_records(self, gateway_ip: str = "192.168.4.49") -> list[DNSRecord]:
        records = []
        for domain in DOMAINS:
            records.append(DNSRecord(domain, "@", "A", gateway_ip))
            records.append(DNSRecord(domain, "www", "CNAME", domain))
        for sub in SUBDOMAINS:
            records.append(DNSRecord("blackroad.io", sub, "CNAME", "blackroad.io"))
        self.records = records
        return records

    def add_record(self, domain: str, name: str, rtype: str, content: str) -> DNSRecord:
        record = DNSRecord(domain, name, rtype, content)
        self.records.append(record)
        return record

    def find(self, domain: str, name: str = "@") -> list[DNSRecord]:
        return [r for r in self.records if r.domain == domain and r.name == name]

    def to_zone_file(self, domain: str) -> str:
        lines = [f"; Zone file for {domain}", f"$ORIGIN {domain}.", f"$TTL 300", ""]
        for r in self.records:
            if r.domain == domain:
                lines.append(f"{r.name}\t{r.ttl}\tIN\t{r.record_type}\t{r.content}")
        return "\n".join(lines)

    def stats(self) -> dict:
        return {"domains": len(DOMAINS), "subdomains": len(SUBDOMAINS),
                "total_records": len(self.records),
                "by_type": {t: sum(1 for r in self.records if r.record_type == t)
                            for t in set(r.record_type for r in self.records) if self.records}}
