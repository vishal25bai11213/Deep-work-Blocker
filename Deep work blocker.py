"""
deep_work_blocker.py
────────────────────
A terminal-based Pomodoro + website blocker.
Run with sudo/admin privileges so it can edit the hosts file.

Usage:
  sudo python3 deep_work_blocker.py          # Linux / macOS
  python deep_work_blocker.py  (as Admin)    # Windows
"""

import time
import os
import sys
import platform
from datetime import datetime

# ──────────────────────────────────────────────────────────
# CONFIGURATION — edit these freely
# ──────────────────────────────────────────────────────────

FOCUS_MINUTES = 25
SHORT_BREAK   = 5
LONG_BREAK    = 15
CYCLES_BEFORE_LONG_BREAK = 4   # how many focus sessions before a long break

BLOCKED_SITES = [
    "youtube.com",    "www.youtube.com",
    "reddit.com",     "www.reddit.com",
    "instagram.com",  "www.instagram.com",
    "twitter.com",    "www.twitter.com",
    "x.com",          "www.x.com",
    "facebook.com",   "www.facebook.com",
    "tiktok.com",     "www.tiktok.com",
    "netflix.com",    "www.netflix.com",
    "twitch.tv",      "www.twitch.tv",
    "discord.com",    "www.discord.com",
    "9gag.com",       "www.9gag.com",
]

STUDY_TOPICS = [
    {"name": "Data Structures",      "exam_date": "2025-07-10", "difficulty": 3, "hours_needed": 6},
    {"name": "Algorithms",           "exam_date": "2025-07-10", "difficulty": 4, "hours_needed": 8},
    {"name": "Operating Systems",    "exam_date": "2025-07-14", "difficulty": 3, "hours_needed": 5},
    {"name": "Computer Networks",    "exam_date": "2025-07-14", "difficulty": 3, "hours_needed": 5},
    {"name": "DBMS",                 "exam_date": "2025-07-18", "difficulty": 2, "hours_needed": 4},
    {"name": "Theory of Computation","exam_date": "2025-07-22", "difficulty": 5, "hours_needed": 10},
]

# ──────────────────────────────────────────────────────────
# HOSTS FILE MANAGEMENT
# ──────────────────────────────────────────────────────────

REDIRECT      = "127.0.0.1"
BLOCK_START   = "# ===== DEEP WORK BLOCKER START ====="
BLOCK_END     = "# ===== DEEP WORK BLOCKER END ====="

def get_hosts_path():
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    return "/etc/hosts"

def _read_hosts():
    with open(get_hosts_path(), "r") as f:
        return f.read()

def _write_hosts(content):
    with open(get_hosts_path(), "w") as f:
        f.write(content)

def _strip_block(content):
    """Remove any existing blocker section from the hosts content."""
    lines  = content.splitlines()
    result = []
    inside = False
    for line in lines:
        if line.strip() == BLOCK_START:
            inside = True
            continue
        if line.strip() == BLOCK_END:
            inside = False
            continue
        if not inside:
            result.append(line)
    return "\n".join(result).rstrip("\n") + "\n"

def block_sites():
    try:
        content = _read_hosts()
        content = _strip_block(content)           # clean up any stale entries
        block   = [BLOCK_START]
        for site in BLOCKED_SITES:
            block.append(f"{REDIRECT}  {site}")
        block.append(BLOCK_END)
        _write_hosts(content.rstrip("\n") + "\n" + "\n".join(block) + "\n")
        print("  🔒 Sites blocked.")
        return True
    except PermissionError:
        print("\n  ⚠  Permission denied — cannot edit hosts file.")
        if platform.system() == "Windows":
            print("     Re-run this script as Administrator.")
        else:
            print(f"     Re-run: sudo python3 {sys.argv[0]}")
        return False

def unblock_sites():
    try:
        content = _read_hosts()
        _write_hosts(_strip_block(content))
        print("  🔓 Sites unblocked.")
    except PermissionError:
        print("  ⚠  Could not unblock sites — remove the DEEP WORK BLOCKER")
        print(f"     section from {get_hosts_path()} manually.")

# ──────────────────────────────────────────────────────────
# STUDY PLANNER  (CO2 — Weighted Shortest Deadline First)
# ──────────────────────────────────────────────────────────

