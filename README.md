# 🧠 Spaced Revision Task Logger

<p align="center">
  <strong>A pixel-style desktop study diary built to make revision automatic.</strong><br>
  Study → Log → Revise → Repeat
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Tkinter-GUI-FF6F00?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/Storage-JSON-000000?style=for-the-badge&logo=json&logoColor=white" alt="JSON">
  <img src="https://img.shields.io/github/last-commit/Aagam-jain124/Spaced-Revision-Task-Logger?style=for-the-badge" alt="Last commit">
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-how-spaced-revision-works">How it works</a> •
  <a href="#-getting-started">Run it</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

---

## 😂 The actual problem

> **Me:** "I'll remember this."
>
> **My brain 3 weeks later:**  
> *404 — Memory Not Found*

That's why this exists.

Instead of trusting Future Me™ to remember what Present Me studied, the app brings old material back automatically.

---

## 🎯 What is this?

**Spaced Revision Task Logger** is a lightweight desktop study system for people who are tired of writing:

> *"I'll revise this later."*

The app records what you studied and brings it back at fixed intervals:

### **3 days → 7 days → 21 days**

No account. No server. No database. Just a local Python app and your study data.

---

## ✨ Features

| Feature | What it does |
|---|---|
| 📋 **Daily Tasks** | Create study tasks and mark them complete |
| 📚 **Topic Logging** | Record what you actually studied |
| 🔁 **Spaced Revision** | Automatically surfaces revision after 3, 7 and 21 days |
| 📅 **Date Navigation** | Move through previous and future study days |
| 📊 **Progress Tracking** | See daily completion progress |
| 💾 **Auto Save** | Stores data locally in JSON |
| 🛡️ **Backup** | Keeps a `.bak` copy of the previous data |
| 🎮 **Pixel UI** | Retro-inspired visual design |
| ⌨️ **Keyboard Controls** | Navigate dates with `Ctrl + ←` / `Ctrl + →` |
| 🖥️ **Offline First** | Works without an internet connection |

<details>
<summary><strong>🔎 What does the app look like internally?</strong></summary>

The main window is organized around:

- 📅 Selected study date
- 📋 Tasks planned for that day
- 📈 Completion progress
- 📚 Topics studied
- 🔁 3-day revision queue
- 🔁 7-day revision queue
- 🔁 21-day revision queue

</details>

---

## 🧠 How Spaced Revision Works

When a task is completed or a topic is logged, the app schedules it for three future revision points.

| Study date | +3 days | +7 days | +21 days |
|---|---|---|---|
| **Sept 30** | **Oct 3** | **Oct 7** | **Oct 21** |

And the emotional journey is basically:

```text
Day 0     Day 3          Day 7             Day 21
 │         │              │                  │
 📚       😎             🤔                 💀
 "Easy"   "I know this"  "Wait..."          "WHAT IS THIS?"
 │         │              │                  │
 └─────────┴──────────────┴──────────────────┘
                 🔁 REVISION
```

> **Current algorithm:** fixed 3/7/21-day intervals. It is not yet an adaptive algorithm based on recall difficulty.

---

## 🚀 Getting Started

### Requirements

- Python 3
- Tkinter

No external Python packages are currently required.

### 1. Clone

```bash
git clone https://github.com/Aagam-jain124/Spaced-Revision-Task-Logger.git
cd Spaced-Revision-Task-Logger
```

### 2. Run

**Windows:**

```bash
python study_diary_tk.py
```

**Linux/macOS:**

```bash
python3 study_diary_tk.py
```

<details>
<summary><strong>🐧 Linux users</strong></summary>

If Tkinter is missing on Debian/Ubuntu:

```bash
sudo apt install python3-tk
```

</details>

---

## 📁 Project Structure

```
Spaced-Revision-Task-Logger/
│
├── 🐍 study_diary_tk.py
│   └── Main Tkinter application
│
├── 💾 study_diary.json
│   └── Local study data
│
├── 🛡️ study_diary.json.bak
│   └── Previous data backup
│
└── 📖 README.md
    └── Project documentation
```

### 💾 Your data stays local

The app stores study information in JSON instead of requiring a cloud service.

That means the data is:

- 🔒 Local
- 📦 Portable
- 🔍 Human-readable
- 💾 Easy to back up

---

## 🎮 Quick Interaction Guide

### Daily workflow

```text
        PLAN
          ↓
      📋 Add tasks
          ↓
       STUDY
          ↓
   📚 Log topics
          ↓
      ✅ Complete
          ↓
    ┌─────┼─────┐
    ↓     ↓     ↓
   +3d   +7d   +21d
    ↓     ↓     ↓
    🔁 REVISION
```

### Keyboard

| Shortcut | Action |
|---|---|
| `Ctrl + ←` | Previous day |
| `Ctrl + →` | Next day |

---

## 🤣 One more thing...

### Me when I finish studying a chapter

> **"Never need to see this again."**  
> — Me, approximately 4 minutes before the revision queue appears

### The revision queue:

```text
┌──────────────────────────┐
│  📚 HELLO AGAIN.         │
│                          │
│  You studied this.       │
│  You forgot this.        │
│  Revise this.            │
└──────────────────────────┘
```

**Brain:** *Can we just watch YouTube instead?*  
**App:** **No. 🔁**

---

## 🧪 Current Status

**🟢 Working prototype**

The core desktop workflow is implemented and usable. The project is intentionally small and is being developed incrementally.

---

## 🗺️ Roadmap

<details>
<summary><strong>🔜 Planned improvements</strong></summary>

- [ ] Adaptive revision intervals based on recall
- [ ] Subject/chapter categories
- [ ] Search and filtering
- [ ] Revision history
- [ ] Study statistics
- [ ] Weak-topic tracking
- [ ] Configurable revision intervals
- [ ] Export/import
- [ ] Optional reminders
- [ ] Improved cross-platform packaging

</details>

---

## 🎯 Design Philosophy

Most study planners focus on:

> **"What should I study today?"**

This project focuses on:

> **"What do I need to remember again?"**

The goal is not to create another complicated productivity dashboard.

It is to build a small tool that makes **revision hard to forget**.

---

## 🤝 Contributing

Found a bug or have an improvement idea?

1. Fork the repository
2. Create a branch
3. Make your change
4. Open a pull request

For larger changes, opening an issue first can help keep the project direction organized.

---

## 📄 License

No license has been specified yet.

---

<p align="center">
  <strong>Built for studying smarter, not just studying longer. 🧠</strong>
</p>
