"""Trinary logic — three-valued logic system (-1, 0, 1)."""
from __future__ import annotations
from enum import IntEnum

class Trit(IntEnum):
    NEG = -1   # false / cancel / already-answered
    ZERO = 0   # unknown / waiting / maybe
    POS = 1    # true / arrived / confirmed

def trit_and(a: Trit, b: Trit) -> Trit:
    return Trit(min(a, b))

def trit_or(a: Trit, b: Trit) -> Trit:
    return Trit(max(a, b))

def trit_not(a: Trit) -> Trit:
    return Trit(-a)

def trit_consensus(values: list[Trit]) -> Trit:
    if not values:
        return Trit.ZERO
    pos = sum(1 for v in values if v == Trit.POS)
    neg = sum(1 for v in values if v == Trit.NEG)
    if pos > neg:
        return Trit.POS
    elif neg > pos:
        return Trit.NEG
    return Trit.ZERO

class TrinaryRegister:
    def __init__(self, width: int = 8):
        self.width = width
        self.trits = [Trit.ZERO] * width

    def set(self, index: int, value: Trit) -> None:
        if 0 <= index < self.width:
            self.trits[index] = value

    def get(self, index: int) -> Trit:
        return self.trits[index] if 0 <= index < self.width else Trit.ZERO

    def to_decimal(self) -> int:
        result = 0
        for i, t in enumerate(reversed(self.trits)):
            result += int(t) * (3 ** i)
        return result

    def __repr__(self) -> str:
        symbols = {Trit.NEG: "-", Trit.ZERO: "0", Trit.POS: "+"}
        return "".join(symbols[t] for t in self.trits)
