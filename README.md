
---

<p align="center">
  <img src="static/images/codeverse-logo.png" alt="CodeVerse Logo" width="200"/>
</p>

# ⚡️ CodeVerse – Online Judge Platform

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow.svg)

> **CodeVerse** is a secure, real-time Online Judge built using **Django**, **PostgreSQL**, and **Docker**.  
> It supports code execution in **Python**, **C**, **C++**, and **Java**, and features a sleek Monaco-powered code editor.

---

## 🚀 Key Features

* ✅ Custom User Model (Full Name, Timestamps)
* ✅ PostgreSQL integration with Django ORM
* ✅ Admin panel for managing Users, Problems, Submissions
* ✅ Problem listing and detail views
* ✅ Code submission and live verdict display
* ✅ Verdict System with: `AC`, `WA`, `TLE`, `MLE`, `RTE`, `CE`
* ✅ Memory limit and timeout enforcement (128MB, timeouts)
* ✅ Monaco Editor integration (branch: `monaco-integration-started`)
* ✅ Secure folder execution (`runs/`, `submissions/`)
* ✅ Toggleable file cleanup (`DELETE_SUBMISSION_FILES_AFTER_EVALUATION`, etc.)
* ✅ Admin panel to **promote/demote users**
* ✅ Add new problems via `/add-problem/` route
* ✅ Galaxy-themed UI, verdict boxes, and responsive layout

---

## 🌱 Branches Overview

| Branch                       | Purpose                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| `main`                       | Core features – problems, submissions, verdict system, and basic code submission UI |
| `monaco-integration-started` | Advanced editor with Monaco integration (syntax highlighting, IntelliSense – WIP)   |

ℹ️ **Current Branch:** `main`

---

## 🔭 Roadmap: Upcoming Milestones

| Phase | Feature                                            | Status        |
| ----- | -------------------------------------------------- | ------------- |
| ✅ 1   | PostgreSQL Setup                                   | ✔️ Complete    |
| ✅ 2   | Custom User Model + Admin Panel                    | ✔️ Complete    |
| ✅ 3   | Problem Pages + Basic Submission UI                | ✔️ Complete    |
| ✅ 4   | User Authentication                                | ✔️ Complete    |
| ✅ 5   | Verdict System (with Memory, Time, Runtime checks) | ✔️ Complete    |
| 🔜 6   | Leaderboard                                        | 🔄 In Progress |
| 🔜 7   | Tab Switch Detection (JS Visibility API)           | 🔜 Planned     |
| 🔜 8   | AI Debug Assistant (OpenAI or Gemini API)          | 🔜 Planned     |
| ✅ 9   | Monaco Editor Integration                          | ✅ Started     |
| 🔜 10  | Production Deployment (Docker + AWS EC2)           | 🔜 Planned     |

---

## 🧰 Tech Stack

| Layer           | Tech Used                                                                 |
| --------------- | ------------------------------------------------------------------------- |
| Backend         | Django 5.2                                                                |
| Database        | PostgreSQL 16                                                             |
| Code Execution  | Verdict system (TLE, MLE, RTE, WA, CE, AC) via subprocess (Docker coming) |
| Frontend        | Django Templates + Bootstrap 5                                            |
| Editor          | Basic `<textarea>` (in `main`) / Monaco Editor (in feature branch)        |
| Auth            | Custom Django User Model with full name                                   |
| Async Execution | Celery + Redis (Planned)                                                  |
| AI Integration  | OpenAI / Gemini API (Planned)                                             |
| Deployment      | AWS EC2 (Planned)                                                         |

---

## ⚙️ System Requirements (Must Be Installed Manually)

CodeVerse supports code execution in multiple languages. The following **system tools must be installed and available in your PATH**:

| Language   | Required Tools  | How to Install                                                                                            |
| ---------- | --------------- | --------------------------------------------------------------------------------------------------------- |
| Python     | `python3`       | [Download](https://www.python.org/downloads/) and install                                                 |
| C          | `gcc`           | ✅ Linux/macOS: pre-installed<br>🪟 Windows: Install [MinGW](https://www.mingw-w64.org/) and add to PATH    |
| C++        | `g++`           | ✅ Same as above                                                                                           |
| Java       | `javac`, `java` | [Adoptium JDK](https://adoptium.net) or [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) |
| PostgreSQL | `psql`          | [Download](https://www.postgresql.org/download/) and install                                              |

> ✅ You can verify installation using: `gcc --version`, `g++ --version`, `javac -version`, `psql --version`, `python3 --version`  
> ⚠️ These tools are **not included** in the virtual environment (`venv`). They must be installed **system-wide**.

---

## 🛠️ Local Development Setup

> 💡 **Note for Windows users:** If you're using PowerShell or CMD, you'll need to activate the virtual environment differently. See below.

### 🐧 Linux / macOS

```bash
# 1. Clone the repository
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

# 2. Set up virtual environment
python3 -m venv codeverse-env
source codeverse-env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Run development server
python manage.py runserver
````

### 🪟 Windows (Command Prompt)

```cmd
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

python -m venv codeverse-env
codeverse-env\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 🪟 Windows (PowerShell)

```powershell
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

python -m venv codeverse-env
.\codeverse-env\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 📁 Project Directory Structure

<details>
<summary>Click to view the structure (13 directories)</summary>

```bash
.
├── codeverse/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── judge/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── static/
│   └── images/
│       └── codeverse-logo.png
├── submissions/
├── runs/
├── requirements.txt
├── README.md
└── manage.py
```

</details>

---
