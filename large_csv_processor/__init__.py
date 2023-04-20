"""
    Ensures Celery app is loaded when Django is started.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
