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