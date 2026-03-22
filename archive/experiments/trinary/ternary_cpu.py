"""Ternary CPU simulator — 3-valued instruction set."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class TernaryCPU:
    registers: dict[str, int] = field(default_factory=lambda: {f"r{i}": 0 for i in range(8)})
    memory: list[int] = field(default_factory=lambda: [0] * 256)
    pc: int = 0
    halted: bool = False
    cycles: int = 0

    OPCODES = {
        0: "NOP", 1: "LOAD", 2: "STORE", 3: "ADD", 4: "SUB",
        5: "MUL", 6: "AND3", 7: "OR3", 8: "NOT3",
        9: "JMP", 10: "JZ", 11: "JNZ", 12: "HALT",
    }

    def execute(self, opcode: int, operands: list[int]) -> None:
        self.cycles += 1
        if opcode == 0:    pass  # NOP
        elif opcode == 1:  self.registers[f"r{operands[0]}"] = operands[1]  # LOAD imm
        elif opcode == 2:  self.memory[operands[1]] = self.registers[f"r{operands[0]}"]  # STORE
        elif opcode == 3:  # ADD (ternary balanced)
            a = self.registers[f"r{operands[0]}"]
            b = self.registers[f"r{operands[1]}"]
            self.registers[f"r{operands[0]}"] = max(-1, min(1, a + b))
        elif opcode == 4:  # SUB
            a = self.registers[f"r{operands[0]}"]
            b = self.registers[f"r{operands[1]}"]
            self.registers[f"r{operands[0]}"] = max(-1, min(1, a - b))
        elif opcode == 5:  # MUL
            a = self.registers[f"r{operands[0]}"]
            b = self.registers[f"r{operands[1]}"]
            self.registers[f"r{operands[0]}"] = max(-1, min(1, a * b))
        elif opcode == 8:  # NOT3 (ternary negation)
            self.registers[f"r{operands[0]}"] = -self.registers[f"r{operands[0]}"]
        elif opcode == 9:  self.pc = operands[0] - 1  # JMP
        elif opcode == 12: self.halted = True  # HALT

    def run(self, program: list[tuple[int, list[int]]], max_cycles: int = 1000) -> dict:
        self.pc = 0
        self.halted = False
        while not self.halted and self.pc < len(program) and self.cycles < max_cycles:
            opcode, operands = program[self.pc]
            self.execute(opcode, operands)
            self.pc += 1
        return {"cycles": self.cycles, "registers": dict(self.registers), "halted": self.halted}
