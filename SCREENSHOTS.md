# Screenshot checklist

The README links to 68 screenshots in `screenshots/`. Take them from **your own** CPU Sim window, save each as PNG with exactly the file name shown, and tick it off here. Until a file exists, GitHub shows the caption text in its place.

**Tips**

- Use one window size for all shots (maximised is fine) and crop out the desktop.
- Registers pane *Data* = **Unsigned Dec** for the trace practicals (6 to 9); RAM pane *Data* = **Hex**.
- For the step-by-step shots, keep the register pane and the highlighted instruction both visible.
- Add your name or roll number somewhere in the first shot of each practical if your teacher asks for it.


## Practical 1

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p01_new_machine.png` | Fig 1.1 – File menu: New machine |
| [ ] | `p01_registers.png` | Fig 1.2 – Hardware Modules: the eight registers |
| [ ] | `p01_condition_bits.png` | Fig 1.3 – Condition bits carry-E and halt-S |
| [ ] | `p01_ram.png` | Fig 1.4 – RAM M: 4096 cells of 16 bits |
| [ ] | `p01_micro_transferrtor.png` | Fig 1.5 – TransferRtoR microinstructions |
| [ ] | `p01_micro_memoryaccess.png` | Fig 1.6 – MemoryAccess microinstructions |
| [ ] | `p01_micro_increment.png` | Fig 1.7 – Increment microinstructions |
| [ ] | `p01_micro_arithmetic.png` | Fig 1.8 – Arithmetic microinstruction |
| [ ] | `p01_micro_logical.png` | Fig 1.9 – Logical microinstructions |
| [ ] | `p01_micro_shift.png` | Fig 1.10 – Shift microinstructions |
| [ ] | `p01_micro_set.png` | Fig 1.11 – Set microinstructions |
| [ ] | `p01_micro_test.png` | Fig 1.12 – Test microinstructions |
| [ ] | `p01_micro_decode.png` | Fig 1.13 – Decode microinstruction |
| [ ] | `p01_micro_setcondbit.png` | Fig 1.14 – SetCondBit microinstruction |
| [ ] | `p01_micro_io.png` | Fig 1.15 – IO microinstructions |
| [ ] | `p01_fields.png` | Fig 1.16 – Edit Fields dialog |
| [ ] | `p01_instr_add_format.png` | Fig 1.17 – Machine instructions: ADD format (op, addr) |
| [ ] | `p01_instr_cla_format.png` | Fig 1.18 – Machine instructions: CLA format (opcode 7800) |
| [ ] | `p01_instr_add_execute.png` | Fig 1.19 – Execute sequence of ADD |
| [ ] | `p01_instr_isz_execute.png` | Fig 1.20 – Execute sequence of ISZ |

## Practical 2

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p02_fetch_sequence.png` | Fig 2.1 – Fetch sequence dialog with the five microinstructions |
| [ ] | `p02_before_stepping.png` | Fig 2.2 – Debug mode before the first micro-step (all registers 0) |
| [ ] | `p02_after_step2.png` | Fig 2.3 – After micro-step 2: IR = 63488 (F800 hex) |
| [ ] | `p02_after_step5.png` | Fig 2.4 – After micro-step 5: decode-IR selects INP |

## Practical 3

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p03_program_loaded.png` | Fig 3.1 – Program open in the text editor |
| [ ] | `p03_after_assemble.png` | Fig 3.2 – After Ctrl+2: machine code in RAM (Data = Hex) |
| [ ] | `p03_waiting_first_input.png` | Fig 3.3 – After Ctrl+R: yellow console waiting for the first number |
| [ ] | `p03_after_first_input.png` | Fig 3.4 – After the first number: waiting for the second |
| [ ] | `p03_output.png` | Fig 3.5 – Final output 42 and "EXECUTION HALTED NORMALLY" |

## Practical 4

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p04_program_loaded.png` | Fig 4.1 – Program open in the text editor |
| [ ] | `p04_after_assemble.png` | Fig 4.2 – After Ctrl+2: machine code in RAM |
| [ ] | `p04_output.png` | Fig 4.3 – Console output -32 and normal halt |

