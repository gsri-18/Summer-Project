<p align="center">
  <img src="static/images/codeverse-logo.png" alt="CodeVerse Logo" width="180"/>
</p>

<h1 align="center"> CodeVerse – Online Judge Platform</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg"/>
  <img src="https://img.shields.io/badge/Django-5.2-green.svg"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-blue.svg"/>
  <img src="https://img.shields.io/badge/Docker-Isolated-brightgreen.svg"/>
  <img src="https://img.shields.io/badge/Status-Actively%20Developed-orange.svg"/>
</p>

<p align="center">
  <strong>Live Demo:</strong> <em>Temporarily offline</em> 
</p>

<p align="center">
  You can run CodeVerse locally by following the setup instructions below.
</p>

> **CodeVerse** is a full-stack, secure **Online Judge Platform** powered by Django, PostgreSQL, and Docker-based isolation.  
> Now with a sleek Monaco editor, **live verdicts**, **AI debug help**, and a growing developer-friendly ecosystem.


---

## Features

- **Live Verdict System** (`AC`, `WA`, `TLE`, `MLE`, `RTE`, `CE`)
- **Docker-based Isolation** for safe code execution
- **Problem Creation via Markdown Templates**
- **Monaco Editor** with syntax highlighting, theming & vertical split
- **Leaderboard** with difficulty-wise performance stats
- **AI Debug Assistant** (integrated with Gemini)
- **Custom Test Runs** (Compiler-only mode)
- **Frontend Admin Tools** (modal-based, JS-enhanced creation)
- **TestCase Management** per problem
- **Custom User Model** with profile & full name
- **File Cleanup Toggles** (`runs/`, `submissions/`)
- **Cosmic UI** – animated intro, mobile responsive, terminal-like I/O

---

## Deployment Note

CodeVerse was successfully deployed and tested on AWS EC2 (Free Tier).
The public demo has been taken offline to avoid persistent cloud costs.

The platform is fully reproducible locally and can be redeployed on any
cloud provider using the documented setup steps.

---

## Roadmap

| Phase | Feature                                         | Status       |
| ----- | ----------------------------------------------- | ------------ |
| 1     | PostgreSQL + Django Setup                       | ✅ Complete   |
| 2     | Custom User Model + Admin                       | ✅ Complete   |
| 3     | Problem Management + TestCases                  | ✅ Complete   |
| 4     | Auth (Register/Login/Logout)                    | ✅ Complete   |
| 5     | Code Execution Engine (subprocess)              | ✅ Complete   |
| 6     | Monaco Editor Integration                       | ✅ Complete   |
| 7     | Docker Isolation for Code Execution             | ✅ Complete   |
| 8     | Leaderboard System                              | ✅ Complete   |
| 9     | Contest Support (Modal UI, Submission Tracking) | ✅ Complete   |
| 10    | AI Debug Assistant                              | ✅ Integrated |
| 11    | EC2 Deployment (Proof of Concept)               | ✅ Complete   |

---

## Tech Stack

| Layer           | Technology                             |
| --------------- | -------------------------------------- |
| Backend         | Django 5.2                             |
| Database        | PostgreSQL 16                          |
| Code Execution  | Docker + Python `subprocess`           |
| Supported Langs | Python, C, C++, Java                   |
| Frontend        | Bootstrap 5, Custom CSS, JS, Fira Code |
| Editor          | Monaco Editor (via CDN)                |
| Admin Tools     | Django Admin + Frontend Modals         |
| File Handling   | `runs/`, `submissions/`, `docker_temp` |

---

## System Requirements

Ensure the following **tools are globally installed**:

| Language   | Toolchain       | Install Guide                                                                                         |
| ---------- | --------------- | ----------------------------------------------------------------------------------------------------- |
| Python     | `python3`       | [python.org](https://www.python.org/downloads/)                                                       |
| C          | `gcc`           | `apt install gcc` or [MinGW](https://www.mingw-w64.org/)                                              |
| C++        | `g++`           | Same as above                                                                                         |
| Java       | `javac`, `java` | [Adoptium](https://adoptium.net) or [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) |
| PostgreSQL | `psql`          | [postgresql.org](https://www.postgresql.org/download/)                                                |
| Docker     | `docker`        | [Docker Installation Guide](https://docs.docker.com/get-docker/)                                      |

### Check Installed Versions (Linux/macOS)

```bash
gcc --version
g++ --version
javac -version
java -version
psql --version
python3 --version
docker --version
````

### Check Installed Versions (Windows CMD)

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

## Local Development Setup

> Recommended: Use virtual environment

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

### Windows (CMD)

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

### Windows (PowerShell)

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

## Superuser Access

To manage users, problems, testcases, or contest verdicts:

```bash
python manage.py createsuperuser
```

Then visit:
 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

> Plus, in-app admin menus let staff users create/update problems or contests without needing the admin panel.

---

## Problem Structure

Each problem contains:

* `Title` and `Difficulty`
* `Description`, `Input Format`, `Output Format`
* `Constraints` (markdown supported)
* `Sample Input/Output`
* `Hidden TestCases`
* `Time` and `Memory` limits
* `Docker Enabled?` toggle

Problems can be added via:

*  AI Markdown Parsing
*  Admin Panel
*  Modal-based Quick Create (for contests)

---


##  AI Assistant

Integrated into the problem detail page, this tool:

* Analyzes user code
* Gives feedback, suggestions, and hints
* Detects logical errors or inefficiencies
* Is completely optional and toggleable

---

## Leaderboard

Track users based on difficulty-wise problems solved:

* Easy 
* Medium 
* Hard 

Ranks update live based on accepted submissions.

---

## Project Structure (Preview)

<details>
<summary>Click to expand</summary>

```bash
.
├── codeverse/             # Core Django project
├── judge/                # Main app: users, contests, AI, submissions
├── problems/             # Problem models, views, templates
├── core/utils/           # Code runner, executor logic
├── docker_runner/        # Dockerfile + run script
├── submission_files/     # File separation (runs, subs, temp)
├── static/               # CSS, JS, Monaco, logo
├── templates/            # Base + feature-specific HTML
├── README.md             # You’re reading it!
├── requirements.txt      # All Python packages
└── manage.py
```

</details>

---

## License

This project is for academic and learning purposes only.
Full Docker sandboxing is integrated for production-grade security.

---

## Maintainer

Built with passion by [@gsri-18](https://github.com/gsri-18)
Drop a ⭐ if you like CodeVerse!

---


