# Root-level WSGI entry point for Render / gunicorn
# Adds classdoodle/ to sys.path so 'from backend.api import ...' resolves
import sys
import os

# Insert the classdoodle folder so web_app.py's relative imports work
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classdoodle'))
# Also ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import web_app  # noqa: E402  (imported after sys.path setup)
app = web_app.app

if __name__ == "__main__":
    app.run()
