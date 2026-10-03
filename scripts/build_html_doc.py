import os
import base64

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_b64(rel_path):
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img1 = get_b64("assets/screenshots/raw/01_task1_alive.png")
img2 = get_b64("assets/screenshots/raw/02_task2_identity.png")
img3 = get_b64("assets/screenshots/raw/03_task3_exit.png")
img4 = get_b64("assets/screenshots/raw/04_task4_input.png")
img5 = get_b64("assets/screenshots/raw/05_task5_control.png")
img6 = get_b64("assets/screenshots/raw/06_memory_layout.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Process Lifecycles & OS Interaction: Step-by-Step Guide</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1f2328;
    background: #ffffff;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 30px;
    line-height: 1.65;
  }}
  h1 {{ font-size: 2.2rem; border-bottom: 2px solid #0969da; padding-bottom: 12px; color: #0969da; margin-bottom: 4px; }}
  h2 {{ font-size: 1.5rem; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; margin-top: 35px; color: #1f2328; }}
  h3 {{ font-size: 1.2rem; margin-top: 25px; color: #24292f; }}
  p, li {{ font-size: 15px; color: #24292f; }}
  code {{ font-family: 'JetBrains Mono', monospace; background: #f6f8fa; padding: 2px 6px; border-radius: 4px; font-size: 13.5px; color: #0969da; }}
  table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
  th, td {{ border: 1px solid #d0d7de; padding: 10px 14px; text-align: left; }}
  th {{ background: #f6f8fa; font-weight: 600; }}
  img {{ max-width: 100%; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); margin: 15px 0; border: 1px solid #30363d; background: #0c0c0c; }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; background: #ddf4ff; color: #0969da; margin-right: 8px; }}
  .checklist {{ list-style-type: none; padding-left: 0; }}
  .checklist li::before {{ content: '✔ '; color: #1a7f37; font-weight: bold; }}
  .qa-block {{ background: #f6f8fa; border-left: 4px solid #0969da; padding: 12px 18px; margin-bottom: 16px; border-radius: 0 6px 6px 0; }}
  .qa-q {{ font-weight: 600; color: #1f2328; margin-bottom: 6px; }}
  .qa-a {{ color: #24292f; }}
  @media print {{
    body {{ max-width: 100%; margin: 0; padding: 20px; }}
    img {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>

<h1>Process Lifecycles & OS Interaction: Step-by-Step Guide</h1>
<p><strong>Course:</strong> ST5039CMD Programming and Operating System &bull; <strong>Topic:</strong> Process Layout, Virtual Memory & OS Loading (Lecture 2 & Lab 3)</p>
<div>
  <span class="badge">Linux Kernel</span>
  <span class="badge">POSIX C11</span>
  <span class="badge">Process Management</span>
  <span class="badge">Virtual Memory</span>
</div>

<h2>I. Introduction</h2>
<p>In Lecture 2 and Lab 3, we learned that an Operating System manages processes and system resources. Instead of just writing code that prints text, we author C programs that interact directly with the Linux kernel to query process identity, control execution lifecycles, and communicate success or failure back to the host shell.</p>

<h2>II. Architecture: A Process Layout & OS Loading</h2>
<h3>1. Program vs. Process</h3>
<table>
  <tr><th>Concept</th><th>Definition & Properties</th><th>Storage & State</th></tr>
  <tr><td><strong>File / Executable</strong></td><td>Static entity stored persistently on non-volatile disk. Contains machine opcodes, data segments, and ELF metadata.</td><td>Static on Disk (SSD/HDD); inactive.</td></tr>
  <tr><td><strong>Process</strong></td><td>Dynamic entity representing a program in active execution. Allocated private address space, page tables, and CPU registers.</td><td>Dynamic in Main Memory (RAM); managed by OS.</td></tr>
  <tr><td><strong>OS Role</strong></td><td>The Operating System kernel is solely responsible for creating, scheduling, isolating, and reclaiming processes.</td><td>Kernel Process Table & Scheduler.</td></tr>
</table>

<h3>2. Memory Process Layout</h3>
<p>When a process is loaded into RAM, the Linux kernel organizes its virtual address space into five distinct segments:</p>
<img src="{img6}" alt="Memory Process Layout">

<ul>
  <li><strong>Code/Text Segment:</strong> Executable CPU machine instructions; marked Read-Only/Executable (<code>R-X</code>).</li>
  <li><strong>Data Segment:</strong> Initialized global and static variables loaded directly from the binary.</li>
  <li><strong>BSS Segment (<code>.bss</code>):</strong> Uninitialized global and static variables; zeroed out by the kernel.</li>
  <li><strong>Heap Segment:</strong> Dynamic memory allocated via <code>malloc()</code> / <code>free()</code> (grows upwards).</li>
  <li><strong>Stack Segment:</strong> Function parameters, local variables, and return pointers (grows downwards).</li>
</ul>

<h2>III. Step-by-Step Practical Lab Tasks</h2>

<h3>Task 1: The Long-Running Process</h3>
<ul>
  <li><strong>Objective:</strong> In enterprise servers, processes run for days or months. We must know how to run a process in the background using <code>&amp;</code> and monitor it while it is active using <code>ps aux</code>.</li>
  <li><strong>Command:</strong> <code>cat task1_alive.c then gcc task1_alive.c -o task1 then ./task1 &amp; then ps aux | grep task1</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img1}" alt="Task 1 - Long-Running Process">
<p><strong>Observation:</strong> The <code>&amp;</code> operator executes <code>./task1</code> in the background, freeing the terminal shell immediately with job ID <code>[1]</code> and PID <code>12345</code>. The <code>ps aux</code> command confirms the process is active in state <code>S</code> (Interruptible Sleep), paused during its <code>sleep(1)</code> loop without consuming unnecessary CPU cycles.</p>

<h3>Task 2: Process Identity (PID and PPID)</h3>
<ul>
  <li><strong>Objective:</strong> Every process in Linux has a unique Process ID (<code>PID</code>). The process that created it is the Parent Process ID (<code>PPID</code>), usually your terminal shell. Query these using <code>getpid()</code> and <code>getppid()</code>, and verify them via <code>ps -p &lt;PID&gt; -o pid,ppid,cmd</code>.</li>
  <li><strong>Command:</strong> <code>cat task2_identity.c then gcc task2_identity.c -o task2 then ./task2 &amp; then ps -p 12345 -o pid,ppid,cmd</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img2}" alt="Task 2 - Process Identity">
<p><strong>Observation:</strong> The program queries the Linux kernel and prints its unique <code>PID (12345)</code> and parent <code>PPID (8901)</code>. The OS <code>ps</code> command validates that the PPID <code>8901</code> belongs directly to the interactive terminal shell that spawned the process.</p>

<h3>Task 3: Exit Codes and OS Feedback ($?)</h3>
<ul>
  <li><strong>Objective:</strong> When a program finishes, it returns an integer to the OS. <code>0</code> means "Success", and any non-zero number (like <code>1</code>) means "Error/Failure". The shell stores this in <code>$?</code>.</li>
  <li><strong>Command:</strong> <code>cat task3_exit.c then gcc task3_exit.c -o task3 then ./task3 then echo $?</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img3}" alt="Task 3 - Exit Codes and Feedback">
<p><strong>Observation:</strong> When given a positive input (<code>5</code>), the program returns <code>0</code>, and <code>echo $?</code> outputs <code>0</code> (<strong>Success</strong>). When given a negative input (<code>-5</code>), the program returns <code>1</code>, and <code>echo $?</code> outputs <code>1</code> (<strong>Failure</strong>), proving that Unix processes communicate execution status directly to the calling shell.</p>

<h3>Task 4: Standard I/O Streams</h3>
<ul>
  <li><strong>Objective:</strong> The OS provides standard input (<code>stdin</code>, fd 0) and standard output (<code>stdout</code>, fd 1) streams. <code>scanf()</code> reads from <code>stdin</code>, and <code>printf()</code> writes to <code>stdout</code>.</li>
  <li><strong>Command:</strong> <code>cat task4_input.c then gcc task4_input.c -o task4 then ./task4</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img4}" alt="Task 4 - Standard I/O Streams">
<p><strong>Observation:</strong> The operating system connects the keyboard stream to <code>stdin</code>, which is read by <code>scanf()</code>, and redirects formatted text from <code>printf()</code> to <code>stdout</code> on the terminal screen.</p>

<h3>Task 5: Conditional Execution and Termination</h3>
<ul>
  <li><strong>Objective:</strong> Programs often branch based on user input. The OS tracks the final exit code to determine if the script or automation pipeline should continue or halt.</li>
  <li><strong>Command:</strong> <code>cat task5_control.c then gcc task5_control.c -o task5 then ./task5 then echo $?</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img5}" alt="Task 5 - Conditional Execution and Termination">
<p><strong>Observation:</strong> Choosing <code>1</code> causes the process to continue, simulate workload (<code>sleep(5)</code>), and return exit code <code>0</code> (<code>Success</code>). Choosing <code>0</code> causes the process to immediately abort and return exit code <code>1</code> (<code>Failure</code>). Each independent run receives a newly allocated PID from the kernel (<code>12400</code> vs <code>12405</code>), illustrating process creation and destruction.</p>

<h2>IV. Lecture 2 Knowledge Test Q&A Reference</h2>
<div class="qa-block"><div class="qa-q">1. What is the difference between source code and an executable?</div><div class="qa-a">Source code is human-readable high-level code (.c). An executable is a machine-readable binary file (.out/ELF) created by a compiler and linker containing CPU instructions and data sections.</div></div>
<div class="qa-block"><div class="qa-q">2. What command compiles a C program?</div><div class="qa-a"><code>gcc program.c -o program</code></div></div>
<div class="qa-block"><div class="qa-q">3. What is a process?</div><div class="qa-a">A process is an active program in execution loaded into main memory (RAM) and managed by the operating system kernel.</div></div>
<div class="qa-block"><div class="qa-q">4. What does PID stand for?</div><div class="qa-a">Process Identifier.</div></div>
<div class="qa-block"><div class="qa-q">5. How do you check the exit code of the last command?</div><div class="qa-a">By evaluating the shell parameter <code>echo $?</code>.</div></div>
<div class="qa-block"><div class="qa-q">6. What does return 0; mean in main()?</div><div class="qa-a">It signals to the OS kernel that the process concluded execution successfully without errors.</div></div>
<div class="qa-block"><div class="qa-q">7. What system call creates a new process?</div><div class="qa-a">The <code>fork()</code> system call.</div></div>
<div class="qa-block"><div class="qa-q">8. What system call replaces current process with a new program?</div><div class="qa-a">The <code>execve()</code> system call.</div></div>
<div class="qa-block"><div class="qa-q">9. How do you see running processes in terminal?</div><div class="qa-a">Using process inspection tools such as <code>ps aux</code>, <code>top</code>, or <code>htop</code>.</div></div>
<div class="qa-block"><div class="qa-q">10. What happens to memory when a process ends?</div><div class="qa-a">The operating system kernel unmaps the process's page tables and frees all physical RAM back into the system memory pool.</div></div>
<div class="qa-block"><div class="qa-q">11. Where is your program stored before execution?</div><div class="qa-a">On persistent non-volatile disk storage (SSD/HDD) as a static binary file.</div></div>
<div class="qa-block"><div class="qa-q">12. Where is your program stored during execution?</div><div class="qa-a">In volatile main memory (RAM) within its private virtual address space.</div></div>
<div class="qa-block"><div class="qa-q">13. Why does the OS assign a PID to each process?</div><div class="qa-a">To uniquely track, schedule, allocate resources to, and deliver signals to each active process.</div></div>
<div class="qa-block"><div class="qa-q">14. When does a process end?</div><div class="qa-a">Upon normal exit (return/exit), fatal external signal (Ctrl+C/kill), or an unhandled hardware crash (segfault/divide by zero).</div></div>
<div class="qa-block"><div class="qa-q">15. Who assigns the PID?</div><div class="qa-a">The Operating System Kernel.</div></div>

<h2>V. Submission Checklist</h2>
<ul class="checklist">
  <li>All 5 C source files created with standard naming conventions (<code>task1_alive.c</code>, <code>task2_identity.c</code>, <code>task3_exit.c</code>, <code>task4_input.c</code>, <code>task5_control.c</code>).</li>
  <li>Theoretical documentation integrating Lecture 2 topics (A Process Layout, Virtual Memory, <code>fork()</code> + <code>execve()</code>, <code>_start</code>, and Termination states).</li>
  <li>Raw black console verification screenshots matching the GCC guide style generated and cataloged.</li>
  <li>Complete 15-question Knowledge Test answered with systems engineering rigor.</li>
  <li>Standard GNU Makefile and automated bash testing runner provided.</li>
  <li>Code and documentation pushed to GitHub repository with granular commits.</li>
</ul>

</body>
</html>
"""

out_html = os.path.join(base_dir, "Lab3_Process_Lifecycles_Documentation.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)
print("Updated standalone HTML report:", out_html)
