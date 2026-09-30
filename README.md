# Spaced Revision Task Logger

A **pixel-style desktop study diary** built with Python and Tkinter for tracking daily study tasks, logging topics, and automatically surfacing revision work after **3, 7, and 21 days**.

The app is designed around a simple loop:

**Study → Log → Revise → Repeat**

## ✨ Features

- 📋 **Daily task list** — add study tasks and mark them complete.
- 📚 **Topic logging** — record what you studied each day.
- 🔁 **Automatic spaced revision** — completed tasks and studied topics reappear after 3, 7, and 21 days.
- 📅 **Date navigation** — move between days, jump to a specific date, or return to today.
- 📊 **Daily progress bar** — see how many planned tasks are complete.
- 💾 **Persistent local storage** — data is saved automatically to `study_diary.json`.
- 🛡️ **Automatic backup** — the previous data file is kept as `study_diary.json.bak`.
- 🎮 **Pixel-inspired UI** — chunky controls, pixel-art icons, and retro styling.
- ⌨️ **Keyboard shortcuts** — use `Ctrl + Left` / `Ctrl + Right` to navigate days.
- 🖥️ **Pure Python desktop app** — uses Tkinter and the Python standard library; no third-party packages are required.

## 🧠 How Spaced Revision Works

The app uses three fixed revision intervals:

**3 days → 7 days → 21 days**

When a task is marked **DONE**, or a topic is logged, it becomes eligible for revision at those intervals.

For example:

| Studied | Revision 1 | Revision 2 | Revision 3 |
|---|---|---|---|
| Sept 30 | Oct 3 | Oct 7 | Oct 21 |

Revision items appear in the footer under their respective interval. Tick an item once you have revised it.

> The current implementation uses fixed intervals rather than an adaptive spaced-repetition algorithm.

## 🖼️ App Structure

The main screen contains:

- **Date navigation** at the top
- **Tasks** for the selected day
- **Daily progress** indicator
- **Topics studied today**
- **Revision footer** containing 3-day, 7-day, and 21-day revision queues

The UI is intentionally lightweight so it can be used as a daily study companion without needing an account, server, or database.

## 🚀 Getting Started

### Requirements

- Python 3
- Tkinter

Tkinter is normally included with Python on Windows. On Ubuntu/Debian, install it with:

```bash
sudo apt install python3-tk
```

### Run

Clone the repository:

```bash
git clone https://github.com/Aagam-jain124/Spaced-Revision-Task-Logger.git
cd Spaced-Revision-Task-Logger
```

Run the app:

```bash
python study_diary_tk.py
```

On some systems you may need:

```bash
python3 study_diary_tk.py
```

## 📁 Files

```
Spaced-Revision-Task-Logger/
├── study_diary_tk.py       # Main Tkinter application
├── study_diary.json        # Local study data
├── study_diary.json.bak    # Previous saved data backup
└── README.md
```

### Data format

Study data is stored locally in JSON. The application creates the file automatically and keeps a backup of the previous version whenever it saves.

This also keeps the data portable and easy to inspect or back up manually.

## 🎯 Project Philosophy

Most study planners answer:

> **"What should I study?"**

This project focuses on another important question:

> **"What do I need to remember again?"**

The goal is to turn revision into a visible, trackable process rather than relying on memory or vague plans like *"I'll revise this later."*

## 🚧 Current Status

**Working prototype / actively evolving**

The core desktop application is implemented. The project can be extended with more advanced scheduling, analytics, and study workflows as development continues.

## 🔮 Possible Future Improvements

- [ ] Adaptive revision intervals based on recall/performance
- [ ] Subject and chapter categories
- [ ] Search and filtering
- [ ] Revision history and statistics
- [ ] Weak-topic / mistake tracking
- [ ] Configurable revision intervals
- [ ] Export/import tools
- [ ] Better cross-platform packaging
- [ ] Browser version / shared data format
- [ ] Optional reminders or notifications

## 📄 License

No license has been specified yet.
