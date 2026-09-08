import sys
import time
from datetime import datetime

from colorama import Fore, Style, init

init(autoreset=True)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class C:
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    MAGENTA = Fore.MAGENTA
    BLUE = Fore.BLUE
    WHITE = Fore.WHITE
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    R = Style.RESET_ALL


def section(title):
    print("\n" + C.BLUE + C.BOLD + "╔" + "═" * 76 + "╗")
    print("║ " + title.ljust(75) + "║")
    print("╚" + "═" * 76 + "╝" + Style.RESET_ALL)


def step(index, total, label):
    print("\n" + C.YELLOW + C.BOLD + f" [{index}/{total}] {label}" + C.R + " ...")


def ok(msg):
    print(C.GREEN + "  OK " + msg + C.R)


def fail(msg):
    print(C.RED + "  FAIL " + msg + C.R)


def warn(msg):
    print(C.YELLOW + "  WARN " + msg + C.R)


def info(msg):
    print(C.CYAN + "  - " + msg + C.R)


def status_badge(status):
    if status == "PASS":
        return C.GREEN + "[PASS]" + C.R
    if status == "FAIL":
        return C.RED + "[FAIL]" + C.R
    if status == "SKIP":
        return C.YELLOW + "[SKIP]" + C.R
    return C.DIM + "[?] " + C.R


def spinner(message, duration=1.0):
    frames = ["|", "/", "-", "\\"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write("\r" + C.CYAN + f" {frames[i % len(frames)]} {message}..." + C.R)
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 12) + "\r")
    sys.stdout.flush()


def progress_bar(done, total, width=30):
    pct = done / total if total else 0
    filled = int(width * pct)
    bar = "#" * filled + "." * (width - filled)
    return f"[{bar}] {done}/{total} ({pct * 100:.0f}%)"


def ask_choice(prompt, options, allow_index=True):
    while True:
        print(C.WHITE + prompt)
        for key, (label, _desc) in options.items():
            print(f"    {C.MAGENTA + C.BOLD}[{key}]{C.R}  {C.WHITE}{label}{C.R}")
        try:
            choice = input("\n  " + C.BOLD + "> Enter your choice: " + C.R).strip().lower()
        except EOFError:
            return None
        if choice in options:
            return choice
        fail("Invalid choice, please try again.")


def press_enter():
    try:
        input("\n  " + C.DIM + "Press Enter to continue..." + C.R)
    except EOFError:
        pass


def timestamp():
    return datetime.now().strftime("%H:%M:%S")