def urgency_score(topic):
    """
    Weighted urgency heuristic (Weighted Job Scheduling / CO2 greedy search).
      score = (difficulty × hours_needed) / days_until_exam
    Higher score → study this first.
    """
    today    = datetime.today().date()
    exam     = datetime.strptime(topic["exam_date"], "%Y-%m-%d").date()
    days_left = max((exam - today).days, 0.5)   # avoid division by zero
    return (topic["difficulty"] * topic["hours_needed"]) / days_left

def show_study_plan():
    ranked = sorted(STUDY_TOPICS, key=urgency_score, reverse=True)
    today  = datetime.today().date()
    print("\n" + "═" * 50)
    print("  📚  OPTIMAL STUDY SEQUENCE  (CO2 greedy search)")
    print("═" * 50)
    print(f"  {'#':<3} {'Topic':<26} {'Days Left':>9} {'Score':>7}")
    print("  " + "─" * 46)
    for i, topic in enumerate(ranked, 1):
        exam  = datetime.strptime(topic["exam_date"], "%Y-%m-%d").date()
        days  = (exam - today).days
        score = urgency_score(topic)
        flag  = " 🔴" if days <= 3 else " 🟡" if days <= 7 else ""
        print(f"  {i:<3} {topic['name']:<26} {days:>6} days  {score:>5.1f}{flag}")
    print("═" * 50)




# ──────────────────────────────────────────────────────────
# TIMER
# ──────────────────────────────────────────────────────────

def countdown(minutes, label):
    """Countdown with a live updating progress bar in the terminal."""
    total_secs = minutes * 60
    remaining  = total_secs
    bar_width  = 30

    print()
    try:
        while remaining >= 0:
            mins, secs = divmod(remaining, 60)
            filled = int(bar_width * (total_secs - remaining) / total_secs)
            bar    = "█" * filled + "░" * (bar_width - filled)
            print(f"\r  {label}  [{bar}]  {mins:02d}:{secs:02d} ", end="", flush=True)
            if remaining == 0:
                break
            time.sleep(1)
            remaining -= 1
    except KeyboardInterrupt:
        print("\n\n  ⏹  Session interrupted.")
        unblock_sites()
        sys.exit(0)

    print()   # newline after bar completes

# ──────────────────────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────────────────────
 
def main():
    print("\n" + "═" * 50)
    print("  🧠  DEEP WORK — Pomodoro + Site Blocker")
    print("═" * 50)
    print(f"  Focus     : {FOCUS_MINUTES} min")
    print(f"  Short break: {SHORT_BREAK} min")
    print(f"  Long break : {LONG_BREAK} min  (every {CYCLES_BEFORE_LONG_BREAK} sessions)")
    print(f"  Blocking   : {len(BLOCKED_SITES)} domains")
 
    # Show study planner upfront
    show_study_plan()
 
    print("\n  Press ENTER to start your first focus session (Ctrl+C to quit).")
    input()
 
    session = 0
 
    while True:
        session += 1
        print(f"\n{'─'*50}")
        print(f"  🍅  Session #{session} — FOCUS  ({FOCUS_MINUTES} min)")
 
        blocked = block_sites()
        if not blocked:
            # No admin rights — timer still works, just no blocking
            print("  (Continuing without website blocking)\n")
 
        countdown(FOCUS_MINUTES, "FOCUS   ")
 
        # Unblock before break
        unblock_sites()
        print(f"\n  ✅  Session #{session} complete! Great work.\n")
 
        # Decide break length
        if session % CYCLES_BEFORE_LONG_BREAK == 0:
            print(f"  ☕  Long break — {LONG_BREAK} min")
            countdown(LONG_BREAK, "BREAK   ")
        else:
            print(f"  ☕  Short break — {SHORT_BREAK} min")
            countdown(SHORT_BREAK, "BREAK   ")
 
        print("\n  Press ENTER for the next session (Ctrl+C to quit).")
        try:
            input()
        except KeyboardInterrupt:
            print("\n  👋  Goodbye! Keep grinding.\n")
            sys.exit(0)
 
 
if __name__ == "__main__":
    main()
 
vishal