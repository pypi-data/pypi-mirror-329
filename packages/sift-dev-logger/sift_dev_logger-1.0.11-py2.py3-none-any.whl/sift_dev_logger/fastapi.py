try:
    from fastapi import FastAPI, Request
    from fastapi.responses import StreamingResponse
except ImportError:
    raise ImportError(
        "FastAPI is not installed. Please install it with 'pip install sift-dev-logger[fastapi]'"
    )
import logging
import time
import uuid
from .handlers import SiftDevHandler
from .config import SiftDevConfig
from .common import get_current_config
from typing import Set, List

def fastapi_logger(
    app: FastAPI,
    config: SiftDevConfig = None,  # Default to None
    max_body_size: int = 100_000,
    ignored_paths: Set[str] = set(),
    capture_request_body: bool = True,
    capture_response_body: bool = False,
    additional_handlers: List[logging.Handler] = [],
):
    """
    Configure FastAPI application logging with SiftDev handler.
    
    Args:
        app: FastAPI application instance
        config: SiftDevConfig for logging configuration
        max_body_size: Maximum size of request/response bodies to log
        ignored_paths: Set of paths to ignore for logging
    """
    if config is None:
        config = get_current_config()
        
    logger = logging.getLogger("sift_dev.fastapi")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    sift_dev_handler = SiftDevHandler(config)
    logger.addHandler(sift_dev_handler)
    for handler in additional_handlers:
        
        if isinstance(handler, logging.Handler):
            logger.addHandler(handler)
        else:
            logger.warning(f"Handler {handler} is not a valid logging.Handler")

    def log_request(logger, level, method, path, status_code, duration_ms, extra):
        """Centralized logging function"""
        # Ensure extra is a dict
        extra = extra or {}
        message = f"{method} {path} {status_code} completed in {duration_ms:.2f}ms"
        
        # If there's an error, include it in the log record
        if status_code >= 500 and not extra.get("error"):
            extra["error"] = "Internal Server Error"
        
        logger.log(level, message, extra=extra)
        sift_dev_handler.flush()

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        if request.url.path in ignored_paths:
            return await call_next(request)
        
        request_id = str(uuid.uuid4())
        start_time = time.time()
        client_addr = request.client.host if request.client else "unknown"

        # Capture request body if enabled
        request_body_str = "[Request body capture disabled]"
        if capture_request_body:
            try:
                body = await request.body()
                if len(body) > max_body_size:
                    request_body = body[:max_body_size] + b"... (truncated)"
                else:
                    request_body = body
                request_body_str = request_body.decode('utf-8', errors='replace')
            except Exception as e:
                request_body = b""
                request_body_str = "[Could not capture request body]"
                logger.warning(f"Failed to capture request body: {str(e)}")
            

        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000

            # Get response body if enabled
            response_body_str = "[Response body capture disabled]"
            if capture_response_body:
                if hasattr(response, "body_iterator"):
                    # Handle streaming responses
                    chunks = []
                    async def capture_response():
                        nonlocal chunks, response_body_str
                        async for chunk in response.body_iterator:
                            chunks.append(chunk)
                            yield chunk
                        try:
                            response_body_str = b"".join(chunks).decode('utf-8', errors='replace')
                            # Ensure processor exists before logging
                            for handler in logger.handlers:
                                if isinstance(handler, SiftDevHandler):
                                    await handler.ensure_processor()
                            extra = {
                                "request_id": request_id,
                                "client_addr": client_addr,
                                "method": request.method,
                                "path": request.url.path,
                                "status_code": response.status_code,
                                "duration_ms": duration_ms,
                                "request_headers": dict(request.headers),
                                "response_headers": dict(response.headers),
                                "request_body": request_body_str,
                                "response_body": response_body_str,
                                "query_params": dict(request.query_params),
                                "error": None
                            }
                            level = logging.ERROR if response.status_code >= 500 else logging.INFO
                            log_request(
                                logger, level, 
                                request.method, request.url.path, 
                                response.status_code, duration_ms,
                                extra
                            )
                        except Exception:
                            response_body_str = "[Binary streaming response]"
                    return StreamingResponse(
                        capture_response(),
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type
                    )
                else:
                    # Handle regular responses
                    try:
                        body = await response.body()
                        response_body_str = body.decode('utf-8', errors='replace')
                    except Exception:
                        response_body_str = "[Could not capture response body]"

            # Log the request/response
            level = logging.ERROR if response.status_code >= 500 else logging.INFO

            extra = {
                "request_id": request_id,
                "client_addr": client_addr,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "request_headers": dict(request.headers),
                "response_headers": dict(response.headers),
                "request_body": request_body_str,
                "response_body": response_body_str,
                "query_params": dict(request.query_params),
                "error": None
            }
            
            log_request(
                logger, level, 
                request.method, request.url.path, 
                response.status_code, duration_ms,
                extra
            )
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "request_id": request_id,
                    "client_addr": client_addr,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                    "request_headers": dict(request.headers),
                    "request_body": request_body_str,
                    "error": str(e)
                }
            )
            log_request(
                logger, logging.ERROR,
                request.method, request.url.path,
                500, duration_ms,
                extra={
                    "error": str(e)
                }
            )
            raise
    
    return app

# For backwards compatibility
instrument_logging_middleware = fastapi_logger
