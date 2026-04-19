"""Vercel serverless entry point.

Vercel's @vercel/python runtime looks for a module-level WSGI `app` in this file.
We simply import the Flask app created in app.py at the project root.
"""
import os
import sys

# Make the project root importable (models.py, routes.py, auth.py, config.py live there)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app  # noqa: E402  (imported after sys.path tweak)

# Vercel picks up this variable automatically
application = app
