# 🚀 CodeVerse - Online Judge Platform

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

**CodeVerse** is a real-time, secure **Online Judge** platform built with **Django + PostgreSQL + Docker** for evaluating Python, C, and C++ code.  
It includes sandboxed execution, custom problems, admin control, and an intuitive frontend with AI debugging and tab monitoring planned.

---

## 📌 Features Implemented So Far

- ✅ User Registration, Login, Logout
- ✅ PostgreSQL Integration
- ✅ Custom User Model (Full Name support)
- ✅ Problem Listing `/problems/`
- ✅ Problem Detail View `/problems/<code>/`
- ✅ Admin Panel for Problems + Submissions
- ✅ Code Submission UI
- ✅ Responsive Styling with Bootstrap
- ✅ Superuser Login via `/admin`

---

## 🌿 Branches Overview

| Branch                       | Description                                                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `main`                       | Core backend + frontend structure — fully working problem submission and admin panel                                 |
| `monaco-integration-started` | Adds Monaco Editor (VS Code–like editor) for rich coding experience — auto-indent, IntelliSense (WIP), syntax colors |

🔄 **You are currently on: `monaco-integration-started`**  
💡 Use `git checkout monaco-integration-started` to explore the editor enhancements.

---

## 🔜 Feature Roadmap (Phase-wise TODO)

| Phase | Feature                                        | Status                                    |
| ----- | ---------------------------------------------- | ----------------------------------------- |
| ✅ 1   | PostgreSQL Setup                               | ✔️ Complete                                |
| ✅ 2   | Custom User + Admin                            | ✔️ Complete                                |
| ✅ 3   | Problem Pages                                  | ✔️ Complete                                |
| 4️⃣     | Login / Logout                                 | 🚧 In Progress                             |
| 5️⃣     | Code Submission + Verdicts (Docker Sandboxing) | 🔜                                         |
| 6️⃣     | Leaderboard Page                               | 🔜                                         |
| 7️⃣     | Tab Switch Detection (JS Visibility API)       | 🔜                                         |
| 8️⃣     | AI Debug Assistant (OpenAI / Gemini API)       | 🔜                                         |
| 9️⃣     | **Monaco Editor Integration**                  | ✅ Started in `monaco-integration-started` |
| 🔟     | Final Hosting (AWS EC2)                        | 🔜                                         |

---

## 🛠️ Tech Stack

| Layer          | Tech Used                                                                    |
| -------------- | ---------------------------------------------------------------------------- |
| Backend        | Django 5.2                                                                   |
| Database       | PostgreSQL 16                                                                |
| Auth           | Custom User Model                                                            |
| Code Execution | Docker (Upcoming)                                                            |
| Task Queue     | Celery + Redis (Planned)                                                     |
| AI API         | OpenAI / Gemini (Planned)                                                    |
| Hosting        | AWS EC2                                                                      |
| Frontend       | Django Templates + Bootstrap                                                 |
| Code Editor    | Basic Textarea (in `main`) / Monaco Editor (in `monaco-integration-started`) |

---

## 🧪 Local Development Setup

```bash
# Clone the repo
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

# Create virtual environment
python3 -m venv codeverse-env
source codeverse-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply DB Migrations
python manage.py migrate

# Run the dev server
python manage.py runserver
