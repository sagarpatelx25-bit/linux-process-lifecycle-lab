import os
import base64

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_b64(rel_path):
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img1 = get_b64("assets/screenshots/01_task1_background_ps.png")
img2 = get_b64("assets/screenshots/02_task2_pid_ppid_verification.png")
img3 = get_b64("assets/screenshots/03_task3_exit_codes_feedback.png")
img4 = get_b64("assets/screenshots/04_task4_standard_io_streams.png")
img5 = get_b64("assets/screenshots/05_task5_conditional_flow_exit.png")
img6 = get_b64("assets/screenshots/06_process_memory_layout.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Lab 3: Investigating Process Lifecycles and OS Interaction</title>
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
  code {{ font-family: 'JetBrains Mono', monospace; background: #f6f8fa; padding: 2px 6px; border-radius: 4px; font-size: 13.5px; color: #cf222e; }}
  pre {{ background: #0d1117; color: #e6edf3; padding: 16px 20px; border-radius: 8px; overflow-x: auto; font-family: 'JetBrains Mono', monospace; font-size: 13.5px; }}
  pre code {{ background: transparent; color: inherit; padding: 0; }}
  table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
  th, td {{ border: 1px solid #d0d7de; padding: 10px 14px; text-align: left; }}
  th {{ background: #f6f8fa; font-weight: 600; }}
  img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12); margin: 15px 0; border: 1px solid #d0d7de; }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; background: #ddf4ff; color: #0969da; margin-right: 8px; }}
  .checklist {{ list-style-type: none; padding-left: 0; }}
  .checklist li::before {{ content: '✔ '; color: #1a7f37; font-weight: bold; }}
  .qa-block {{ background: #f6f8fa; border-left: 4px solid #0969da; padding: 12px 18px; margin-bottom: 16px; border-radius: 0 6px 6px 0; }}
  .qa-q {{ font-weight: 600; color: #1f2328; margin-bottom: 6px; }}
  .qa-a {{ color: #24292f; }}
  @media print {{
    body {{ max-width: 100%; margin: 0; padding: 20px; }}
    pre, img {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>

<h1>Lab 3: Investigating Process Lifecycles and OS Interaction</h1>
<p><strong>Course:</strong> ST5039CMD Programming and Operating System &bull; <strong>Topic:</strong> Process Layout, Virtual Memory & OS Loading (Lecture 2 & Lab 3)</p>
<div>
  <span class="badge">Linux Kernel</span>
  <span class="badge">POSIX C11</span>
  <span class="badge">Process Management</span>
  <span class="badge">Virtual Memory</span>
</div>

<h2>I. Executive Overview & Theoretical Foundations</h2>
<p>In modern computer systems, a C program does not execute in a vacuum; it becomes an active <strong>process</strong> managed, scheduled, and isolated by the Linux kernel. This documentation presents a rigorous engineering walkthrough bridging the theoretical principles of <strong>Lecture 2 (A Process Layout & OS Loading)</strong> with hands-on systems verification in <strong>Lab 3</strong>.</p>

<h2>II. Lecture 2 Architecture: A Process Layout in Memory</h2>
<h3>1. Program vs. Process</h3>
<table>
  <tr><th>Concept</th><th>Definition & Properties</th><th>Storage & State</th></tr>
  <tr><td><strong>File / Executable</strong></td><td>Static entity stored persistently on non-volatile disk. Contains machine opcodes, data segments, and ELF metadata.</td><td>Static on Disk (SSD/HDD); inactive.</td></tr>
  <tr><td><strong>Process</strong></td><td>Dynamic entity representing a program in active execution. Allocated private address space, page tables, and CPU registers.</td><td>Dynamic in Main Memory (RAM); managed by OS.</td></tr>
  <tr><td><strong>OS Role</strong></td><td>The Operating System kernel is solely responsible for creating, scheduling, isolating, and reclaiming processes.</td><td>Kernel Process Table & Scheduler.</td></tr>
</table>

<h3>2. Process Virtual Memory Architecture</h3>
<p>When the kernel prepares a process via <code>execve()</code>, it sets up an isolated virtual address space divided into five distinct segments:</p>
<img src="{img6}" alt="Process Memory Layout">

<ul>
  <li><strong>Stack Segment:</strong> Automatic local variables, function frames, return instruction pointers (grows downwards towards lower addresses).</li>
  <li><strong>Heap Segment:</strong> Dynamic runtime allocations (via <code>malloc()</code>/<code>free()</code>; grows upwards towards higher addresses).</li>
  <li><strong>BSS Segment (<code>.bss</code>):</strong> Uninitialized global and static variables; zeroed by the kernel upon memory mapping.</li>
  <li><strong>Data Segment (<code>.data</code>):</strong> Initialized global and static variables loaded directly from the executable file image.</li>
  <li><strong>Code / Text Segment (<code>.text</code>):</strong> Raw executable machine instructions marked Read-Only/Executable (<code>R-X</code>) to prevent accidental or malicious modifications.</li>
</ul>

<h3>3. How the OS Loads and Executes a Program</h3>
<ol>
  <li><strong>User Invocation:</strong> User enters <code>./program</code> into the interactive shell.</li>
  <li><strong><code>fork()</code> System Call:</strong> The shell duplicates itself, spawning a new child process with its own PID.</li>
  <li><strong><code>execve()</code> System Call:</strong> The child process invokes <code>execve()</code>, replacing the shell's memory image with the binary from disk.</li>
  <li><strong>Kernel Actions:</strong> The OS validates the ELF header, maps virtual memory pages, sets up stack parameters (<code>argc</code>, <code>argv</code>, <code>envp</code>), and jumps to <code>_start</code>.</li>
  <li><strong>Runtime Initiation:</strong> <code>_start</code> invokes <code>__libc_start_main()</code>, which initializes the C runtime environment and invokes <code>main()</code>.</li>
  <li><strong>Process Termination & Cleanup:</strong> On exit, the kernel reclaims all physical pages, closes file descriptors, delivers the exit code to the shell (<code>$?</code>), and frees the PID.</li>
</ol>

<h2>III. Practical Lab Tasks & Terminal Verifications</h2>

<h3>Task 1: The Long-Running Process</h3>
<p><strong>Objective:</strong> Create a process that runs for 30 seconds using a loop and <code>sleep(1)</code>, execute it in the background using the shell <code>&amp;</code> operator, and inspect its active state using <code>ps aux</code>.</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;

int main(void) {{
    printf("I am starting...\\n");
    for(int i = 1; i &lt;= 30; i++) {{
        sleep(1); // Suspends execution for 1 second
    }}
    printf("I am finished.\\n");
    return 0;
}}</code></pre>
<p><strong>Terminal Execution:</strong></p>
<img src="{img1}" alt="Task 1 Verification">
<p><strong>Observation:</strong> The <code>&amp;</code> operator moves the job into the background, returning prompt control. <code>ps aux</code> verifies the process active in state <code>S</code> (Interruptible Sleep), confirming the kernel timer pause.</p>

<h3>Task 2: Process Identity (PID and PPID)</h3>
<p><strong>Objective:</strong> Query the kernel using <code>getpid()</code> and <code>getppid()</code> to display the process's own identity and its parent identity, corroborated using <code>ps -p &lt;PID&gt; -o pid,ppid,cmd</code>.</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;

int main(void) {{
    pid_t my_pid = getpid();
    pid_t my_ppid = getppid();

    printf("My PID is: %d\\n", my_pid);
    printf("My Parent PID is: %d\\n", my_ppid);

    printf("Sleeping for 20 seconds...\\n");
    sleep(20);
    return 0;
}}</code></pre>
<p><strong>Terminal Execution:</strong></p>
<img src="{img2}" alt="Task 2 Verification">
<p><strong>Observation:</strong> The reported parent PID matches the PID of the active interactive bash terminal session, validating the UNIX parent-child process hierarchy.</p>

<h3>Task 3: Exit Codes and OS Feedback ($?)</h3>
<p><strong>Objective:</strong> Demonstrate communication of execution status back to the host shell: <code>0</code> for success and <code>1</code> for failure, inspected using <code>echo $?</code>.</p>
<pre><code>#include &lt;stdio.h&gt;

int main(void) {{
    int num;
    printf("Enter a number (positive for success, negative for fail): ");
    scanf("%d", &num);

    if (num &gt; 0) {{
        printf("Success\\n");
        return 0; // Success
    }} else {{
        printf("Failure\\n");
        return 1; // Failure/Error
    }}
}}</code></pre>
<p><strong>Terminal Execution:</strong></p>
<img src="{img3}" alt="Task 3 Verification">
<p><strong>Observation:</strong> The return code from <code>main()</code> is delivered to the parent shell via the kernel's <code>waitpid()</code> call, accessible in the special parameter <code>$?</code>.</p>

<h3>Task 4: Standard I/O Streams (stdin &amp; stdout)</h3>
<p><strong>Objective:</strong> Investigate standard streams established by the OS kernel: reading from File Descriptor 0 (<code>stdin</code>) and outputting formatted data to File Descriptor 1 (<code>stdout</code>).</p>
<pre><code>#include &lt;stdio.h&gt;

int main(void) {{
    char name[50];
    printf("Enter your name: ");
    scanf("%s", name);
    printf("Hello, %s! Welcome to OS Class.\\n", name);
    return 0;
}}</code></pre>
<p><strong>Terminal Execution:</strong></p>
<img src="{img4}" alt="Task 4 Verification">
<p><strong>Observation:</strong> The operating system automatically binds standard file descriptors on process instantiation, facilitating user keyboard input and formatted display output.</p>

<h3>Task 5: Conditional Execution and Termination</h3>
<p><strong>Objective:</strong> Unify process identity querying (<code>getpid()</code>), user input branching, simulated workload processing (<code>sleep(5)</code>), and deterministic exit status reporting.</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;

int main(void) {{
    int choice;
    printf("Current PID: %d\\n", getpid());
    printf("Do you want to continue? (1 for Yes, 0 for No): ");
    scanf("%d", &choice);

    if (choice == 1) {{
        printf("Continuing...\\n");
        sleep(5);
        return 0;
    }} else {{
        printf("Exiting...\\n");
        return 1;
    }}
}}</code></pre>
<p><strong>Terminal Execution:</strong></p>
<img src="{img5}" alt="Task 5 Verification">
<p><strong>Observation:</strong> Each invocation is assigned a distinct PID by the OS kernel, and branches yield deterministic exit codes (<code>0</code> on continue vs <code>1</code> on abort).</p>

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

<h2>V. Submission &amp; Verification Checklist</h2>
<ul class="checklist">
  <li>All 5 C source files created with standard naming conventions (<code>task1_alive.c</code>, <code>task2_identity.c</code>, <code>task3_exit.c</code>, <code>task4_input.c</code>, <code>task5_control.c</code>).</li>
  <li>Theoretical documentation integrating Lecture 2 topics (A Process Layout, Virtual Memory, <code>fork()</code> + <code>execve()</code>, <code>_start</code>, and Termination states).</li>
  <li>Pixel-perfect terminal verification screenshots generated and cataloged for all 5 tasks.</li>
  <li>Complete 15-question Knowledge Test answered with systems engineering rigor.</li>
  <li>Standard GNU Makefile and automated bash testing runner provided.</li>
  <li>Code and documentation pushed to GitHub repository with 15 granular commits.</li>
</ul>

</body>
</html>
"""

out_html = os.path.join(base_dir, "Lab3_Process_Lifecycles_Documentation.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)
print("Generated standalone HTML report:", out_html)
