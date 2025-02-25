from .common import getLogger, flush_logs
from .config import SiftDevConfig, get_current_config, configure
from .handlers import SiftDevHandler

def flask_logger(*args, **kwargs):
    """Flask logging middleware."""
    try:
        from .flask import flask_logger as _flask_logger
        return _flask_logger(*args, **kwargs)
    except ImportError:
        print("Error: Flask dependencies not installed. Run: pip install 'sift-dev-logger[flask]' to use Flask logging middleware.")
        return None

def fastapi_logger(*args, **kwargs):
    """FastAPI logging middleware."""
    try:
        from .fastapi import fastapi_logger as _fastapi_logger
        return _fastapi_logger(*args, **kwargs)
    except ImportError:
        print("Error: FastAPI dependencies not installed. Run: pip install 'sift-dev-logger[fastapi]' to use FastAPI logging middleware.")
        return None

__all__ = [
    # Core functionality
    'configure',
    'getLogger',
    'flush_logs',
    'get_current_config',
    'SiftDevConfig',
    'SiftDevHandler',
    
    # Framework integrations
    'flask_logger',
    'fastapi_logger',
]

# Version info
__version__ = "1.0.9"