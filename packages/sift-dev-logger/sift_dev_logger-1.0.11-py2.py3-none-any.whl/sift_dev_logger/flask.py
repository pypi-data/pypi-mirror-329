try:
    from flask import Flask, request, g, Response
except ImportError:
    raise ImportError(
        "Flask is not installed. Please install it with 'pip install sift-dev-logger[flask]'"
    )
import time
import uuid
import logging
from .handlers import SiftDevHandler
from .config import SiftDevConfig
from .common import get_current_config
from typing import Set, List

def flask_logger(
    app: Flask,
    config: SiftDevConfig = None,  # Default to None
    max_body_size: int = 100_000,
    ignored_paths: Set[str] = set(),
    additional_handlers: List[logging.Handler] = [],
):
    """
    Configure Flask application logging with SiftDev handler.
    
    Args:
        app: Flask application instance
        config: SiftDevConfig for logging configuration
        max_body_size: Maximum size of request/response bodies to log
        ignored_paths: Set of paths to ignore for logging
    """
    if config is None:
        config = get_current_config()
    
    # Create our internal logger with a clear name
    logger = logging.getLogger('sift_dev.flask')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    # Configure with SiftDev handler
    handler = SiftDevHandler(config)
    logger.addHandler(handler)
    for handler in additional_handlers:
        if isinstance(handler, logging.Handler):
            logger.addHandler(handler)
        else:
            logger.warning(f"Handler {handler} is not a valid logging.Handler")
    
    # Rest of the request logging middleware setup...
    @app.before_request
    def start_timer():
        if request.path in ignored_paths:
            return
        g.start_time = time.time()
        try:
            data = request.get_data()
            if len(data) > max_body_size:
                g.request_body = data[:max_body_size] + b"... (truncated)"
            else:
                g.request_body = data
        except Exception as e:
            logger.warning(f"Failed to capture request body: {str(e)}")
            g.request_body = b""
        g.request_id = str(uuid.uuid4())

    @app.after_request
    def log_request(response: Response):
        if request.path in ignored_paths:
            return response

        duration_ms = (time.time() - g.start_time) * 1000 if hasattr(g, "start_time") else 0

        try:
            request_body = g.request_body if hasattr(g, "request_body") else b""
            request_body_str = request_body.decode('utf-8', errors="replace")
        except Exception:
            request_body_str = "<binary>"

        try:
            response_body_bytes = response.get_data()
            if len(response_body_bytes) > max_body_size:
                response_body_str = response_body_bytes[:max_body_size].decode('utf-8', errors="replace") + "... (truncated)"
            else:
                response_body_str = response_body_bytes.decode('utf-8', errors="replace")
        except Exception:
            response_body_str = "<binary>"

        # All request data available as extra fields for formatters
        extra = {
            "request_id": g.request_id if hasattr(g, "request_id") else "",
            "client_addr": request.remote_addr or "unknown",
            "route": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "request_headers": dict(request.headers),
            "response_headers": dict(response.headers),
            "request_body": request_body_str,
            "response_body": response_body_str,
            "query_params": dict(request.args),
        }

        # Use ERROR level for 5xx responses
        level = logging.ERROR if response.status_code >= 500 else logging.INFO
        logger.log(
            level, 
            f"{request.method} {request.path} {response.status_code} completed in {duration_ms:.2f}ms",
            extra=extra
        )
        return response

    return app

# For backwards compatibility
instrument_logging_middleware = flask_logger