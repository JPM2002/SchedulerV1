# 🧠 SchedulerV1

Welcome to **SchedulerV1** – your minimalist yet powerful terminal-based assistant for tracking Canvas assignments and syncing with your academic calendar.

---

## 📁 Project Structure

```bash
SchedulerV1/
│
├── App/                        # Main application folder
│   ├── Main.py                 # Main CLI app entry point
│   ├── requirements.txt        # Python dependencies
│   ├── config/                 # API key storage
│   ├── core/                   # Core logic for API, calendar, UI
│   └── ICS/                    # Folder where your .ics calendar lives
│
├── Development/               # All development scripts and utilities used during build
├── canvas_env/                # Your virtual environment (not pushed to Git)
├── .gitignore
└── README.md
```

---

## 🚀 Features

- ✅ Fetch today's Canvas assignments
- ✅ View today's calendar classes from .ics files
- ✅ Import any calendar file (.ics)
- ✅ CLI with ASCII art and fun commentary
- ✅ API key + calendar folder setup
- ✅ Reset everything with a single command

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-user/SchedulerV1.git
cd SchedulerV1/App
```

### 2. Create & activate a virtual environment

```bash
python -m venv canvas_env
# Activate:
# On Windows:
canvas_env\Scripts\activate
# On Mac/Linux:
source canvas_env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python Main.py
```

---

## 🧩 Inside the App

When you run it, you'll see a menu:

- `🔑 Add new API key` – stores your Canvas API key locally
- `📁 Setup calendar folder with .ics file` – copy your course schedule
- `📅 What is due today?` – view assignments due today
- `🚀 Let’s get ahead` – placeholder for future planning features
- `❌ Exit` – close the app like a responsible adult

---

## 🧼 Resetting

Use the reset option to clear saved API keys and .ics files. You'll be asked to confirm by typing `RESTART`.

---

## 📎 Notes

- Your API key is stored locally in `App/config/api_key.txt`
- Calendar file goes in `App/ICS/calendar/`
- Development logic/scripts live in the `Development/` folder and are not needed to run the app

---

Made to try to not overthink by Javier (done in, 2 hours)
## 📁 Development Folder Structure

This folder contains atomic-level experimental and development scripts.

```
Development/
│   .env
│
├───ICS
│   │   read_today_event.py
│   │   read_week.py
│   │   
│   └───calendar
│           SP_2025-JDP5958.ics
│
└───Scripts
        canvas_api_key.txt
        canvas_fetch.py
        due_today.py
        read_today_week.py
        simple.py
        test.py
        test1.py
```
