<p align="center">
  <img src="static/images/codeverse-logo.png" alt="CodeVerse Logo" width="180"/>
</p>

<h1 align="center"> CodeVerse – Online Judge Platform</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg"/>
  <img src="https://img.shields.io/badge/Django-5.2-green.svg"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-blue.svg"/>
  <img src="https://img.shields.io/badge/Status-In_Progress-yellow.svg"/>
</p>

> **CodeVerse** is a full-stack, real-time **Online Judge** built with Django + PostgreSQL + Docker-isolated code execution.
> Designed for performance, customizability, and clarity — it supports **Python**, **C**, **C++**, and **Java**, and features a modern **Monaco Editor** interface.

---

##  Features

*  **Custom User Model** (full name, timestamps)
*  **User Authentication** (Register, Login, Logout, Profile Edit)
*  **Live Verdicts** on submission: `Accepted`, `Wrong Answer`, `TLE`, `MLE`, `RTE`, `CE`
*  **Add Problems via Markdown** template
*  **Time & Memory Limit Enforcement** (up to 5s / 512MB supported)
*  **Docker-based Code Execution Sandbox** for safe, isolated runs
*  **Monaco Editor Integration**: themes, syntax highlight, vertical split UI
*  **Compiler-only Mode** for trial runs
*  **User Dashboard** with submission stats
*  **Admin Panel** to manage Problems, TestCases, Users, and Submissions
*  **File Cleanup Toggles** to control cleanup of generated code files
*  **Cosmic UI** with animated intro, verdict box styling, and mobile responsiveness
*  **Folder Separation** for `runs/` vs `submissions/` to avoid collisions

---

##  Roadmap

| Phase | Feature                                        | Status        |
| ----- | ---------------------------------------------- | ------------- |
| 1     | PostgreSQL + Django Setup                      | ✅ Complete    |
| 2     | Custom User Model + Admin Control              | ✅ Complete    |
| 3     | Problem Creation, Listing, Detail Page         | ✅ Complete    |
| 4     | User Authentication (Register/Login/Logout)    | ✅ Complete    |
| 5     | Code Submission Verdict System (subprocess)    | ✅ Complete    |
| 6     | Monaco Editor Integration                      | ✅ Complete    |
| 7     | Docker Isolation for Code Execution            | ✅ Complete    |
| 8     | Leaderboard System                             | 🔄 In Progress |
| 9     | Tab Visibility/Focus Detection (anti-cheating) | 🔜 Planned     |
| 10    | AI Debug Assistant (OpenAI/Gemini integration) | 🔜 Planned     |
| 11    | EC2 Deployment                                 | 🔜 Planned     |

---

##  Tech Stack

| Layer           | Technology                           |
| --------------- | ------------------------------------ |
| Backend         | Django 5.2                           |
| Database        | PostgreSQL 16                        |
| Code Execution  | Docker + Python `subprocess` sandbox |
| Supported Langs | Python, C, C++, Java                 |
| Frontend        | Bootstrap 5, custom CSS, Fira Code   |
| Editor          | Monaco Editor (via CDN)              |
| Admin Tools     | Django Admin Panel                   |
| File Handling   | `runs/`, `submissions/` folders      |

---

##  System Requirements

The following **tools must be installed globally** on your system:

| Language   | Toolchain       | Install Guide                                                                                         |
| ---------- | --------------- | ----------------------------------------------------------------------------------------------------- |
| Python     | `python3`       | [python.org](https://www.python.org/downloads/)                                                       |
| C          | `gcc`           | `apt install gcc` or [MinGW](https://www.mingw-w64.org/)                                              |
| C++        | `g++`           | Same as above                                                                                         |
| Java       | `javac`, `java` | [Adoptium](https://adoptium.net) or [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) |
| PostgreSQL | `psql`          | [Download PostgreSQL](https://www.postgresql.org/download/)                                           |
| Docker     | `docker`        | [Docker Installation Guide](https://docs.docker.com/get-docker/)                                      |

###  Version Check (Linux/macOS)

```bash
gcc --version
g++ --version
javac -version
java -version
psql --version
python3 --version
docker --version
```

###  Version Check (Windows CMD)

```cmd
gcc --version
g++ --version
javac -version
java -version
psql --version
python --version
docker --version
```

---

##  Local Development Setup

> Virtual environment is highly recommended.

### 🐧 Linux/macOS

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

### 🪟 Windows (CMD)

```cmd
git clone https://github.com/gsri-18/Summer-Project.git
cd Summer-Project

python -m venv codeverse-env
codeverse-env\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
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
python manage.py createsuperuser
python manage.py runserver
```

---

## 🔑 Superuser Access

To manage users, problems, and verdicts:

```bash
python manage.py createsuperuser
```

Then visit:
👉 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

You don’t need to rely on the `/admin/` page only — users with staff privileges can add/update/delete problems from the frontend admin dropdown menu.

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>


```bash
.
├── check_project_health.sh
├── codeverse
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   └── utils
│       ├── code_executor.py
│       └── code_runner.py
├── docker_runner
│   ├── Dockerfile
│   └── run_code.sh
├── judge
│   ├── admin.py
│   ├── forms.py
│   ├── migrations
│   ├── models.py
│   ├── templates
│   ├── templatetags
│   ├── tests
│   ├── urls.py
│   └── views.py
├── manage.py
├── ojfinal_hld_Srivardhan_Ginjala.pdf
├── problems
│   ├── admin.py
│   ├── migrations
│   ├── models.py
│   ├── templates
│   ├── tests
│   ├── urls.py
│   └── views.py
├── static
│   ├── css
│   ├── downloads
│   ├── images
│   ├── js
│   └── monaco-themes
├── staticfiles
│   ├── admin
│   ├── css
│   ├── img
│   └── js
└── submission_files
    ├── contest_subs
    ├── docker_temp
    ├── runs
    └── submissions
```

</details>

---

## 📄 License

This project is intended for academic and personal use.
For production or competitive deployment, Docker-based isolation is strongly recommended (and now integrated!).

---

### 👨‍🚀 Maintainer

Made with love by [@gsri-18](https://github.com/gsri-18)
Drop a ⭐ on the repo if you found it helpful!

