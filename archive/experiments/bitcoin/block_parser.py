"""Bitcoin block parser — for RoadChain research."""
from __future__ import annotations
import hashlib
import struct
from dataclasses import dataclass

@dataclass
class BlockHeader:
    version: int
    prev_hash: str
    merkle_root: str
    timestamp: int
    bits: int
    nonce: int

    @property
    def hash(self) -> str:
        header_bytes = (
            struct.pack("<I", self.version)
            + bytes.fromhex(self.prev_hash)[::-1]
            + bytes.fromhex(self.merkle_root)[::-1]
            + struct.pack("<III", self.timestamp, self.bits, self.nonce)
        )
        return hashlib.sha256(hashlib.sha256(header_bytes).digest()).digest()[::-1].hex()

@dataclass
class Transaction:
    txid: str
    inputs: list[dict]
    outputs: list[dict]
    value_sat: int

class BlockParser:
    def __init__(self):
        self.blocks: list[BlockHeader] = []

    def parse_header(self, raw: bytes) -> BlockHeader:
        version = struct.unpack("<I", raw[0:4])[0]
        prev_hash = raw[4:36][::-1].hex()
        merkle_root = raw[36:68][::-1].hex()
        timestamp = struct.unpack("<I", raw[68:72])[0]
        bits = struct.unpack("<I", raw[72:76])[0]
        nonce = struct.unpack("<I", raw[76:80])[0]
        header = BlockHeader(version, prev_hash, merkle_root, timestamp, bits, nonce)
        self.blocks.append(header)
        return header

    def genesis_block(self) -> BlockHeader:
        return BlockHeader(
            version=1,
            prev_hash="0" * 64,
            merkle_root="4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
            timestamp=1231006505,
            bits=0x1d00ffff,
            nonce=2083236893,
        )
