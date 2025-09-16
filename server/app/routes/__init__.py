"""
This module initializes the FastAPI routes for the application.
It exports all route modules for easy access.
"""

from .chats import router as chats_router
from .messages import router as messages_router
from .users import router as users_router
