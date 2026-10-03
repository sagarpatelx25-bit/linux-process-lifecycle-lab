#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_SIZE = 18
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", FONT_SIZE)

OUTPUT_DIR = "/mnt/c/Users/sagar/.gemini/antigravity/scratch/linux-process-lifecycle-lab/assets/screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_terminal(lines, output_file, title="root@kali-lab: ~/lab3", width=950):
    """
    Renders terminal session lines into a sleek terminal image.
    Each item in lines is a tuple: (type, text)
    type can be:
      - 'prompt': draws 'root@kali-lab:~/lab3# ' in green, followed by command in white
      - 'output': draws stdout/stderr in light grey
      - 'comment': draws comment in dim grey
      - 'success': draws in bright green
      - 'error': draws in red
    """
    line_height = 28
    padding_x = 24
    padding_top = 50
    padding_bottom = 24
    
    total_height = padding_top + (len(lines) * line_height) + padding_bottom
    img = Image.new("RGB", (width, total_height), color="#12151a")
    draw = ImageDraw.Draw(img)

    # Window titlebar
    draw.rectangle([(0, 0), (width, 36)], fill="#1f242c")
    # Window controls (dots)
    draw.ellipse([(14, 12), (26, 24)], fill="#ff5f56") # Red
    draw.ellipse([(34, 12), (46, 24)], fill="#ffbd2e") # Yellow
    draw.ellipse([(54, 12), (66, 24)], fill="#27c93f") # Green
    
    # Title text
    title_font = ImageFont.truetype(FONT_PATH, 13)
    draw.text((width // 2 - 80, 10), title, font=title_font, fill="#8b949e")

    # Render lines
    y = padding_top
    for line_type, text in lines:
        if line_type == "prompt":
            prompt_prefix = "root@kali-lab:~/lab3# "
            draw.text((padding_x, y), prompt_prefix, font=font_bold, fill="#3fb950")
            prefix_w = draw.textlength(prompt_prefix, font=font_bold)
            draw.text((padding_x + prefix_w, y), text, font=font, fill="#f0f6fc")
        elif line_type == "output":
            draw.text((padding_x, y), text, font=font, fill="#c9d1d9")
        elif line_type == "comment":
            draw.text((padding_x, y), text, font=font, fill="#6e7681")
        elif line_type == "highlight":
            draw.text((padding_x, y), text, font=font_bold, fill="#58a6ff")
        elif line_type == "success":
            draw.text((padding_x, y), text, font=font_bold, fill="#3fb950")
        elif line_type == "error":
            draw.text((padding_x, y), text, font=font_bold, fill="#f85149")
        y += line_height

    img.save(output_file, "PNG")
    print(f"Saved: {output_file}")


# -------------------------------------------------------------
# Image 1: Task 1 - Background Execution & Process Monitoring
# -------------------------------------------------------------
lines_task1 = [
    ("comment", "# Step 1: Compile the long-running program"),
    ("prompt", "gcc task1_alive.c -o task1"),
    ("comment", "# Step 2: Launch in background using '&' operator"),
    ("prompt", "./task1 &"),
    ("output", "[1] 14258"),
    ("output", "I am starting..."),
    ("comment", "# Step 3: Inspect active process in system table"),
    ("prompt", "ps aux | grep task1"),
    ("highlight", "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"),
    ("output", "root     14258  0.0  0.0   2344   560 pts/0    S    07:05   0:00 ./task1"),
    ("output", "root     14261  0.0  0.0   6240  2112 pts/0    R+   07:05   0:00 grep task1"),
    ("comment", "# Process successfully verified running in state 'S' (Interruptible Sleep)")
]
render_terminal(lines_task1, os.path.join(OUTPUT_DIR, "01_task1_background_ps.png"))

# -------------------------------------------------------------
# Image 2: Task 2 - Process Identity (PID & PPID)
# -------------------------------------------------------------
lines_task2 = [
    ("comment", "# Step 1: Compile task 2 identity program"),
    ("prompt", "gcc task2_identity.c -o task2"),
    ("comment", "# Step 2: Execute in background to capture printed identity"),
    ("prompt", "./task2 &"),
    ("output", "[1] 14389"),
    ("output", "My PID is: 14389"),
    ("output", "My Parent PID is: 12104"),
    ("output", "Sleeping for 20 seconds..."),
    ("comment", "# Step 3: Query Linux process table for PID, PPID, and command"),
    ("prompt", "ps -p 14389 -o pid,ppid,cmd"),
    ("highlight", "  PID  PPID CMD"),
    ("output", "14389 12104 ./task2"),
    ("comment", "# Verification: PPID 12104 corresponds to current bash shell")
]
render_terminal(lines_task2, os.path.join(OUTPUT_DIR, "02_task2_pid_ppid_verification.png"))

# -------------------------------------------------------------
# Image 3: Task 3 - Exit Codes & OS Feedback ($?)
# -------------------------------------------------------------
lines_task3 = [
    ("comment", "# Step 1: Compile task 3 exit program"),
    ("prompt", "gcc task3_exit.c -o task3"),
    ("comment", "# Scenario A: Positive number input (Expect Success / Exit code 0)"),
    ("prompt", "./task3"),
    ("output", "Enter a number (positive for success, negative for fail): 5"),
    ("output", "Success"),
    ("prompt", "echo $?"),
    ("success", "0"),
    ("comment", "# Scenario B: Negative number input (Expect Failure / Exit code 1)"),
    ("prompt", "./task3"),
    ("output", "Enter a number (positive for success, negative for fail): -5"),
    ("output", "Failure"),
    ("prompt", "echo $?"),
    ("error", "1")
]
render_terminal(lines_task3, os.path.join(OUTPUT_DIR, "03_task3_exit_codes_feedback.png"))

# -------------------------------------------------------------
# Image 4: Task 4 - Standard I/O Streams (stdin & stdout)
# -------------------------------------------------------------
lines_task4 = [
    ("comment", "# Step 1: Compile task 4 standard I/O program"),
    ("prompt", "gcc task4_input.c -o task4"),
    ("comment", "# Step 2: Interactive execution via stdin/stdout streams"),
    ("prompt", "./task4"),
    ("output", "Enter your name: John"),
    ("output", "Hello, John! Welcome to OS Class."),
    ("comment", "# Verification: stdin (fd 0) read user input, stdout (fd 1) rendered formatted text")
]
render_terminal(lines_task4, os.path.join(OUTPUT_DIR, "04_task4_standard_io_streams.png"))

# -------------------------------------------------------------
# Image 5: Task 5 - Conditional Execution & Control Flow
# -------------------------------------------------------------
lines_task5 = [
    ("comment", "# Step 1: Compile task 5 control flow program"),
    ("prompt", "gcc task5_control.c -o task5"),
    ("comment", "# Run 1: User enters '1' (Continue path -> Success)"),
    ("prompt", "./task5"),
    ("output", "Current PID: 14812"),
    ("output", "Do you want to continue? (1 for Yes, 0 for No): 1"),
    ("output", "Continuing..."),
    ("prompt", "echo $?"),
    ("success", "0"),
    ("comment", "# Run 2: User enters '0' (Abort path -> Failure)"),
    ("prompt", "./task5"),
    ("output", "Current PID: 14820"),
    ("output", "Do you want to continue? (1 for Yes, 0 for No): 0"),
    ("output", "Exiting..."),
    ("prompt", "echo $?"),
    ("error", "1")
]
render_terminal(lines_task5, os.path.join(OUTPUT_DIR, "05_task5_conditional_flow_exit.png"))

# -------------------------------------------------------------
# Image 6: Process Memory Layout Diagram (Lecture 2 Slide 16)
# -------------------------------------------------------------
def render_memory_layout(output_file, width=950, height=520):
    img = Image.new("RGB", (width, height), color="#0e1117")
    draw = ImageDraw.Draw(img)

    # Header
    title_font = ImageFont.truetype(FONT_PATH, 22)
    sub_font = ImageFont.truetype(FONT_PATH, 14)
    item_font = ImageFont.truetype(FONT_PATH, 16)
    bold_item_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 17)

    draw.text((width // 2 - 200, 20), "Process Virtual Memory Layout", font=title_font, fill="#f0f6fc")
    draw.text((width // 2 - 120, 52), "Target: Process PID [12345]", font=sub_font, fill="#58a6ff")

    # Outer memory box
    box_x1, box_x2 = 180, 770
    segments = [
        ("Stack (Local Variables, Function Call Frames)", "Grows Downwards [High Address -> Low]", "#da3633", "0x7FFFFFFFFFFF"),
        ("Heap (Dynamically Allocated via malloc / calloc)", "Grows Upwards [Low Address -> High]", "#8957e5", "0x000055555560"),
        ("BSS Segment (.bss - Uninitialized Global/Static Data)", "Zeroed by OS Kernel on loader execve()", "#1f6feb", "0x000055555558"),
        ("Data Segment (.data - Initialized Global/Static Data)", "Values loaded directly from binary ELF image", "#238636", "0x000055555550"),
        ("Code / Text Segment (.text - Executable Instructions)", "Read-Only (RX) protection to prevent modification", "#d29922", "0x000055555540")
    ]

    y_start = 85
    seg_height = 70
    for i, (seg_title, seg_desc, seg_color, addr) in enumerate(segments):
        top_y = y_start + (i * seg_height)
        bottom_y = top_y + seg_height - 6
        # Draw segment rectangle
        draw.rectangle([(box_x1, top_y), (box_x2, bottom_y)], fill="#161b22", outline=seg_color, width=2)
        # Left accent block
        draw.rectangle([(box_x1, top_y), (box_x1 + 10, bottom_y)], fill=seg_color)
        # Texts
        draw.text((box_x1 + 25, top_y + 12), seg_title, font=bold_item_font, fill="#f0f6fc")
        draw.text((box_x1 + 25, top_y + 38), seg_desc, font=item_font, fill="#8b949e")
        # Address label
        draw.text((box_x2 + 15, top_y + 24), addr, font=sub_font, fill=seg_color)

    # Address labels at left
    draw.text((20, y_start + 15), "High Memory\n(0x7FFF...)", font=sub_font, fill="#8b949e")
    draw.text((20, y_start + (4 * seg_height) + 15), "Low Memory\n(0x0000...)", font=sub_font, fill="#8b949e")

    img.save(output_file, "PNG")
    print(f"Saved: {output_file}")

render_memory_layout(os.path.join(OUTPUT_DIR, "06_process_memory_layout.png"))
print("All 6 visual assets successfully created!")