## Practical 5

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p05_program_loaded.png` | Fig 5.1 – Program open in the text editor |
| [ ] | `p05_after_assemble.png` | Fig 5.2 – After Ctrl+2: machine code in RAM |
| [ ] | `p05_output.png` | Fig 5.3 – Console showing all seven outputs (scroll to the top) |

## Practical 6

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p06_before_stepping.png` | Fig 6.1 – Debug mode before the first step (all registers 0) |
| [ ] | `p06_after_step4.png` | Fig 6.2 – After step 4, ISZ CTR: CTR = -2 (DR = 65534), not zero, so no skip (PC = 4) |
| [ ] | `p06_after_step5.png` | Fig 6.3 – After step 5, BUN LOOP: PC = AR = 0 |
| [ ] | `p06_after_step14.png` | Fig 6.4 – After step 14, third ISZ CTR: DR = 0, PC incremented again (PC = 5) |
| [ ] | `p06_after_step16.png` | Fig 6.5 – After step 16, HLT: AC = 15 and PROD (address 9) = 000F |

## Practical 7

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p07_loaded.png` | Fig 7.1 – After assembling and loading (debug mode) |
| [ ] | `p07_after_step1.png` | Fig 7.2 – After step 1, LDA NUM: AC = 25 |
| [ ] | `p07_after_step2.png` | Fig 7.3 – After step 2, CLA: AC = 0, AR = 2048 |
| [ ] | `p07_after_step3.png` | Fig 7.4 – After step 3, CMA: AC = 65535, AR = 512 |
| [ ] | `p07_after_step4.png` | Fig 7.5 – After step 4, CME: E = 1, AR = 256 |
| [ ] | `p07_after_step5.png` | Fig 7.6 – After step 5, HLT: S = 1, execution halted |

## Practical 8

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p08_loaded.png` | Fig 8.1 – After assembling and loading (debug mode) |
| [ ] | `p08_after_step1.png` | Fig 8.2 – After step 1, LDA NUM: AC = 65534 (-2) |
| [ ] | `p08_after_step2.png` | Fig 8.3 – After step 2, INC: AC = 65535 (-1) |
| [ ] | `p08_after_step3.png` | Fig 8.4 – After step 3, SNA: AC negative, PC jumps from 2 to 4 |
| [ ] | `p08_after_step4.png` | Fig 8.5 – After step 4, INC: AC = 0 |
| [ ] | `p08_after_step5.png` | Fig 8.6 – After step 5, SPA: sign bit 0, PC jumps from 5 to 7 |
| [ ] | `p08_after_step6.png` | Fig 8.7 – After step 6, SZE: E = 0, PC jumps from 7 to 9 |
| [ ] | `p08_after_step7.png` | Fig 8.8 – After step 7, INC: AC = 1 |
| [ ] | `p08_after_step8.png` | Fig 8.9 – After step 8, HLT: halted with PC = 11 |

## Practical 9

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p09_loaded.png` | Fig 9.1 – After assembling and loading (debug mode) |
| [ ] | `p09_after_step1.png` | Fig 9.2 – After step 1, LDA NUM: AC = 9, E = 0 |
| [ ] | `p09_after_step2.png` | Fig 9.3 – After step 2, CIR: AC = 4, E = 1 |
| [ ] | `p09_after_step3.png` | Fig 9.4 – After step 3, CIR: AC = 32770, E = 0 |
| [ ] | `p09_after_step4.png` | Fig 9.5 – After step 4, CIL: AC = 4, E = 1 |
| [ ] | `p09_after_step5.png` | Fig 9.6 – After step 5, CIL: AC = 9, E = 0 |
| [ ] | `p09_after_step6.png` | Fig 9.7 – After step 6, HLT: halted |

## Practical 10

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p10_program_loaded.png` | Fig 10.1 – Program open in the text editor |
| [ ] | `p10_after_assemble.png` | Fig 10.2 – After Ctrl+2: machine code in RAM |
| [ ] | `p10_output.png` | Fig 10.3 – Console after entering 4, 10, 0, 6, -3: Output 20 |

## Practical 11

| Done | File | What it must show |
| :--- | :--- | :--- |
| [ ] | `p11_program_loaded.png` | Fig 11.1 – Program open in the text editor |
| [ ] | `p11_after_assemble.png` | Fig 11.2 – After Ctrl+2: machine code in RAM |
| [ ] | `p11_output.png` | Fig 11.3 – Console after entering 8, 12, -5, 0: Output 15 |
