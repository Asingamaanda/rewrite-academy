# Rewrite Academy — ClassDoodle Portal

A Flask-based student management and learning portal for Rewrite Academy.

## Features
- **Admin portal** — manage students, attendance, assessments, payments, subject content, video library
- **Student portal** — view subjects, timetable, progress, and learning resources
- Role-based login (admin / student)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/Asingamaanda/rewrite-academy.git
cd rewrite-academy

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python classdoodle/web_app.py
```

Open `http://localhost:5000` in your browser.

## Default Login
| Role | Username | Password |
|------|----------|----------|
| Admin/Teacher | `admin` | `Classdoodle@password` |
| Student | _student ID_ | _set via admin panel_ |

## Stack
- Python 3.13 + Flask 3.1
- SQLite (local database)
- Jinja2 templates
- Vanilla CSS (custom design system)
