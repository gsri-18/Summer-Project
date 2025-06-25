
# ⚡️ CodeVerse – Online Judge Platform

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow.svg)

> **CodeVerse** is a secure, real-time Online Judge built using **Django**, **PostgreSQL**, and **Docker**.  
> It supports code execution in **Python**, **C**, **C++**, and **Java** (via sandboxing), and features a sleek Monaco-powered code editor.

---

## 🚀 Key Features

- ✅ User Registration, Login, Logout (with custom user model)
- ✅ PostgreSQL integration with Django ORM
- ✅ Admin panel for managing problems, users, and submissions
- ✅ Problem listing & detail views with code submission form
- ✅ Verdict system (AC, WA, TLE, MLE, RTE, CE)
- ✅ Monaco Editor-based IDE (via `monaco-integration-started` branch)
- ✅ Resizable IDE layout and custom input/output support
- ✅ Bootstrap-powered responsive frontend

---

## 🌱 Branches Overview

| Branch                       | Purpose                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| `main`                       | Core features – problems, submissions, verdict system, and basic code submission UI |
| `monaco-integration-started` | Advanced editor with Monaco integration (syntax highlighting, IntelliSense – WIP)   |

ℹ️ **Current Branch:** `main`  


---

## 🔭 Roadmap: Upcoming Milestones

| Phase | Feature                                            | Status                                   |
| ----- | -------------------------------------------------- | ---------------------------------------- |
| ✅ 1   | PostgreSQL Setup                                   | ✔️ Complete                               |
| ✅ 2   | Custom User Model + Admin Panel                    | ✔️ Complete                               |
| ✅ 3   | Problem Pages + Basic Submission UI                | ✔️ Complete                               |
| ✅ 4   | User Authentication                                | ✔️ Complete                               |
| ✅ 5   | Verdict System (with Memory, Time, Runtime checks) | ✔️ Complete                               |
| 🔜 6   | Leaderboard                                        | 🔄 In Progress                            |
| 🔜 7   | Tab Switch Detection (JS Visibility API)           | 🔜 Planned                                |
| 🔜 8   | AI Debug Assistant (OpenAI or Gemini API)          | 🔜 Planned                                |
| ✅ 9   | Monaco Editor Integration                          | ✅ Started 
| 🔜 10  | Production Deployment (Docker + AWS EC2)           | 🔜 Planned                                |

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

## 🛠️ Local Development Setup

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
```


---

## 📁 Project Directory Structure

<details>
<summary>Click to view the structure (13 directories)</summary>

```bash
.
├── codeverse
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── codeverse-env/
│   ├── bin/
│   ├── include/
│   ├── lib/
│   ├── lib64 -> lib
│   └── pyvenv.cfg
├── judge
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py
│   ├── __pycache__/
│   ├── templates/
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── ojfinal_hld_Srivardhan_Ginjala.pdf
├── README.md
├── requirements.txt
└── submission_files/
```

</details>

---

