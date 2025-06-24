# 🚀 CodeVerse - Online Judge Platform

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

CodeVerse is a secure, real-time **Online Judge** platform for submitting and evaluating code in Python and C/C++. Built using **Django + PostgreSQL + Docker**, it supports custom problems, secure sandboxed execution, AI-powered debugging help, and tab-switch detection to ensure exam integrity.

---

## 📌 Features Implemented So Far

- ✅ **User Registration**
- ✅ **PostgreSQL Setup (instead of SQLite)**
- ✅ **Custom `User` Model with Full Name**
- ✅ **Problem Listing Page** `/problems/`
- ✅ **Problem Detail Page** `/problems/<code>/`
- ✅ **Admin Panel for Managing Problems and Submissions**
- ✅ **Superuser Login (via /admin)**
- ✅ **Custom Migrations**

---

## 🔜 Features Coming Soon (TODO List)

| Phase | Feature | Status |
|-------|---------|--------|
| 4️⃣ | User Login + Logout system | 🚧 In Progress |
| 5️⃣ | Code submission + verdict system using Docker | 🔜 |
| 6️⃣ | Leaderboard screen (`/leaderboard/`) | 🔜 |
| 7️⃣ | Tab switch detection using JS Visibility API | 🔜 |
| 8️⃣ | AI-based Debugging Assistant using OpenAI API | 🔜 |
| 9️⃣ | Frontend Enhancements with **CodeMirror**, styling | 🔜 |
| 🔟 | Final Deployment on **AWS EC2** | 🔜 |

---

## 🛠️ Technology Stack

| Component | Tech |
|----------|------|
| Backend | Django 5.2 |
| Database | PostgreSQL 16 |
| Auth | Django built-in with custom `User` |
| Code Execution | Docker Containers (to be integrated) |
| Queue System | Celery + Redis (upcoming) |
| AI Integration | Gemini / OpenAI API |
| Deployment | AWS EC2 (target) |
| Frontend | Django Templates + Bootstrap + JavaScript |

---

## 🔧 Local Setup (For Devs)

```bash
# Clone the repository
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

# Create a virtual environment
python3 -m venv codeverse-env
source codeverse-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL manually or use Docker (instructions coming soon)

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver

