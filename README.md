# Linux Process Lifecycles and OS Interaction

[![Standard](https://img.shields.io/badge/Language-C11%20%7C%20POSIX-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20POSIX-orange.svg)]()
[![Course](https://img.shields.io/badge/OS-ST5039CMD%20Programming%20%26%20OS-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A practical systems programming repository investigating **Linux Process Lifecycles, Virtual Memory Layouts, and OS Kernel Interaction**, mapping directly to **Lecture 2 (A Process Layout & OS Loading)** and **Lab 3 (Investigating Process Lifecycles)**.

---

## 🏗️ Architectural Overview: A Process in Memory

```
  [ Source Code: .c ] ──► [ gcc Compilation ] ──► [ Executable Binary: ELF ]
                                                          │
                                                          │ ./program (fork + execve)
                                                          ▼
                                              ┌───────────────────────────┐
                                              │    PROCESS (PID in RAM)   │
                                              │                           │
                                              │ ◄── Keyboard (scanf)      │
                                              │ ◄── OS Kernel (getpid)    │
                                              │ ──► Screen (printf)       │
                                              │ ──► Shell Exit Code ($?)  │
                                              └───────────────────────────┘
```

### Virtual Memory Layout
When a binary is loaded by `execve()`, the Linux kernel allocates a dedicated virtual address space structured into five major segments:

![Process Memory Layout](assets/screenshots/06_process_memory_layout.png)

1. **Stack**: Automatic local variables, function frames, return addresses (grows downwards).
2. **Heap**: Dynamic memory managed by `malloc()` and `free()` (grows upwards).
3. **BSS (`.bss`)**: Uninitialized global/static data (zeroed by OS kernel on load).
4. **Data (`.data`)**: Initialized global/static variables loaded directly from ELF image.
5. **Code/Text (`.text`)**: Executable binary machine instructions (Read-Only/Executable `R-X`).

---

## 📋 Lab Tasks & Terminal Verifications

### Task 1: The Long-Running Background Process
* **Source**: [`src/task1_alive.c`](src/task1_alive.c)
* **Concept**: Long-running server processes, background execution using the shell `&` operator, and process inspection via `ps aux`.

```bash
gcc src/task1_alive.c -o bin/task1
./bin/task1 &
ps aux | grep task1
```

![Task 1 - Background Execution](assets/screenshots/01_task1_background_ps.png)

* **Key Observation**: The process runs in the background with state `S` (**Interruptible Sleep**), demonstrating that `sleep(1)` yields CPU cycles back to the OS scheduler.

---

### Task 2: Process Identity (PID and PPID)
* **Source**: [`src/task2_identity.c`](src/task2_identity.c)
* **Concept**: Kernel process tracking using `getpid()` and `getppid()`, and verification using `ps -p <PID> -o pid,ppid,cmd`.

```bash
gcc src/task2_identity.c -o bin/task2
./bin/task2 &
ps -p 14389 -o pid,ppid,cmd
```

![Task 2 - PID and PPID Verification](assets/screenshots/02_task2_pid_ppid_verification.png)

* **Key Observation**: The program's Parent PID (`PPID: 12104`) matches the active bash shell process, demonstrating process hierarchy and inheritance.

---

### Task 3: Exit Codes and OS Feedback (`$?`)
* **Source**: [`src/task3_exit.c`](src/task3_exit.c)
* **Concept**: Communicating program outcome back to the operating system using exit codes (`0` for success, `1` for error) inspected via `$?`.

```bash
gcc src/task3_exit.c -o bin/task3

# Positive input -> Success (0)
./bin/task3
echo $?

# Negative input -> Failure (1)
./bin/task3
echo $?
```

![Task 3 - Exit Codes and Feedback](assets/screenshots/03_task3_exit_codes_feedback.png)

* **Key Observation**: Shell pipelines and automation rely on `$?` to determine whether subsequent commands should execute.

---

### Task 4: Standard I/O Streams (stdin & stdout)
* **Source**: [`src/task4_input.c`](src/task4_input.c)
* **Concept**: Standard streams provided by the OS: File Descriptor 0 (`stdin`) and File Descriptor 1 (`stdout`).

```bash
gcc src/task4_input.c -o bin/task4
./bin/task4
```

![Task 4 - Standard I/O Streams](assets/screenshots/04_task4_standard_io_streams.png)

* **Key Observation**: `scanf()` reads from `stdin` (unbuffered/line-buffered input), and `printf()` streams formatted text to `stdout`.

---

### Task 5: Conditional Execution and Termination
* **Source**: [`src/task5_control.c`](src/task5_control.c)
* **Concept**: Control flow branching based on user decisions, workload simulation, and deterministic exit code generation.

```bash
gcc src/task5_control.c -o bin/task5

# Run 1: Choice 1 (Continue -> Success)
./bin/task5
echo $?

# Run 2: Choice 0 (Abort -> Failure)
./bin/task5
echo $?
```

![Task 5 - Control Flow and Exit](assets/screenshots/05_task5_conditional_flow_exit.png)

* **Key Observation**: Each invocation receives a brand new, unique PID from the OS kernel, proving process creation and destruction lifecycle.

---

## 🛠️ Building & Running

### Using GNU Make
```bash
make all        # Compile all 5 task binaries into bin/
make clean      # Clean build artifacts
```

### Automated Live Verification Script
Run all 5 tasks sequentially with automated inputs and visual diagnostics:
```bash
chmod +x scripts/run_all.sh
./scripts/run_all.sh
```

---

## 📚 Technical Documentation Directory
- [Comprehensive Lab 3 Technical Report](Lab3_Process_Lifecycles_Documentation.md)
- [Theory 1: Process Concept & Virtual Memory Segments](docs/01_theory_process_layout.md)
- [Theory 2: How the OS Loads and Executes Programs (`fork` + `execve`)](docs/02_os_loading_and_execution.md)
- [Theory 3: Process Lifecycle, Termination, and Kernel Cleanup](docs/03_process_lifecycle_and_termination.md)
- [Lecture 2 Knowledge Assessment: All 15 Questions & Answers](docs/04_knowledge_test_qa.md)

---

## 📄 License
Distributed under the [MIT License](LICENSE).
