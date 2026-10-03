"""
basic_computer.py - tiny model of the CPU Sim "BasicComputer" machine
(Mano's Basic Computer, 16-bit words, 4096-word RAM).

It mirrors the machine built in Practicals 1-2:
  fetch  : PC->AR, M[AR]->IR, PC+1->PC, IR(0-11)->AR, decode-IR
  execute: the micro-sequences listed in the README (Table of instructions)

Used only to check the programs and to generate the trace tables in the
README. It is not a replacement for running CPU Sim itself.
"""
import re

MASK = 0xFFFF
MREF = {"AND": 0x0, "ADD": 0x1, "LDA": 0x2, "STA": 0x3, "BUN": 0x4, "ISZ": 0x6}
RREF = {
    "CLA": 0x7800, "CLE": 0x7400, "CMA": 0x7200, "CME": 0x7100,
    "CIR": 0x7080, "CIL": 0x7040, "INC": 0x7020, "SPA": 0x7010,
    "SNA": 0x7008, "SZA": 0x7004, "SZE": 0x7002, "HLT": 0x7001,
    "INP": 0xF800, "OUT": 0xF400,
}


def signed(v):
    return v - 0x10000 if v & 0x8000 else v


def assemble(path_or_text):
    """Return (memory list, listing). listing rows: addr, label, text, word."""
    try:
        with open(path_or_text) as f:
            text = f.read()
    except (FileNotFoundError, OSError):
        text = path_or_text
    stmts = []
    for raw in text.splitlines():
        line = raw.split(";", 1)[0].rstrip()
        if not line.strip():
            continue
        label = None
        m = re.match(r"^\s*([A-Za-z_]\w*):\s*(.*)$", line)
        if m:
            label, line = m.group(1), m.group(2)
        stmts.append((label, line.split()))
    labels = {}
    for addr, (label, _) in enumerate(stmts):
        if label:
            labels[label] = addr
    mem, listing = [], []
    for addr, (label, toks) in enumerate(stmts):
        op = toks[0]
        if op == ".data":
            assert toks[1] == "1", "only '.data 1 n' is used"
            word = int(toks[2], 0) & MASK
            shown = ".data 1 " + toks[2]
        elif op in MREF:
            word = (MREF[op] << 12) | labels[toks[1]]
            shown = op + " " + toks[1]
        elif op in RREF:
            word = RREF[op]
            shown = op
        else:
            raise ValueError("unknown instruction %r" % op)
        mem.append(word)
        listing.append((addr, label or "", shown, word))
    return mem, listing


class Machine:
    def __init__(self, mem, inputs=()):
        self.M = list(mem) + [0] * (4096 - len(mem))
        self.AC = self.DR = self.IR = 0
        self.AR = self.PC = 0
        self.E = self.S = 0
        self.inputs = list(inputs)
        self.output = []

    # one complete machine instruction (fetch + execute)
    def step(self):
        # --- fetch sequence ---
        self.AR = self.PC                       # PC->AR
        self.IR = self.M[self.AR]               # M[AR]->IR
        self.PC = (self.PC + 1) & 0xFFF         # PC+1->PC
        self.AR = self.IR & 0xFFF               # IR(0-11)->AR
        # --- decode ---
        top = self.IR >> 12
        if top in MREF.values():
            name = [k for k, v in MREF.items() if v == top][0]
        else:
            name = [k for k, v in RREF.items() if v == self.IR][0]
        # --- execute ---
        if name == "AND":
            self.DR = self.M[self.AR]; self.AC &= self.DR
        elif name == "ADD":
            self.DR = self.M[self.AR]
            s = self.AC + self.DR
            self.E = 1 if s > MASK else 0
            self.AC = s & MASK
        elif name == "LDA":
            self.DR = self.M[self.AR]; self.AC = self.DR
        elif name == "STA":
            self.M[self.AR] = self.AC
        elif name == "BUN":
            self.PC = self.AR
        elif name == "ISZ":
            self.DR = (self.M[self.AR] + 1) & MASK
            self.M[self.AR] = self.DR
            if self.DR == 0:
                self.PC = (self.PC + 1) & 0xFFF
        elif name == "CLA":
            self.AC = 0
        elif name == "CLE":
            self.E = 0
        elif name == "CMA":
            self.AC ^= MASK
        elif name == "CME":
            self.E ^= 1
        elif name == "CIR":
            tmp = self.AC & 1
            self.AC = (self.AC >> 1) | (self.E << 15)
            self.E = tmp
        elif name == "CIL":
            tmp = (self.AC >> 15) & 1
            self.AC = ((self.AC << 1) & MASK) | self.E
            self.E = tmp
        elif name == "INC":
            self.AC = (self.AC + 1) & MASK
        elif name == "SPA":
            if not (self.AC >> 15) & 1: self.PC = (self.PC + 1) & 0xFFF
        elif name == "SNA":
            if (self.AC >> 15) & 1: self.PC = (self.PC + 1) & 0xFFF
        elif name == "SZA":
            if self.AC == 0: self.PC = (self.PC + 1) & 0xFFF
        elif name == "SZE":
            if self.E == 0: self.PC = (self.PC + 1) & 0xFFF
        elif name == "HLT":
            self.S = 1
        elif name == "INP":
            self.AC = int(self.inputs.pop(0)) & MASK
        elif name == "OUT":
            self.output.append(signed(self.AC))
        return name


def run(path, inputs=(), limit=10000):
    """Run to HLT. Returns (machine, trace); trace has one dict per instruction."""
    mem, listing = assemble(path)
    m = Machine(mem, inputs)
    trace = []
    text = {a: t for a, _, t, _ in listing}
    n = 0
    while not m.S:
        n += 1
        assert n <= limit, "program did not halt"
        pc_before = m.PC
        name = m.step()
        trace.append(dict(
            step=n, pc_before=pc_before, instr=text[pc_before], name=name,
            ir=m.IR, ac=m.AC, dr=m.DR, e=m.E, pc=m.PC, ar=m.AR))
    return m, trace


def fetch_micro_trace(path):
    """The five micro-steps of the first fetch (Practical 2)."""
    mem, _ = assemble(path)
    M = mem + [0] * (4096 - len(mem))
    pc = ar = ir = 0
    rows = [("start", "-", ar, pc, ir)]
    ar = pc;               rows.append((1, "PC->AR", ar, pc, ir))
    ir = M[ar];            rows.append((2, "M[AR]->IR", ar, pc, ir))
    pc = (pc + 1) & 0xFFF; rows.append((3, "PC+1->PC", ar, pc, ir))
    ar = ir & 0xFFF;       rows.append((4, "IR(0-11)->AR", ar, pc, ir))
    rows.append((5, "decode-IR", ar, pc, ir))
    return rows
