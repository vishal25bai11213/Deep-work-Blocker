# Deep-work-Blocker
# 🧠 Deep Work Distraction Blocker

A terminal-based **Pomodoro timer** that temporarily blocks distracting websites by editing your system's `hosts` file during focus sessions. Built with pure Python — no extra packages required.

---

## Features

- ⏱ **Pomodoro Timer** — 25-min focus sessions with configurable short (5 min) and long (15 min) breaks
- 🔒 **Website Blocker** — edits `/etc/hosts` (or Windows equivalent) to redirect distracting sites to `127.0.0.1`
- 🔓 **Auto-unblock** — sites are unblocked automatically when the session or break ends, and on Ctrl+C
- 📚 **Study Planner** — ranks your study topics using a greedy urgency algorithm (CO2 Weighted Job Scheduling)
- 💻 **Terminal-only** — works entirely in VS Code's integrated terminal, no GUI needed

---

## Requirements

- Python 3.6+
- No third-party packages — uses only `time`, `os`, `sys`, `platform`, `datetime`

---

## How to Run

### macOS / Linux
```bash
sudo python3 deep_work_blocker.py
```
`sudo` is required because the script edits `/etc/hosts`.

### Windows
1. Open VS Code **as Administrator** (right-click → Run as Administrator)
2. Open the integrated terminal and run:
```bash
python deep_work_blocker.py
```

> **Note:** If you run without admin rights, the timer still works — website blocking is just skipped with a warning.

---

## Configuration

Everything is at the top of `deep_work_blocker.py` under the **CONFIGURATION** section:

```python
FOCUS_MINUTES = 25          # Length of each focus session
SHORT_BREAK   = 5           # Short break after each session
LONG_BREAK    = 15          # Long break after N sessions
CYCLES_BEFORE_LONG_BREAK = 4

BLOCKED_SITES = [
    "youtube.com", "www.youtube.com",
    "reddit.com",  ...      # Add or remove sites freely
]

STUDY_TOPICS = [
    {"name": "Algorithms", "exam_date": "2025-07-10", "difficulty": 4, "hours_needed": 8},
    ...                     # Edit with your own subjects
]
```

---

## Study Planner — CO2 Algorithm

When you start the script, it prints an optimal study sequence using the **Weighted Shortest Deadline First** heuristic — a classical greedy search algorithm from CO2:

```
score = (difficulty × hours_needed) / days_until_exam
```

Topics with higher scores (hard subject, many hours needed, close deadline) are ranked first. Colour indicators show urgency:
- 🔴 3 days or fewer
- 🟡 7 days or fewer

---

## Project Structure

```
deep_work_blocker.py    # Single file — everything is here
README.md
Project_Report.docx
```

---

## How It Works — Hosts File Blocking

The script appends entries like these to your hosts file during a focus session:

```
# ===== DEEP WORK BLOCKER START =====
127.0.0.1  youtube.com
127.0.0.1  www.youtube.com
...
# ===== DEEP WORK BLOCKER END =====
```

These are cleanly removed when the session ends. If the script is interrupted (Ctrl+C), it unblocks before exiting. You can also manually delete the section between the two marker comments if needed.

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| `Enter` | Start next session |
| `Ctrl+C` | Stop and unblock sites immediately |

---

## Troubleshooting

**Sites not being blocked?**
Make sure you ran with `sudo` (Linux/macOS) or as Administrator (Windows).

**Sites still blocked after quitting?**
Open your hosts file and delete everything between `# ===== DEEP WORK BLOCKER START =====` and `# ===== DEEP WORK BLOCKER END =====`.

**Hosts file location:**
- Linux/macOS: `/etc/hosts`
- Windows: `C:\Windows\System32\drivers\etc\hosts`
