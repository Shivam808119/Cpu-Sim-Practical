"""
verify.py - checks every program against the numbers printed in the lab
manual (memory maps, register traces, sample runs) and against plain Python
arithmetic. Run:  python3 tools/verify.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from basic_computer import assemble, run, fetch_micro_trace, signed

P = os.path.join(os.path.dirname(__file__), "..", "programs")
f = lambda n: os.path.join(P, n)
bad = []


def check(label, got, want):
    if got != want:
        bad.append(label)
        print("FAIL", label, "\n   got ", got, "\n   want", want)
    else:
        print("ok  ", label)


# ---------- memory maps (hex words) ----------
maps = {
    "P03_ADD.a": "F800 3007 F800 1007 3008 F400 7001 0000 0000",
    "P04_SUBTRACT.a": "F800 3009 F800 7200 7020 1009 300A F400 7001 0000 0000",
    "P06_MEMORY_REFERENCE.a": "2009 1007 3009 6008 4000 2009 7001 0005 FFFD 0000",
    "P07_REGISTER_REF_CLA_CMA_CME_HLT.a": "2005 7800 7200 7100 7001 0019",
    "P08_REGISTER_REF_INC_SPA_SNA_SZE.a": "200B 7020 7008 7001 7020 7010 7001 7002 7001 7020 7001 FFFE",
    "P09_REGISTER_REF_CIR_CIL.a": "2006 7080 7080 7040 7040 7001 0009",
    "P10_SUM_UNTIL_NEGATIVE.a": "F800 7010 4006 1009 3009 4000 2009 F400 7001 0000",
    "P11_SUM_UNTIL_ZERO.a": "F800 7004 4004 4007 100A 300A 4000 200A F400 7001 0000",
}
for name, want in maps.items():
    mem, _ = assemble(f(name))
    check("memory map " + name, " ".join("%04X" % w for w in mem), want)

mem, listing = assemble(f("P05_LOGIC.a"))
check("P05 length", len(mem), 44)
check("P05 first words", " ".join("%04X" % w for w in mem[:8]),
      "F800 3023 F800 3024 2023 0024 3027 F400")
addr = {lab: a for a, lab, _, _ in listing if lab}
check("P05 data addresses", [addr[k] for k in ("A", "B", "NA", "NB", "RAND", "ROR", "RXOR", "RNOR", "RNAND")],
      [0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B])

# ---------- Practical 2: fetch micro-steps ----------
got = [(r[2], r[3], r[4]) for r in fetch_micro_trace(f("P03_ADD.a"))]
check("P02 fetch AR/PC/IR", got,
      [(0, 0, 0), (0, 0, 0), (0, 0, 63488), (0, 1, 63488), (2048, 1, 63488), (2048, 1, 63488)])

# ---------- register traces from the manual ----------
# (pc_before, mnemonic, IR hex, AC, E, PC, AR, IR dec)  [P6 also has DR]
exp6 = [
    (0, "LDA PROD", "2009", 0, 0, 0, 1, 9, 8201), (1, "ADD X", "1007", 5, 5, 0, 2, 7, 4103),
    (2, "STA PROD", "3009", 5, 5, 0, 3, 9, 12297), (3, "ISZ CTR", "6008", 5, 65534, 0, 4, 8, 24584),
    (4, "BUN LOOP", "4000", 5, 65534, 0, 0, 0, 16384), (0, "LDA PROD", "2009", 5, 5, 0, 1, 9, 8201),
    (1, "ADD X", "1007", 10, 5, 0, 2, 7, 4103), (2, "STA PROD", "3009", 10, 5, 0, 3, 9, 12297),
    (3, "ISZ CTR", "6008", 10, 65535, 0, 4, 8, 24584), (4, "BUN LOOP", "4000", 10, 65535, 0, 0, 0, 16384),
    (0, "LDA PROD", "2009", 10, 10, 0, 1, 9, 8201), (1, "ADD X", "1007", 15, 5, 0, 2, 7, 4103),
    (2, "STA PROD", "3009", 15, 5, 0, 3, 9, 12297), (3, "ISZ CTR", "6008", 15, 0, 0, 5, 8, 24584),
    (5, "LDA PROD", "2009", 15, 15, 0, 6, 9, 8201), (6, "HLT", "7001", 15, 15, 0, 7, 1, 28673),
]
m, tr = run(f("P06_MEMORY_REFERENCE.a"))
check("P06 trace", [(t["pc_before"], t["instr"], "%04X" % t["ir"], t["ac"], t["dr"], t["e"], t["pc"], t["ar"], t["ir"]) for t in tr], exp6)
check("P06 PROD in memory", m.M[9], 15)
check("P06 CTR in memory", m.M[8], 0)

# (pc_before, mnemonic, IR hex, AC, E, PC, AR, IR dec)
exp7 = [
    (0, "LDA NUM", "2005", 25, 0, 1, 5, 8197), (1, "CLA", "7800", 0, 0, 2, 2048, 30720),
    (2, "CMA", "7200", 65535, 0, 3, 512, 29184), (3, "CME", "7100", 65535, 1, 4, 256, 28928),
    (4, "HLT", "7001", 65535, 1, 5, 1, 28673),
]
exp8 = [
    (0, "LDA NUM", "200B", 65534, 0, 1, 11, 8203), (1, "INC", "7020", 65535, 0, 2, 32, 28704),
    (2, "SNA", "7008", 65535, 0, 4, 8, 28680), (4, "INC", "7020", 0, 0, 5, 32, 28704),
    (5, "SPA", "7010", 0, 0, 7, 16, 28688), (7, "SZE", "7002", 0, 0, 9, 2, 28674),
    (9, "INC", "7020", 1, 0, 10, 32, 28704), (10, "HLT", "7001", 1, 0, 11, 1, 28673),
]
exp9 = [
    (0, "LDA NUM", "2006", 9, 0, 1, 6, 8198), (1, "CIR", "7080", 4, 1, 2, 128, 28800),
    (2, "CIR", "7080", 32770, 0, 3, 128, 28800), (3, "CIL", "7040", 4, 1, 4, 64, 28736),
    (4, "CIL", "7040", 9, 0, 5, 64, 28736), (5, "HLT", "7001", 9, 0, 6, 1, 28673),
]
for tag, name, exp in (("P07", "P07_REGISTER_REF_CLA_CMA_CME_HLT.a", exp7),
                       ("P08", "P08_REGISTER_REF_INC_SPA_SNA_SZE.a", exp8),
                       ("P09", "P09_REGISTER_REF_CIR_CIL.a", exp9)):
    m, tr = run(f(name))
    check(tag + " trace", [(t["pc_before"], t["instr"], "%04X" % t["ir"], t["ac"], t["e"], t["pc"], t["ar"], t["ir"]) for t in tr], exp)

# ---------- sample runs from the manual ----------
runs = {
    "P03_ADD.a": [((25, 17), [42]), ((-40, 15), [-25]), ((-1, 1), [0]), ((30000, 10000), [-25536])],
    "P04_SUBTRACT.a": [((50, 18), [32]), ((18, 50), [-32]), ((-7, -7), [0]), ((0, 1), [-1])],
    "P05_LOGIC.a": [((12, 10), [8, 14, -13, -11, 6, -15, -9]),
                    ((5, 3), [1, 7, -6, -4, 6, -8, -2]),
                    ((255, 15), [15, 255, -256, -16, 240, -256, -16])],
    "P10_SUM_UNTIL_NEGATIVE.a": [((4, 10, 0, 6, -3), [20]), ((-5,), [0]), ((7, 8, -1), [15])],
    "P11_SUM_UNTIL_ZERO.a": [((8, 12, -5, 0), [15]), ((0,), [0]), ((100, 200, 300, 0), [600])],
}
for name, cases in runs.items():
    for ins, want in cases:
        m, _ = run(f(name), ins)
        check("%s %s" % (name, list(ins)), m.output, want)

# ---------- independent arithmetic cross-checks ----------
import random
random.seed(1)
for _ in range(300):
    a, b = random.randint(-32768, 32767), random.randint(-32768, 32767)
    s = lambda v: signed(v & 0xFFFF)
    check_ok = (run(f("P03_ADD.a"), (a, b))[0].output == [s(a + b)]
                and run(f("P04_SUBTRACT.a"), (a, b))[0].output == [s(a - b)])
    A, B = a & 0xFFFF, b & 0xFFFF
    want = [s(A & B), s(A | B), s(~A), s(~B), s(A ^ B), s(~(A | B)), s(~(A & B))]
    check_ok = check_ok and run(f("P05_LOGIC.a"), (a, b))[0].output == want
    if not check_ok:
        bad.append("random %d %d" % (a, b)); print("FAIL random", a, b)
print("ok   300 random pairs for ADD / SUB / six logic ops")

for _ in range(100):
    xs = [random.randint(0, 3000) for _ in range(random.randint(0, 8))]
    got = run(f("P10_SUM_UNTIL_NEGATIVE.a"), xs + [-1])[0].output
    got0 = run(f("P11_SUM_UNTIL_ZERO.a"), [x for x in xs if x] + [0])[0].output
    if got != [sum(xs)] or got0 != [sum(x for x in xs if x)]:
        bad.append("sum loop"); print("FAIL sum loop", xs)
print("ok   100 random lists for the two sum loops")

# ---------- exact final values quoted in the README ----------
m, _ = run(f("P03_ADD.a"), (25, 17))
check("P03 final regs", (m.AC, m.DR, m.PC, m.IR, m.E, m.M[7], m.M[8]), (42, 25, 7, 28673, 0, 0x19, 0x2A))
m, _ = run(f("P03_ADD.a"), (-1, 1))
check("P03 -1+1 carry E", (m.AC, m.E), (0, 1))
m, _ = run(f("P04_SUBTRACT.a"), (18, 50))
check("P04 final regs", (m.AC, m.DR, m.PC, m.E, m.M[10]), (0xFFE0, 18, 9, 0, 0xFFE0))
m, _ = run(f("P05_LOGIC.a"), (12, 10))
check("P05 stored results", [m.M[a] for a in (0x27, 0x28, 0x29, 0x2A, 0x2B)],
      [0x0008, 0x000E, 0x0006, 0xFFF1, 0xFFF7])
m, _ = run(f("P10_SUM_UNTIL_NEGATIVE.a"), (4, 10, 0, 6, -3))
check("P10 SUM word", m.M[9], 0x14)
m, tr = run(f("P10_SUM_UNTIL_NEGATIVE.a"), (4, 10, 0, 6, -3))
check("P10 INP executed 5 times", sum(1 for t in tr if t["name"] == "INP"), 5)
m, _ = run(f("P11_SUM_UNTIL_ZERO.a"), (8, 12, -5, 0))
check("P11 final regs", (m.AC, m.DR, m.E, m.M[10]), (15, 15, 1, 15))

print()
print("ALL CHECKS PASSED" if not bad else "FAILED: %d" % len(bad))
sys.exit(1 if bad else 0)
