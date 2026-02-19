# Root-level WSGI entry point for Render / gunicorn
# Render auto-detects this file and runs: gunicorn app:app
from classdoodle.web_app import app  # noqa: F401

if __name__ == "__main__":
    app.run()
