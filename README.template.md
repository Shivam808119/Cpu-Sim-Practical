# Computer System Architecture – CPU Sim Practicals

**Simulating Mano's Basic Computer in CPU Sim 4.0.11**

| | |
| :--- | :--- |
| Name | |
| Roll No. | |
| Course / Semester | Computer System Architecture (DSC02 / DSC03 / GE2c) |
| College | Ramanujan College, University of Delhi |
| Tool | CPU Sim 4.0.11 (needs Java 8 **with JavaFX**) |

## Contents

| No. | Practical | Program file |
| :--- | :--- | :--- |
| 1 | [Create a machine based on the Basic Computer](#practical-1-create-a-machine-basic-computer-architecture) | `BasicComputer.cpu` |
| 2 | [Create the fetch routine of the instruction cycle](#practical-2-create-the-fetch-routine-of-the-instruction-cycle) | `programs/P03_ADD.a` (test) |
| 3 | [ADD two user-entered numbers](#practical-3-add-operation-on-two-user-entered-numbers) | `programs/P03_ADD.a` |
| 4 | [SUBTRACT two user-entered numbers](#practical-4-subtract-operation-on-two-user-entered-numbers) | `programs/P04_SUBTRACT.a` |
| 5 | [AND, OR, NOT, XOR, NOR, NAND](#practical-5-logical-operations-and-or-not-xor-nor-nand) | `programs/P05_LOGIC.a` |
| 6 | [Memory-reference instructions ADD, LDA, STA, BUN, ISZ](#practical-6-memory-reference-instructions-add-lda-sta-bun-isz) | `programs/P06_MEMORY_REFERENCE.a` |
| 7 | [Register-reference: CLA, CMA, CME, HLT](#practical-7-register-reference-instructions-cla-cma-cme-hlt) | `programs/P07_REGISTER_REF_CLA_CMA_CME_HLT.a` |
| 8 | [Register-reference: INC, SPA, SNA, SZE](#practical-8-register-reference-instructions-inc-spa-sna-sze) | `programs/P08_REGISTER_REF_INC_SPA_SNA_SZE.a` |
| 9 | [Register-reference: CIR, CIL](#practical-9-register-reference-instructions-cir-cil) | `programs/P09_REGISTER_REF_CIR_CIL.a` |
| 10 | [Sum of integers until a negative number](#practical-10-sum-of-integers-until-a-negative-number-is-read) | `programs/P10_SUM_UNTIL_NEGATIVE.a` |
| 11 | [Sum of integers until zero](#practical-11-sum-of-integers-until-zero-is-read) | `programs/P11_SUM_UNTIL_ZERO.a` |

## How this repository is organised

```
BasicComputer.cpu        machine built in Practicals 1 and 2 (saved from CPU Sim)
programs/                assembly programs for Practicals 3 to 11
screenshots/             screenshots used in this README (see SCREENSHOTS.md)
tools/                   Python model used to double-check every result
```

**To run any program:** start CPU Sim → *File → Open machine…* → `BasicComputer.cpu` → *File → Open text…* → the `.a` file → press **Ctrl+2** (assemble and load) → **Ctrl+R** (run). When the console turns yellow it is waiting at an `INP`: type a number and press Enter. For the register-trace practicals press **Ctrl+D** (debug mode) instead of Ctrl+R, set the Registers *Data* box to **Unsigned Dec** and click **Step by Instr**.

**How the results were checked:** `tools/verify.py` models the machine (same fetch sequence and execute sequences as the tables below) and replays every program. All memory maps, register traces and sample runs printed in this README come from that model, and the logic and arithmetic programs were also compared with ordinary Python arithmetic on random inputs. Run `python3 tools/verify.py` to repeat the check.

---

# Practical 1: Create a Machine (Basic Computer Architecture)

**Aim:** To create, in CPU Sim, a machine based on Mano's Basic Computer: its registers, condition bits, memory, microinstructions, instruction fields and machine instructions.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

CPU Sim describes a computer at the register-transfer level. Four kinds of object make up a machine:

| Object | What it is | Where to edit it |
| :--- | :--- | :--- |
| Hardware modules | Registers, condition bits (single bits that can record a carry or halt the machine) and RAM | Modify → Hardware Modules (Ctrl+K) |
| Microinstructions | One elementary register transfer, such as `PC->AR`, `M[AR]->DR`, a test-and-skip or a decode | Modify → Microinstructions (Ctrl+Shift+M) |
| Fetch sequence | Microinstructions that run before every instruction (built in Practical 2) | Modify → Fetch Sequence (Ctrl+Y) |
| Machine instructions | A name, an opcode, a format made of fields, and an *execute sequence* of microinstructions ending in `End` | Modify → Machine Instructions (Ctrl+M) |

Because every instruction is carried out by a stored list of microinstructions, this is a **microprogrammed** control unit.

The Basic Computer is a 16-bit, single-accumulator machine with 4096 words of memory. Its instruction word is laid out as:

```
 15   14 13 12   11 ........................ 0
+---+----------+------------------------------+
| I |  opcode  |           address            |
+---+----------+------------------------------+
Memory-reference : opcode 000-110         (hex 0xxx to 6xxx when I = 0)
Register-reference: opcode 111, I = 0     (hex 7xxx)
Input-output     : opcode 111, I = 1      (hex Fxxx)
```

> **Bit numbering.** CPU Sim counts bits from the **left**: its bit 0 is the most significant bit, which Mano calls bit 15. So Mano's `IR(0-11)` is CPU Sim's `IR` start bit **4**, 12 bits, and Mano's `AC(0)` (the least significant bit) is CPU Sim's `AC` bit **15**. Check *Execute → Options…* that bits are indexed from the left (the default).

How this CPU Sim machine differs from the textbook design: only direct addressing is used (the I bit is always 0), `INP`/`OUT` move a whole signed integer between the console and AC instead of one character through INPR/OUTR, `HLT` *sets* the halt bit S to 1 (CPU Sim stops when a halt bit becomes 1), and interrupt hardware is left out because no practical needs it.

## Procedure

### Step 1 – Start a new machine

*File → New machine* (Ctrl+Shift+N) creates a machine with no hardware.

![Fig 1.1 – File menu: New machine](screenshots/p01_new_machine.png)

### Step 2 – Create the registers

Open *Modify → Hardware Modules* (Ctrl+K), keep *Type of Module* = **Register**, click **New** for each row and type the name and width (initial value 0).

| Register | Width | Role |
| :--- | :--- | :--- |
| AC | 16 | Accumulator |
| DR | 16 | Data register (memory operand) |
| AR | 12 | Address register |
| PC | 12 | Program counter |
| IR | 16 | Instruction register |
| E | 1 | Extended bit: carry out of the adder, rotated by CIR/CIL |
| TMP | 1 | Scratch bit used only inside CIR and CIL |
| S | 1 | Start/stop flip-flop, set by HLT |

![Fig 1.2 – Hardware Modules: the eight registers](screenshots/p01_registers.png)

### Step 3 – Create the condition bits and the RAM

Switch *Type of Module* to **ConditionBit** and add two bits. Tick **halt** only for `halt-S`: when a microinstruction sets that bit the machine stops.

| Condition bit | Register | Bit | Halt |
| :--- | :--- | :--- | :--- |
| carry-E | E | 0 | no |
| halt-S | S | 0 | yes |

![Fig 1.3 – Condition bits carry-E and halt-S](screenshots/p01_condition_bits.png)

Switch to **RAM** and add one module: name `M`, length `4096`, cell size `16`. A 16-bit cell makes the memory word-addressed, like the 4096 × 16 memory of the textbook design. Click **OK**.

![Fig 1.4 – RAM M: 4096 cells of 16 bits](screenshots/p01_ram.png)

### Step 4 – Create the microinstructions

Open *Modify → Microinstructions* (Ctrl+Shift+M). Pick each type in **Type of Microinstruction**, click **New** per row and fill the columns as below. The names are only labels, but the execute sequences in Step 6 must use the same names.

**TransferRtoR** – copy bits from one register to another

| name | source | srcStartBit | dest | destStartBit | numBits |
| :--- | :--- | :--- | :--- | :--- | :--- |
| PC->AR | PC | 0 | AR | 0 | 12 |
| IR(0-11)->AR | IR | 4 | AR | 0 | 12 |
| AR->PC | AR | 0 | PC | 0 | 12 |
| DR->AC | DR | 0 | AC | 0 | 16 |
| AC(0)->TMP | AC | 15 | TMP | 0 | 1 |
| AC(15)->TMP | AC | 0 | TMP | 0 | 1 |
| E->AC(15) | E | 0 | AC | 0 | 1 |
| E->AC(0) | E | 0 | AC | 15 | 1 |
| TMP->E | TMP | 0 | E | 0 | 1 |

> `IR(0-11)->AR` must keep **srcStartBit = 4** and **destStartBit = 0**. Starting at bit 0 would copy the opcode bits into AR and every memory-reference instruction would address the wrong word.

![Fig 1.5 – TransferRtoR microinstructions](screenshots/p01_micro_transferrtor.png)

**MemoryAccess** – read a memory word into a register, or write a register to memory

| name | direction | memory | data | address |
| :--- | :--- | :--- | :--- | :--- |
| M[AR]->IR | read | M | IR | AR |
| M[AR]->DR | read | M | DR | AR |
| AC->M[AR] | write | M | AC | AR |
| DR->M[AR] | write | M | DR | AR |

![Fig 1.6 – MemoryAccess microinstructions](screenshots/p01_micro_memoryaccess.png)

**Increment** – add a constant to a register

| name | register | delta |
| :--- | :--- | :--- |
| PC+1->PC | PC | 1 |
| DR+1->DR | DR | 1 |
| AC+1->AC | AC | 1 |

![Fig 1.7 – Increment microinstructions](screenshots/p01_micro_increment.png)

**Arithmetic** – add two registers; the carry goes to E

| name | type | source1 | source2 | destination | carryBit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| AC+DR->AC,E | ADD | AC | DR | AC | carry-E |

![Fig 1.8 – Arithmetic microinstruction](screenshots/p01_micro_arithmetic.png)

**Logical** – bitwise AND and NOT

| name | type | source1 | source2 | destination |
| :--- | :--- | :--- | :--- | :--- |
| AC^DR->AC | AND | AC | DR | AC |
| AC'->AC | NOT | AC | AC | AC |
| E'->E | NOT | E | E | E |

![Fig 1.9 – Logical microinstructions](screenshots/p01_micro_logical.png)

**Shift** – move AC by one bit (used inside CIR and CIL)

| name | source | destination | type | direction | distance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| shr AC | AC | AC | logical | right | 1 |
| shl AC | AC | AC | logical | left | 1 |

![Fig 1.10 – Shift microinstructions](screenshots/p01_micro_shift.png)

**Set** – load a constant into bits of a register (clears AC or E)

| name | register | start | numBits | value |
| :--- | :--- | :--- | :--- | :--- |
| 0->AC | AC | 0 | 16 | 0 |
| 0->E | E | 0 | 1 | 0 |

![Fig 1.11 – Set microinstructions](screenshots/p01_micro_set.png)

**Test** – compare bits of a register with a value and omit the next *n* microinstructions when the comparison is true. This is how the skip instructions are built.

| name | register | start | numBits | comparison | value | omission |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| if(DR!=0)skip-1 | DR | 0 | 16 | NE | 0 | 1 |
| if(AC(15)!=0)skip-1 | AC | 0 | 1 | NE | 0 | 1 |
| if(AC(15)==0)skip-1 | AC | 0 | 1 | EQ | 0 | 1 |
| if(AC!=0)skip-1 | AC | 0 | 16 | NE | 0 | 1 |
| if(E!=0)skip-1 | E | 0 | 1 | NE | 0 | 1 |

(For the `AC(15)` tests the *start* is 0 because Mano's AC(15), the sign bit, is CPU Sim's bit 0.)

![Fig 1.12 – Test microinstructions](screenshots/p01_micro_test.png)

**Decode** – pick the machine instruction whose opcode matches IR

| name | ir |
| :--- | :--- |
| decode-IR | IR |

![Fig 1.13 – Decode microinstruction](screenshots/p01_micro_decode.png)

**SetCondBit** – set the halt bit

| name | bit | value |
| :--- | :--- | :--- |
| 1->S(halt) | halt-S | 1 |

![Fig 1.14 – SetCondBit microinstruction](screenshots/p01_micro_setcondbit.png)

**IO** – read an integer from, or print an integer to, the console

| name | direction | type | buffer | connection |
| :--- | :--- | :--- | :--- | :--- |
| input-int->AC | input | integer | AC | [Console] |
| output-AC->int | output | integer | AC | [Console] |

![Fig 1.15 – IO microinstructions](screenshots/p01_micro_io.png)

That makes **33 microinstructions**. Click **OK**. An `End` microinstruction exists in every machine automatically; it finishes an execute sequence and returns control to the fetch sequence.

### Step 5 – Create the instruction fields

*Modify → Machine Instructions* (Ctrl+M) → **Edit Fields…** → **New** three times (all *required*, *absolute*, unsigned, default 0):

| Field | Bits | Used for |
| :--- | :--- | :--- |
| op | 4 | opcode digit of memory-reference instructions (0 to 6) |
| addr | 12 | address part of memory-reference instructions |
| opcode | 16 | the complete 16-bit code of register-reference and I/O instructions |

![Fig 1.16 – Edit Fields dialog](screenshots/p01_fields.png)

> **Why two opcode lengths work.** The decoder compares the leftmost 1 bit of IR, then 2 bits, then 3 and so on, and picks the first instruction whose opcode matches. No instruction has the 4-bit opcode 7 or F, so an IR such as `7800` keeps being examined until all 16 bits match `CLA`.

### Step 6 – Create the 20 machine instructions

For each instruction click **new**, type the name, then on the **Format** tab enter the opcode and drag the fields into the format bar (`op` then `addr`, or just `opcode`). On the **Implementation** tab drag the microinstructions into *Execute sequence* in the order shown, ending with `End`.

| Name | Opcode | Format | Execute sequence |
| :--- | :--- | :--- | :--- |
| AND | 0x0 | op addr | M[AR]->DR, AC^DR->AC, End |
| ADD | 0x1 | op addr | M[AR]->DR, AC+DR->AC,E, End |
| LDA | 0x2 | op addr | M[AR]->DR, DR->AC, End |
| STA | 0x3 | op addr | AC->M[AR], End |
| BUN | 0x4 | op addr | AR->PC, End |
| ISZ | 0x6 | op addr | M[AR]->DR, DR+1->DR, DR->M[AR], if(DR!=0)skip-1, PC+1->PC, End |
| CLA | 0x7800 | opcode | 0->AC, End |
| CLE | 0x7400 | opcode | 0->E, End |
| CMA | 0x7200 | opcode | AC'->AC, End |
| CME | 0x7100 | opcode | E'->E, End |
| CIR | 0x7080 | opcode | AC(0)->TMP, shr AC, E->AC(15), TMP->E, End |
| CIL | 0x7040 | opcode | AC(15)->TMP, shl AC, E->AC(0), TMP->E, End |
| INC | 0x7020 | opcode | AC+1->AC, End |
| SPA | 0x7010 | opcode | if(AC(15)!=0)skip-1, PC+1->PC, End |
| SNA | 0x7008 | opcode | if(AC(15)==0)skip-1, PC+1->PC, End |
| SZA | 0x7004 | opcode | if(AC!=0)skip-1, PC+1->PC, End |
| SZE | 0x7002 | opcode | if(E!=0)skip-1, PC+1->PC, End |
| HLT | 0x7001 | opcode | 1->S(halt), End |
| INP | 0xF800 | opcode | input-int->AC, End |
| OUT | 0xF400 | opcode | output-AC->int, End |

Reading the skip instructions: the test microinstruction omits `PC+1->PC` when the *opposite* condition holds, so PC is incremented (the next instruction is skipped) only when the instruction's own condition is true.

![Fig 1.17 – Machine instructions: ADD format (op, addr)](screenshots/p01_instr_add_format.png)

![Fig 1.18 – Machine instructions: CLA format (opcode 7800)](screenshots/p01_instr_cla_format.png)

![Fig 1.19 – Execute sequence of ADD](screenshots/p01_instr_add_execute.png)

![Fig 1.20 – Execute sequence of ISZ](screenshots/p01_instr_isz_execute.png)

### Step 7 – Fetch sequence, program counter and saving

Build the fetch sequence as described in Practical 2. Then in *Execute → Options…* choose **PC** as the program counter (debug mode needs it). Finally *File → Save machine as…* → `BasicComputer.cpu`.

## Observations

The Hardware Modules dialog shows 8 registers, 2 condition bits and the 4096-word RAM `M`. The machine has 33 microinstructions and 20 machine instructions. Loading `P03_ADD.a` (Practical 3) gives the machine code `F800 3007 F800 1007 …` in RAM, which confirms the instruction formats.

## Result

A machine based on the Basic Computer architecture was created in CPU Sim and saved as `BasicComputer.cpu`.

## Viva questions

**Q1. Why are PC and AR 12 bits wide while AC is 16 bits?**
Memory holds 4096 = 2¹² words, so an address needs 12 bits; each data word is 16 bits.

**Q2. Machine instruction versus microinstruction?**
A machine instruction (e.g. `ADD`) is what the programmer writes; it is carried out by a list of microinstructions, each a single register transfer such as `DR ← M[AR]`.

**Q3. What does the *halt* option of a condition bit do?**
When a microinstruction sets that bit to 1, CPU Sim stops the program. `HLT` uses it through `halt-S`.

**Q4. Why is the RAM cell size 16?**
Each instruction or data value is one 16-bit word, so one address holds one word and PC can simply advance by 1.

**Q5. Is this control unit hardwired or microprogrammed?**
Microprogrammed: every instruction is a stored sequence of microinstructions.

---

# Practical 2: Create the Fetch Routine of the Instruction Cycle

**Aim:** To create the fetch (and decode) routine of the instruction cycle and watch it run one microinstruction at a time.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

Every instruction cycle starts with the same fetch and decode phase. In Mano's design it takes three clock pulses, driven by the sequence counter outputs T0, T1 and T2:

```
T0 : AR <- PC
T1 : IR <- M[AR],  PC <- PC + 1
T2 : D0..D7 <- decode IR(12-14),  AR <- IR(0-11),  I <- IR(15)
```

After T2 the control unit knows which instruction is in IR and AR already holds its address field, so execution starts at T3. In CPU Sim the fetch routine is a list of microinstructions that runs before every execute sequence. Real hardware does `IR ← M[AR]` and `PC ← PC + 1` on the same clock edge; CPU Sim runs microinstructions one after another, so they appear as separate steps.

| Order | CPU Sim microinstruction | Register transfer | Time step |
| :--- | :--- | :--- | :--- |
| 1 | `PC->AR` | AR ← PC | T0 |
| 2 | `M[AR]->IR` | IR ← M[AR] | T1 |
| 3 | `PC+1->PC` | PC ← PC + 1 | T1 |
| 4 | `IR(0-11)->AR` | AR ← IR(0–11) | T2 |
| 5 | `decode-IR` | D0…D7 ← decode IR(12–14) | T2 |

## Procedure

1. Open the machine from Practical 1 and choose *Modify → Fetch Sequence* (Ctrl+Y).
2. In the *MicroInstructions* tree, drag `PC->AR` (transferRtoR) into *Fetch Sequence Implementation*.
3. Drag `M[AR]->IR` (memoryAccess) below it.
4. Drag `PC+1->PC` (increment).
5. Drag `IR(0-11)->AR` (transferRtoR).
6. Drag `decode-IR` (decode) to the end, click **OK**, and save the machine (Ctrl+B).

![Fig 2.1 – Fetch sequence dialog with the five microinstructions](screenshots/p02_fetch_sequence.png)

## Testing the routine

Open `programs/P03_ADD.a`, press **Ctrl+2** to assemble and load, then **Ctrl+D** for debug mode. Set the Registers *Data* box to **Unsigned Dec**. Click **Step by Micro** five times and watch which register each microinstruction changes (changed registers are outlined in green).

![Fig 2.2 – Debug mode before the first micro-step (all registers 0)](screenshots/p02_before_stepping.png)

![Fig 2.3 – After micro-step 2: IR = 63488 (F800 hex)](screenshots/p02_after_step2.png)

![Fig 2.4 – After micro-step 5: decode-IR selects INP](screenshots/p02_after_step5.png)

## Observations

{{FETCH}}

The first instruction in memory is `F800` (`INP`). `IR(0-11)->AR` copies its low 12 bits (`800` hex = 2048) into AR, even though INP does not use AR as an address; the fetch routine is shared by all instructions.

## Result

The fetch routine `PC->AR`, `M[AR]->IR`, `PC+1->PC`, `IR(0-11)->AR`, `decode-IR` was created and verified by single-stepping the first instruction of a program.

## Viva questions

**Q1. Why is PC incremented during fetch?**
So it already points to the next instruction; a branch can simply overwrite it and a skip can add one more.

**Q2. Why does AR receive IR(0–11) even for register-reference instructions?**
The fetch routine is common to every instruction. For memory-reference instructions that field is the operand address; for the others it is simply unused.

**Q3. What does the decode microinstruction do?**
It examines IR and transfers control to the execute sequence of the matching machine instruction.

**Q4. How many clock pulses does fetch-and-decode take in the Basic Computer?**
Three: T0, T1 and T2.

---

# Practical 3: ADD Operation on Two User-entered Numbers

**Aim:** To write an assembly program that reads two numbers entered by the user, adds them and displays the sum.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

`INP` reads an integer into AC. Because the second `INP` overwrites AC, the first number is saved in memory with `STA A`. `ADD A` is a memory-reference instruction: `DR ← M[A]`, then `AC ← AC + DR`, and the carry out of the top bit goes to E. `OUT` prints AC and `HLT` stops the machine.

Numbers are 16-bit two's complement, so the range is −32768 to +32767. A sum outside that range wraps around (see the last sample run below).

## Program – `programs/P03_ADD.a`

{{PROGRAM P03_ADD.a}}

### Assembled program (memory map)

{{MEMMAP P03_ADD.a}}

Memory-reference instructions are the opcode digit followed by the 12-bit address (`ADD A` with A at address 7 is `1007`); `INP`, `OUT` and `HLT` are fixed 16-bit codes (`F800`, `F400`, `7001`).

## Procedure

1. *File → Open machine…* → `BasicComputer.cpu`.
2. *File → Open text…* → `P03_ADD.a`. Set the RAM pane's *Data* box to **Hex**.
3. Press **Ctrl+2** (assemble and load) and compare the RAM pane with the memory map above.
4. Press **Ctrl+R**. When the console turns yellow type `25` and press Enter, then type `17` and press Enter.
5. The console prints `Output: 42` and the halt message.

![Fig 3.1 – Program open in the text editor](screenshots/p03_program_loaded.png)

![Fig 3.2 – After Ctrl+2: machine code in RAM (Data = Hex)](screenshots/p03_after_assemble.png)

![Fig 3.3 – After Ctrl+R: yellow console waiting for the first number](screenshots/p03_waiting_first_input.png)

![Fig 3.4 – After the first number: waiting for the second](screenshots/p03_after_first_input.png)

![Fig 3.5 – Final output 42 and "EXECUTION HALTED NORMALLY"](screenshots/p03_output.png)

## Observations

{{RUNS P03_ADD.a}}

With inputs 25 and 17 the final registers are AC = 42, DR = 25 (the operand read by `ADD`), PC = 7, IR = 28673 (`7001`, the HLT) and E = 0. Memory holds A = `0019` and SUM = `002A` (hex).

For −1 + 1 the result is 0 and **E = 1**: the 16-bit addition `FFFF + 0001` carries out of bit 15. For 30000 + 10000 the true sum 40000 does not fit in 16-bit two's complement, so the output wraps to 40000 − 65536 = −25536.

## Result

The program correctly adds two user-entered numbers: 25 + 17 = **42**.

## Viva questions

**Q1. Why is the first number stored before the second `INP`?**
`INP` overwrites AC, so the first number would be lost.

**Q2. What is the machine code of `ADD A` if A is at address 7?**
Opcode 1 and address 007: `1007` hex.

**Q3. What does E hold after `ADD`?**
The carry out of the most significant bit of the addition.

**Q4. Why does 30000 + 10000 print −25536?**
The sum exceeds +32767; the 16-bit result `9C40` is read as a negative two's complement number (overflow).

---

# Practical 4: SUBTRACT Operation on Two User-entered Numbers

**Aim:** To write an assembly program that reads two numbers A and B and displays A − B.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

The Basic Computer has no subtract instruction, so subtraction is done with the two's complement: **A − B = A + (B′ + 1)**. `CMA` forms the one's complement B′, `INC` adds 1 to give −B, and `ADD` adds A.

```
A       = 18 = 0000 0000 0001 0010
B       = 50 = 0000 0000 0011 0010
B'      =      1111 1111 1100 1101     (CMA)
B' + 1  =      1111 1111 1100 1110     (INC)  = -50
A + (-B)=      1111 1111 1110 0000     = -32
```

## Program – `programs/P04_SUBTRACT.a`

{{PROGRAM P04_SUBTRACT.a}}

### Assembled program (memory map)

{{MEMMAP P04_SUBTRACT.a}}

## Procedure

1. Open `BasicComputer.cpu` and `P04_SUBTRACT.a`; set the RAM *Data* box to **Hex**.
2. Press **Ctrl+2**, then **Ctrl+R**.
3. Enter the minuend `18` (Enter), then the subtrahend `50` (Enter).
4. The console prints `Output: -32`.

![Fig 4.1 – Program open in the text editor](screenshots/p04_program_loaded.png)

![Fig 4.2 – After Ctrl+2: machine code in RAM](screenshots/p04_after_assemble.png)

![Fig 4.3 – Console output -32 and normal halt](screenshots/p04_output.png)

## Observations

{{RUNS P04_SUBTRACT.a}}

For 18 − 50 the final AC is −32 (`FFE0` hex), DR = 18 and PC = 9.

## Result

The program subtracts two user-entered numbers using the two's complement: 18 − 50 = **−32** and 50 − 18 = **32**.

## Viva questions

**Q1. How do you subtract without a SUB instruction?**
Add the two's complement of the subtrahend: complement it (`CMA`), add 1 (`INC`), then `ADD`.

**Q2. Why is `INC` needed after `CMA`?**
`CMA` gives −B − 1; adding 1 gives −B.

**Q3. What is the two's complement of `0000 0000 0011 0010`?**
`1111 1111 1100 1110` (`FFCE` hex) = −50.

**Q4. Which register-reference instructions does the program use?**
`CMA` (7200), `INC` (7020) and `HLT` (7001).

---

# Practical 5: Logical Operations: AND, OR, NOT, XOR, NOR, NAND

**Aim:** To write an assembly program that performs AND, OR, NOT, XOR, NOR and NAND on two user-entered numbers.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

The machine has only two logic instructions: `AND` (memory-reference, AC ← AC ∧ M[x]) and `CMA` (AC ← AC′). Since {AND, NOT} is functionally complete, everything else can be built from them with Boolean algebra, applied to all 16 bits at once:

| Operation | Identity used | Instruction sequence |
| :--- | :--- | :--- |
| A AND B | A·B | `LDA A`, `AND B` |
| A OR B | (A′·B′)′ (De Morgan) | `LDA B`, `CMA`, `STA NB`, `LDA A`, `CMA`, `AND NB`, `CMA` |
| NOT A | A′ | `LDA A`, `CMA` |
| A XOR B | (A + B)·(A·B)′ | `LDA RAND`, `CMA`, `AND ROR` |
| A NOR B | (A + B)′ | `LDA ROR`, `CMA` |
| A NAND B | (A·B)′ | `LDA RAND`, `CMA` |

Results are shown as signed decimal numbers. Complementing a small positive number sets the sign bit, so NOT 12 = −13 (in two's complement, x′ = −x − 1).

## Program – `programs/P05_LOGIC.a`

{{PROGRAM P05_LOGIC.a}}

### Assembled program (memory map)

{{MEMMAP P05_LOGIC.a}}

## Procedure

1. Open `BasicComputer.cpu` and `P05_LOGIC.a`; set the RAM *Data* box to **Hex**.
2. Press **Ctrl+2**, then **Ctrl+R**; enter `12` (Enter) and `10` (Enter).
3. Seven outputs are printed in the order AND, OR, NOT A, NOT B, XOR, NOR, NAND. Scroll the console up to see them all.

![Fig 5.1 – Program open in the text editor](screenshots/p05_program_loaded.png)

![Fig 5.2 – After Ctrl+2: machine code in RAM](screenshots/p05_after_assemble.png)

![Fig 5.3 – Console showing all seven outputs (scroll to the top)](screenshots/p05_output.png)

## Observations

For A = 12 and B = 10:

{{LOGICTABLE}}

Further runs:

{{RUNS P05_LOGIC.a}}

## Result

All six logical operations were produced using only `AND` and `CMA`. For A = 12 and B = 10 the outputs are AND = 8, OR = 14, NOT A = −13, NOT B = −11, XOR = 6, NOR = −15, NAND = −9.

## Viva questions

**Q1. Which logic instructions does the Basic Computer have?**
`AND` (memory-reference) and `CMA` (complement AC). OR and XOR have to be built from them.

**Q2. State De Morgan's law as used for OR.**
A + B = (A′·B′)′.

**Q3. Why is NOT 12 displayed as −13?**
`CMA` flips all 16 bits: `000C` becomes `FFF3`, which is −13 in two's complement.

**Q4. What does "functionally complete" mean?**
Every Boolean function can be written using only that set of operations, e.g. {AND, NOT} or {NAND}.

**Q5. How would you clear the upper 8 bits of AC?**
`AND` with a memory word containing `00FF` (a mask).

---

# Practical 6: Memory-reference Instructions: ADD, LDA, STA, BUN, ISZ

**Aim:** To write an assembly program that exercises the memory-reference instructions `ADD`, `LDA`, `STA`, `BUN` and `ISZ`, and record the registers after every instruction.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

A memory-reference instruction has an opcode 0–6 and a 12-bit address. During fetch `AR ← IR(0–11)`, so when execution starts AR already holds the operand address (direct addressing, I = 0).

| Symbol | Code | Execute micro-operations |
| :--- | :--- | :--- |
| ADD | 1xxx | DR ← M[AR]; AC ← AC + DR, E ← Cout |
| LDA | 2xxx | DR ← M[AR]; AC ← DR |
| STA | 3xxx | M[AR] ← AC |
| BUN | 4xxx | PC ← AR |
| ISZ | 6xxx | DR ← M[AR]; DR ← DR + 1; M[AR] ← DR; if DR = 0 then PC ← PC + 1 |

The program multiplies X = 5 by N = 3 using repeated addition. `CTR` starts at −3. Each pass adds X to `PROD` and `ISZ CTR` increments CTR; while CTR is not zero the following `BUN LOOP` repeats the loop. When CTR reaches 0 the `ISZ` skips the `BUN` and the program ends with PROD = 15.

## Program – `programs/P06_MEMORY_REFERENCE.a`

{{PROGRAM P06_MEMORY_REFERENCE.a}}

### Assembled program (memory map)

{{MEMMAP P06_MEMORY_REFERENCE.a}}

## Procedure

1. Open `BasicComputer.cpu` and `P06_MEMORY_REFERENCE.a`.
2. Press **Ctrl+2**, then **Ctrl+D** to enter debug mode.
3. Set the Registers *Data* box to **Unsigned Dec** and the RAM *Data* box to **Hex**.
4. Click **Step by Instr** once per instruction (16 times) and record AC, DR, E, PC, AR and IR after each step.
5. When `HLT` runs the console shows "EXECUTION HALTED NORMALLY". **Start Over** repeats the trace.

![Fig 6.1 – Debug mode before the first step (all registers 0)](screenshots/p06_before_stepping.png)

![Fig 6.2 – After step 4, ISZ CTR: CTR = -2 (DR = 65534), not zero, so no skip (PC = 4)](screenshots/p06_after_step4.png)

![Fig 6.3 – After step 5, BUN LOOP: PC = AR = 0](screenshots/p06_after_step5.png)

![Fig 6.4 – After step 14, third ISZ CTR: DR = 0, PC incremented again (PC = 5)](screenshots/p06_after_step14.png)

![Fig 6.5 – After step 16, HLT: AC = 15 and PROD (address 9) = 000F](screenshots/p06_after_step16.png)

## Observations

Register contents (decimal) after each instruction:

{{TRACE P06_MEMORY_REFERENCE.a dr}}

Values in brackets are the signed reading of the 16-bit number. Final memory: X = 5, CTR = 0, PROD = 15.

## Result

`LDA`, `ADD` and `STA` computed the running product, `ISZ` counted the passes and skipped the branch when the counter reached zero, and `BUN` formed the loop. Final **AC = PROD = 15**.

## Viva questions

**Q1. What is a memory-reference instruction?**
One whose operand is in memory; its 12-bit address field gives the location (opcodes 0–6 here).

**Q2. Why is CTR initialised to −3 and not 3?**
`ISZ` can only count upwards and test for zero, so counting up from −N reaches zero after N increments.

**Q3. What is the machine code of `ISZ CTR` with CTR at address 8?**
`6008` hex.

**Q4. What happens if CTR starts at 0?**
The first `ISZ` makes it 1, so the loop would run about 65536 times before CTR wraps back to 0.

**Q5. How does `ISZ` differ from `INC`?**
`ISZ` increments a *memory word* and may skip; `INC` increments AC and never skips.

---

# Practical 7: Register-reference Instructions: CLA, CMA, CME, HLT

**Aim:** To simulate `CLA`, `CMA`, `CME` and `HLT` and determine AC, E, PC, AR and IR (decimal) after each instruction.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

Register-reference instructions have the code 7xxx (opcode 111 with I = 0). The low 12 bits select one operation on AC or E, and no memory is accessed. Because the fetch routine always performs `AR ← IR(0–11)`, AR ends up holding the low 12 bits of the instruction code (800 hex = 2048 for `CLA`).

| Symbol | Code | Bit set in IR(0–11) | Operation |
| :--- | :--- | :--- | :--- |
| CLA | 7800 | B11 | AC ← 0 |
| CMA | 7200 | B9 | AC ← AC′ |
| CME | 7100 | B8 | E ← E′ |
| HLT | 7001 | B0 | S ← 1 (halt) |

An `LDA NUM` (AC ← 25) is placed first so the effect of `CLA` can be seen.

## Program – `programs/P07_REGISTER_REF_CLA_CMA_CME_HLT.a`

{{PROGRAM P07_REGISTER_REF_CLA_CMA_CME_HLT.a}}

### Assembled program (memory map)

{{MEMMAP P07_REGISTER_REF_CLA_CMA_CME_HLT.a}}

## Procedure

1. Open `BasicComputer.cpu` and the program; press **Ctrl+2**, then **Ctrl+D**.
2. Set the Registers *Data* box to **Unsigned Dec** and the RAM *Data* box to **Hex**.
3. Click **Step by Instr** five times, recording AC, E, PC, AR and IR after each click.

![Fig 7.1 – After assembling and loading (debug mode)](screenshots/p07_loaded.png)

![Fig 7.2 – After step 1, LDA NUM: AC = 25](screenshots/p07_after_step1.png)

![Fig 7.3 – After step 2, CLA: AC = 0, AR = 2048](screenshots/p07_after_step2.png)

![Fig 7.4 – After step 3, CMA: AC = 65535, AR = 512](screenshots/p07_after_step3.png)

![Fig 7.5 – After step 4, CME: E = 1, AR = 256](screenshots/p07_after_step4.png)

![Fig 7.6 – After step 5, HLT: S = 1, execution halted](screenshots/p07_after_step5.png)

## Observations

Register contents (decimal) after each instruction:

{{TRACE P07_REGISTER_REF_CLA_CMA_CME_HLT.a}}

Final register contents after `HLT`:

{{FINAL P07_REGISTER_REF_CLA_CMA_CME_HLT.a}}

AC is 65535 in *Unsigned Dec* and −1 in *Dec*; both are `FFFF`. PC = 5 because it holds the address after the `HLT` at address 4.

## Result

After execution: **AC = 65535 (−1), E = 1, PC = 5, AR = 1, IR = 28673.**

## Viva questions

**Q1. How does the control unit recognise a register-reference instruction?**
IR(14–12) = 111 and I = 0 (code 7xxx).

**Q2. Why is AR = 1 after `HLT`?**
Fetch does `AR ← IR(0–11)`, and the low 12 bits of `7001` are 001.

**Q3. Difference between `CLA` and `CLE`?**
`CLA` clears the 16-bit accumulator; `CLE` clears the 1-bit E flip-flop.

**Q4. Write two instructions that load −1 into AC.**
`CLA` followed by `CMA`.

---

# Practical 8: Register-reference Instructions: INC, SPA, SNA, SZE

**Aim:** To simulate `INC`, `SPA`, `SNA` and `SZE` and determine AC, E, PC, AR and IR (decimal) after each instruction.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

| Symbol | Code | Operation |
| :--- | :--- | :--- |
| INC | 7020 | AC ← AC + 1 |
| SPA | 7010 | if AC(15) = 0 (AC positive or zero) then PC ← PC + 1 |
| SNA | 7008 | if AC(15) = 1 (AC negative) then PC ← PC + 1 |
| SZE | 7002 | if E = 0 then PC ← PC + 1 |

A skip instruction increments PC one extra time when its condition is true, so the next instruction is not executed. In this program every skip is followed by a `HLT` "trap": the last `HLT` is reached only if every skip works. AC starts at −2 so that both a negative and a non-negative value are tested.

## Program – `programs/P08_REGISTER_REF_INC_SPA_SNA_SZE.a`

{{PROGRAM P08_REGISTER_REF_INC_SPA_SNA_SZE.a}}

### Assembled program (memory map)

{{MEMMAP P08_REGISTER_REF_INC_SPA_SNA_SZE.a}}

## Procedure

1. Open `BasicComputer.cpu` and the program; press **Ctrl+2**, then **Ctrl+D**.
2. Set the Registers *Data* box to **Unsigned Dec** and the RAM *Data* box to **Hex**.
3. Click **Step by Instr** eight times, recording AC, E, PC, AR and IR after each click.

![Fig 8.1 – After assembling and loading (debug mode)](screenshots/p08_loaded.png)

![Fig 8.2 – After step 1, LDA NUM: AC = 65534 (-2)](screenshots/p08_after_step1.png)

![Fig 8.3 – After step 2, INC: AC = 65535 (-1)](screenshots/p08_after_step2.png)

![Fig 8.4 – After step 3, SNA: AC negative, PC jumps from 2 to 4](screenshots/p08_after_step3.png)

![Fig 8.5 – After step 4, INC: AC = 0](screenshots/p08_after_step4.png)

![Fig 8.6 – After step 5, SPA: sign bit 0, PC jumps from 5 to 7](screenshots/p08_after_step5.png)

![Fig 8.7 – After step 6, SZE: E = 0, PC jumps from 7 to 9](screenshots/p08_after_step6.png)

![Fig 8.8 – After step 7, INC: AC = 1](screenshots/p08_after_step7.png)

![Fig 8.9 – After step 8, HLT: halted with PC = 11](screenshots/p08_after_step8.png)

## Observations

Register contents (decimal) after each instruction:

{{TRACE P08_REGISTER_REF_INC_SPA_SNA_SZE.a}}

The instructions at addresses 3, 6 and 8 were never executed: the PC column goes 2 → 4, 5 → 7 and 7 → 9.

Final register contents after `HLT`:

{{FINAL P08_REGISTER_REF_INC_SPA_SNA_SZE.a}}

## Result

`INC`, `SPA`, `SNA` and `SZE` were simulated and every skip was verified. After execution: **AC = 1, E = 0, PC = 11, AR = 1, IR = 28673.**

## Viva questions

**Q1. What does "skip" mean in the Basic Computer?**
PC is incremented once more, so the next instruction in memory is not executed.

**Q2. Does `SPA` skip when AC = 0?**
Yes. `SPA` tests only the sign bit, and zero has a sign bit of 0.

**Q3. How do you branch to X when AC is negative?**
`SPA` followed by `BUN X`: if AC is non-negative the `BUN` is skipped, otherwise it executes.

**Q4. Difference between `SZA` and `SZE`?**
`SZA` skips if AC = 0; `SZE` skips if E = 0.

**Q5. Why is AR = 32 after `INC`?**
Fetch loads AR with the low 12 bits of `7020`, which is `020` hex = 32.

---

# Practical 9: Register-reference Instructions: CIR, CIL

**Aim:** To simulate `CIR` and `CIL` and determine AC, E, PC, AR and IR (decimal) after each instruction.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

`CIR` and `CIL` circulate (rotate) the 17-bit combination of E and AC by one position:

```
CIR (7080): E -> AC(15) -> AC(14) -> ... -> AC(0) -> E     rotate right
CIL (7040): E <- AC(15) <- AC(14) <- ... <- AC(0) <- E     rotate left
```

No bit is lost, so a `CIR` followed by a `CIL` restores AC and E. CPU Sim has no 17-bit rotate, so each is built with the 1-bit scratch register TMP: the bit leaving AC is saved in TMP, AC is shifted, the old E enters the vacated end, and TMP is copied to E.

```
               E   AC
start          0   0000 0000 0000 1001  = 9
CIR            1   0000 0000 0000 0100  = 4      (AC bit 0 went into E)
CIR            0   1000 0000 0000 0010  = 32770  (old E entered AC bit 15)
CIL            1   0000 0000 0000 0100  = 4
CIL            0   0000 0000 0000 1001  = 9      (original value restored)
```

## Program – `programs/P09_REGISTER_REF_CIR_CIL.a`

{{PROGRAM P09_REGISTER_REF_CIR_CIL.a}}

### Assembled program (memory map)

{{MEMMAP P09_REGISTER_REF_CIR_CIL.a}}

## Procedure

1. Open `BasicComputer.cpu` and the program; press **Ctrl+2**, then **Ctrl+D**.
2. Set the Registers *Data* box to **Unsigned Dec** and the RAM *Data* box to **Hex**.
3. Click **Step by Instr** six times, recording AC, E, PC, AR and IR after each click.

![Fig 9.1 – After assembling and loading (debug mode)](screenshots/p09_loaded.png)

![Fig 9.2 – After step 1, LDA NUM: AC = 9, E = 0](screenshots/p09_after_step1.png)

![Fig 9.3 – After step 2, CIR: AC = 4, E = 1](screenshots/p09_after_step2.png)

![Fig 9.4 – After step 3, CIR: AC = 32770, E = 0](screenshots/p09_after_step3.png)

![Fig 9.5 – After step 4, CIL: AC = 4, E = 1](screenshots/p09_after_step4.png)

![Fig 9.6 – After step 5, CIL: AC = 9, E = 0](screenshots/p09_after_step5.png)

![Fig 9.7 – After step 6, HLT: halted](screenshots/p09_after_step6.png)

## Observations

Register contents (decimal) after each instruction:

{{TRACE P09_REGISTER_REF_CIR_CIL.a}}

Final register contents after `HLT`:

{{FINAL P09_REGISTER_REF_CIR_CIL.a}}

## Result

Two right rotations followed by two left rotations restored AC = 9. After execution: **AC = 9, E = 0, PC = 6, AR = 1, IR = 28673.** The values after each individual instruction are in the table above.

## Viva questions

**Q1. How does a circular shift differ from a logical shift?**
A circular shift feeds the bit shifted out back in at the other end (through E); a logical shift inserts 0 and loses the bit.

**Q2. How many bits take part in `CIR` / `CIL`?**
17: the 16 bits of AC plus E.

**Q3. How can `CIL` double AC?**
Clear E first (`CLE`); then `CIL` shifts AC left with a 0 entering bit 0, and E receives the old sign bit.

**Q4. What is AR after `CIR`?**
128, the low 12 bits of `7080` hex.

**Q5. After how many `CIL` operations do AC and E return to their starting values?**
17.

---

# Practical 10: Sum of Integers until a Negative Number is Read

**Aim:** To write an assembly program that reads integers and adds them until a negative non-zero number is read, then outputs the sum (not including that last number).

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

This is a sentinel-controlled loop: a negative number marks the end of the data. After each `INP`, `SPA` skips the exit branch when AC ≥ 0. For a negative number the skip does not happen, so `BUN DONE` leaves the loop *before* the number is added. Zero counts as non-negative, so it is added (it does not change the sum).

```
LOOP: INP -> AC >= 0 ?  --yes--> SUM = SUM + AC --> back to LOOP
                         |
                         no
                         v
DONE: LDA SUM -> OUT -> HLT
```

## Program – `programs/P10_SUM_UNTIL_NEGATIVE.a`

{{PROGRAM P10_SUM_UNTIL_NEGATIVE.a}}

### Assembled program (memory map)

{{MEMMAP P10_SUM_UNTIL_NEGATIVE.a}}

## Procedure

1. Open `BasicComputer.cpu` and the program; set the RAM *Data* box to **Hex**.
2. Press **Ctrl+2**, then **Ctrl+R**.
3. Enter `4`, `10`, `0`, `6` and finally `-3`, pressing Enter after each.
4. The console prints `Output: 20`.

![Fig 10.1 – Program open in the text editor](screenshots/p10_program_loaded.png)

![Fig 10.2 – After Ctrl+2: machine code in RAM](screenshots/p10_after_assemble.png)

![Fig 10.3 – Console after entering 4, 10, 0, 6, -3: Output 20](screenshots/p10_output.png)

## Observations

{{RUNS P10_SUM_UNTIL_NEGATIVE.a}}

For the inputs 4, 10, 0, 6, −3 the loop adds four numbers; SUM (address 9) holds `0014` hex = 20. If the first number is negative the sum is 0.

## Result

The program adds integers until a negative number is read and displays the sum excluding it: 4 + 10 + 0 + 6 = **20**.

## Viva questions

**Q1. Why is `SPA` used and not `SNA`?**
`SPA` skips the exit branch for non-negative numbers, so `BUN DONE` runs only for negative input. With `SNA` the branches would have to be arranged the other way round.

**Q2. What happens when 0 is entered?**
Zero is non-negative, so it is added and the loop continues.

**Q3. Why is the negative number not included in the sum?**
The test is made right after `INP`, before `ADD SUM`.

**Q4. What is a sentinel value?**
A special input (here, any negative number) that marks the end of the data.

---

# Practical 11: Sum of Integers until Zero is Read

**Aim:** To write an assembly program that reads integers and adds them until zero is read, then outputs the sum.

**Tool:** CPU Sim 4.0.11 (Java 8 with JavaFX)

## Theory

Here the sentinel is 0. `SZA` skips the next instruction when AC = 0. A skip can jump over only one instruction, so two branches are used: when AC ≠ 0 the `BUN ADDIT` executes and the number is added; when AC = 0 that branch is skipped and `BUN DONE` ends the loop. Negative numbers are added normally.

## Program – `programs/P11_SUM_UNTIL_ZERO.a`

{{PROGRAM P11_SUM_UNTIL_ZERO.a}}

### Assembled program (memory map)

{{MEMMAP P11_SUM_UNTIL_ZERO.a}}

## Procedure

1. Open `BasicComputer.cpu` and the program; set the RAM *Data* box to **Hex**.
2. Press **Ctrl+2**, then **Ctrl+R**.
3. Enter `8`, `12`, `-5` and `0`, pressing Enter after each.
4. The console prints `Output: 15`.

![Fig 11.1 – Program open in the text editor](screenshots/p11_program_loaded.png)

![Fig 11.2 – After Ctrl+2: machine code in RAM](screenshots/p11_after_assemble.png)

![Fig 11.3 – Console after entering 8, 12, -5, 0: Output 15](screenshots/p11_output.png)

## Observations

{{RUNS P11_SUM_UNTIL_ZERO.a}}

For 8, 12, −5, 0 the final AC and SUM are 15. **E = 1** in the final register view, because adding −5 (`FFFB`) to 20 carries out of bit 15; the 16-bit result `000F` is still correct. (In the *Dec* view a 1-bit register holding 1 is shown as −1.)

## Result

The program adds integers until 0 is read and displays the sum: 8 + 12 + (−5) = **15**.

## Viva questions

**Q1. Why are two `BUN` instructions needed after `SZA`?**
A skip jumps over only one instruction, so one branch handles the non-zero case and the next handles zero.

**Q2. How does this differ from Practical 10?**
The loop ends on 0 instead of a negative number, and negative numbers are added.

**Q3. Why is E = 1 at the end for 8, 12, −5, 0?**
`20 + FFFB` exceeds `FFFF`, so a carry goes into E. The 16-bit result is still correct.

**Q4. What is the output if the first number is 0?**
0.

**Q5. What is the machine code of `SZA`?**
`7004` hex.

---

# Appendix: Quick reference

| Symbol | Hex | Operation |
| :--- | :--- | :--- |
| AND | 0xxx | DR ← M[AR]; AC ← AC ∧ DR |
| ADD | 1xxx | DR ← M[AR]; AC ← AC + DR, E ← Cout |
| LDA | 2xxx | DR ← M[AR]; AC ← DR |
| STA | 3xxx | M[AR] ← AC |
| BUN | 4xxx | PC ← AR |
| ISZ | 6xxx | DR ← M[AR]; DR ← DR + 1; M[AR] ← DR; if DR = 0 then PC ← PC + 1 |
| CLA | 7800 | AC ← 0 |
| CLE | 7400 | E ← 0 |
| CMA | 7200 | AC ← AC′ |
| CME | 7100 | E ← E′ |
| CIR | 7080 | rotate E and AC right |
| CIL | 7040 | rotate E and AC left |
| INC | 7020 | AC ← AC + 1 |
| SPA | 7010 | if AC(15) = 0 then PC ← PC + 1 |
| SNA | 7008 | if AC(15) = 1 then PC ← PC + 1 |
| SZA | 7004 | if AC = 0 then PC ← PC + 1 |
| SZE | 7002 | if E = 0 then PC ← PC + 1 |
| HLT | 7001 | S ← 1 (halt) |
| INP | F800 | AC ← integer typed by the user |
| OUT | F400 | display AC as an integer |

**Common problems**

| Symptom | Cause and fix |
| :--- | :--- |
| `Undefined symbol` / label error | A label is misspelt or has no colon. Labels are case-sensitive. |
| `Unknown instruction` | The loaded machine is not `BasicComputer.cpu`, or the mnemonic is not in capitals. |
| Console stays yellow | The program is waiting at an `INP`: type a number and press Enter. |
| Program never ends | A loop has no exit. Use *Execute → Stop* (Ctrl+.). |
| Warning when entering debug mode | Select **PC** as the program counter in *Execute → Options…*. |
| RAM shows little boxes | Set the RAM pane's *Data* box to Hex or Dec. |
| CPU Sim will not start | Java 8 **with JavaFX** is required (e.g. Azul Zulu JDK FX 8 or BellSoft Liberica JDK 8 Full); newer Java versions ship without JavaFX. |

Number bases in the Registers pane: **Dec** shows each register as a signed two's complement number of its own width (a 1-bit register holding 1 appears as −1); **Unsigned Dec** shows the plain binary value. Use *Unsigned Dec* for register traces and *Dec* for arithmetic results.
