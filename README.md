
<p align="center">
  <img src="static/images/codeverse-logo.png" alt="CodeVerse Logo" width="180"/>
</p>

# CodeVerse – Online Judge Platform

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow.svg)

> **CodeVerse** is a secure, customizable Online Judge built with **Django**, **PostgreSQL**, and **subprocess-based code execution**.  
> It supports **Python**, **C**, **C++**, and **Java**, provides real-time verdicts, and features a powerful **Monaco-based editor**. 

---

## Features

- Custom User Model (with full name & timestamps)
- PostgreSQL-backed data integrity
- Superuser controls to add/edit/delete problems and manage users
- Clean submission pipeline with live verdicts: `Accepted`, `Wrong Answer`, `TLE`, `MLE`, `RTE`, `CE`
- Time and memory limit enforcement (e.g. 5s cap, 128MB RAM cap)
- Monaco Editor: syntax highlighting, smart layout, and theme support
- Non-submission compiler mode (for trial runs)
- User profile with overview, submission history, accuracy, and per-language verdict stats
- Profile editing and password change support
- Stylish UI with dark theme and clear feedback
- Simplified the problem add feature, Just upload your Problem in .md format, using the template.

---

## Current Branch

**`main`** — all experimental branches (e.g., `monaco-integration-started`) have been merged and deleted.

---

## Roadmap

| Phase | Feature                                        | Status        |
| ----- | ---------------------------------------------- | ------------- |
| 1     | PostgreSQL + Django Setup                      | ✅ Complete    |
| 2     | Custom User Model + Admin Control              | ✅ Complete    |
| 3     | Problem Creation, Listing, Detail Page         | ✅ Complete    |
| 4     | User Authentication (Register/Login/Logout)    | ✅ Complete    |
| 5     | Code Submission Verdict System (subprocess)    | ✅ Complete    |
| 6     | Monaco Editor Integration                      | ✅ Complete    |
| 7     | Leaderboard System                             | 🔄 In Progress |
| 8     | Tab Visibility/Focus Detection (anti-cheating) | 🔜 Planned     |
| 9     | AI Debug Assistant (OpenAI/Gemini integration) | 🔜 Planned     |
| 10    | Docker Isolation + EC2 Deployment              | 🔜 Planned     |

---

## Tech Stack

| Layer          | Technology                                |
| -------------- | ----------------------------------------- |
| Backend        | Django 5.2                                |
| Database       | PostgreSQL 16                             |
| Code Execution | Python `subprocess` (Docker planned)      |
| Supported Lang | Python 3, C, C++, Java (JDK)              |
| Frontend       | Bootstrap 5, Fira Code, custom CSS        |
| Code Editor    | Monaco Editor (via CDN integration)       |
| Admin Tools    | Django Admin + Custom UI controls         |
| File Handling  | `submission_files/runs/` & `submissions/` |

---

## System Requirements

Install the following **globally** before running the project:

| Language   | Toolchain       | Installation Hint                                                                                     |
| ---------- | --------------- | ----------------------------------------------------------------------------------------------------- |
| Python     | `python3`       | [Python.org](https://www.python.org/downloads/)                                                       |
| C          | `gcc`           | Use `apt`, `brew`, or [MinGW](https://www.mingw-w64.org/) on Windows                                  |
| C++        | `g++`           | Same as above                                                                                         |
| Java       | `javac`, `java` | [Adoptium](https://adoptium.net) or [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) |
| PostgreSQL | `psql`          | [Download](https://www.postgresql.org/download/)                                                      |

---

## Checking Tool Versions

### On Linux/macOS:
```bash
gcc --version
g++ --version
javac -version
java -version
psql --version
python3 --version
````

### On Windows (CMD/PowerShell):

```cmd
gcc --version
g++ --version
javac -version
java -version
psql --version
python --version
```

---

## Local Development Setup

### Linux/macOS

```bash
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

python3 -m venv codeverse-env
source codeverse-env/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Windows

```cmd
python -m venv codeverse-env
codeverse-env\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Superuser Access

By default, newly registered users are **not** admins. To access the admin panel:

```bash
python manage.py createsuperuser
```

Then visit:

```
http://127.0.0.1:8000/admin/
```

Use this to:

* Manage problems/test cases
* Promote/demote users
* Monitor data directly

Admin-only management also available from CodeVerse’s own UI via dropdown menus.

---

## Directory Structure

<details>
<summary>Expand to view structure</summary>

```bash
.
├── codeverse/              # Django project settings
├── codeverse-env/          # Virtual environment (local)
├── judge/                  # Main app (models, views, templates)
├── static/                 # Static files (CSS, images, JS)
│   └── images/
│       └── codeverse-logo.png
├── submission_files/
│   ├── runs/               # Compiler-only runs
│   └── submissions/        # Real submissions
├── manage.py
├── requirements.txt
├── README.md
├── ojfinal_hld_Srivardhan_Ginjala.pdf  # HLD Report
```

</details>

---

## License

This project is intended for academic and learning purposes.
Commercial deployment or scaling will require appropriate Docker isolation and external sandboxing.



