
<p align="center">
  <img src="static/images/codeverse-logo.png" alt="CodeVerse Logo" width="200"/>
</p>

# ⚡️ CodeVerse – Online Judge Platform

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow.svg)

> **CodeVerse** is a secure, real-time Online Judge built using **Django**, **PostgreSQL**, and **subprocess-based execution**.  
> It supports multiple languages including **Python**, **C**, **C++**, and **Java**, with a powerful Monaco editor and custom verdict system.

---

## 🚀 Key Features

* ✅ Custom User Model (full name, timestamps)
* ✅ PostgreSQL integration with Django ORM
* ✅ Admin panel to **add/edit/delete problems**
* ✅ Promote/Demote users to admin
* ✅ Problem listing + Problem detail with code submission
* ✅ Live verdict system: `AC`, `WA`, `TLE`, `MLE`, `RTE`, `CE`
* ✅ Memory and Time limits enforced (e.g. 128MB, 5s cap)
* ✅ Online compiler (non-submission, testing-only)
* ✅ Monaco Editor (syntax highlighting, theme, autosize)
* ✅ AI Debug Assistant (planned)
* ✅ Tab Switch Detection (planned anti-cheating)
* ✅ Responsive Galaxy-themed UI with stylish verdict boxes

---

## 🧠 Current Branch: `main`

> All previous branches like `monaco-integration-started` have been **merged into `main`** and deleted.

---

## 🔭 Roadmap: Upcoming Milestones

| Phase | Feature                                            | Status        |
| ----- | -------------------------------------------------- | ------------- |
| ✅ 1   | PostgreSQL Setup                                   | ✔️ Complete    |
| ✅ 2   | Custom User Model + Admin Panel                    | ✔️ Complete    |
| ✅ 3   | Problem Pages + Basic Submission UI                | ✔️ Complete    |
| ✅ 4   | User Authentication                                | ✔️ Complete    |
| ✅ 5   | Verdict System (with Memory, Time, Runtime checks) | ✔️ Complete    |
| ✅ 6   | Monaco Editor Integration                          | ✔️ Complete    |
| 🔜 7   | Leaderboard                                        | 🔄 In Progress |
| 🔜 8   | Tab Switch Detection (JS Visibility API)           | 🔜 Planned     |
| 🔜 9   | AI Debug Assistant (OpenAI or Gemini API)          | 🔜 Planned     |
| 🔜 10  | Docker + EC2 Deployment                            | 🔜 Planned     |

---

## 🧰 Tech Stack

| Layer          | Tech Used                                                                   |
| -------------- | --------------------------------------------------------------------------- |
| Backend        | Django 5.2                                                                  |
| Database       | PostgreSQL 16                                                               |
| Code Execution | Python `subprocess` (Docker sandboxing planned)                             |
| Languages      | Python 3, C, C++, Java (JDK)                                                |
| Frontend       | Bootstrap 5, custom CSS, Fira Code font                                     |
| Editor         | Monaco Editor (theme, layout, code parsing)                                 |
| Admin Tools    | Promote/demote users, manage problems via `/manage/`                        |
| File Handling  | Organized into `submission_files/runs/` and `submission_files/submissions/` |
| Deployment     | Local dev (Docker + AWS planned)                                            |

---

## ⚙️ System Requirements (Manual)

Make sure these are installed **system-wide** (not just in `venv`):

| Language   | Required Tools  | How to Install                                                                                            |
| ---------- | --------------- | --------------------------------------------------------------------------------------------------------- |
| Python     | `python3`       | [Download](https://www.python.org/downloads/) and install                                                 |
| C          | `gcc`           | ✅ Linux/macOS: pre-installed<br>🪟 Windows: Install [MinGW](https://www.mingw-w64.org/) and add to PATH    |
| C++        | `g++`           | ✅ Same as above                                                                                           |
| Java       | `javac`, `java` | [Adoptium JDK](https://adoptium.net) or [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) |
| PostgreSQL | `psql`          | [Download](https://www.postgresql.org/download/) and install                                              |

> Check versions using: `gcc --version`, `javac -version`, `psql --version`, `python3 --version`

---

## 🛠️ Local Development Setup

### 🐧 Linux / macOS

```bash
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

python3 -m venv codeverse-env
source codeverse-env/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````

### 🪟 Windows (CMD)

```cmd
python -m venv codeverse-env
codeverse-env\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 📁 Project Directory Structure

<details>
<summary>Click to view the structure (20 directories)</summary>

```bash
.
├── codeverse/              # Django project config (settings, urls, wsgi, etc.)
│   ├── asgi.py
│   ├── settings.py
│   └── ...
├── codeverse-env/          # Python virtual environment (not pushed to Git)
│   ├── bin/
│   ├── lib/
│   └── ...
├── judge/                  # Core app: models, views, admin, templates
│   ├── admin.py
│   ├── forms.py
│   ├── templates/
│   ├── templatetags/
│   └── ...
├── static/                 # Static assets (images, css, js)
│   └── images/
│       └── codeverse-logo.png
├── submission_files/       # Isolated run and submission folders
│   ├── runs/
│   └── submissions/
├── manage.py               # Django CLI launcher
├── requirements.txt        # Python package dependencies
├── README.md               # You're reading it ;)
├── ojfinal_hld_Srivardhan_Ginjala.pdf  # Project report (HLD)
```

</details>



