import pytest

# Skip all tests in this module if FastAPI isn't installed
pytest.importorskip("fastapi")

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from sift_dev_logger import SiftDevConfig, configure, fastapi_logger
import logging
import json
import time

@pytest.fixture
def app():
    app = FastAPI()
    
    config = SiftDevConfig(
        service_name="fastapi-app",
        service_instance_id="fastapi-app-1",
        otlp_endpoint="http://35.188.170.83:5301",
        sift_dev_ingest_key="your-sift-dev-ingest-key",
    )
    configure(config)
    
    logger = logging.getLogger("fastapi.access")
    fastapi_logger(app)
    
    @app.get("/")
    async def index():
        return {"message": "Hello, World!"}
    
    @app.get("/error")
    async def error():
        # Log the error before raising
        logger.error("Test error occurred", extra={"error": "Test error"})
        raise ValueError("Test error")
    
    @app.post("/echo")
    async def echo(request: Request):
        body = await request.json()
        return {
            "headers": dict(request.headers),
            "json": body
        }
    
    @app.get("/slow")
    async def slow():
        time.sleep(1)  # Simulate slow response
        return {"message": "Slow response"}
    
    @app.post("/users")
    async def create_user(request: Request):
        body = await request.json()
        return JSONResponse(
            status_code=201,
            content={"id": 123, **body}
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        # Log the error in the exception handler
        logger.error(f"Error handling request: {str(exc)}", 
                    extra={"error": str(exc)})
        return JSONResponse(
            status_code=500,
            content={"error": str(exc)}
        )
    
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_successful_request(client, caplog):
    with caplog.at_level(logging.INFO, logger="sift_dev.fastapi"):  # Specify logger name
        response = client.get("/")
        
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
    
    # Find our middleware's log record (not httpx's internal logs)
    records = [r for r in caplog.records if r.name == "sift_dev.fastapi"]
    assert len(records) > 0
    record = records[-1]
    
    assert record.levelname == "INFO"
    assert "GET /" in record.message
    assert hasattr(record, "duration_ms")
    assert record.duration_ms > 0

def test_error_request(client, caplog):
    with caplog.at_level(logging.ERROR, logger="sift_dev.fastapi"):
        response = client.get("/error")
    
    assert response.status_code == 500
    assert response.json() == {"error": "Test error"}
    
    records = [r for r in caplog.records if r.name == "sift_dev.fastapi"]
    assert len(records) > 0
    record = records[-1]
    assert "GET /error" in record.message
    
    # The error might be in different attributes depending on how it's logged
    error_present = any([
        "Test error" in record.__dict__.get("error", ""),
        "Test error" in getattr(record, "exception", ""),
        "Test error" in record.message,
        "Test error" in str(record.exc_info) if record.exc_info else ""
    ])
    assert error_present, "Error message not found in log record"

def test_post_request_with_json(client, caplog):
    test_data = {"name": "test", "value": 123}
    with caplog.at_level(logging.INFO, logger="sift_dev.fastapi"):
        response = client.post(
            "/echo",
            json=test_data,
            headers={"Custom-Header": "test"}
        )
    
    assert response.status_code == 200
    response_data = response.json()
    
    # Verify response contains our data
    assert response_data["json"] == test_data
    assert response_data["headers"]["custom-header"] == "test"  # FastAPI normalizes header names
    
    # Find our middleware's log record (not httpx's internal logs)
    records = [r for r in caplog.records if r.name == "sift_dev.fastapi"]
    assert len(records) > 0
    record = records[-1]
    
    # Normalize JSON strings before comparing
    actual_json = json.loads(record.request_body)
    expected_json = test_data
    assert actual_json == expected_json

def test_large_request_body(client, caplog):
    large_data = {"data": "x" * 1000000}  # 1MB of data
    with caplog.at_level(logging.INFO, logger="sift_dev.fastapi"):
        response = client.post("/echo", json=large_data)
    
    assert response.status_code == 200
    
    # Find our middleware's log record (not httpx's internal logs)
    records = [r for r in caplog.records if r.name == "sift_dev.fastapi"]
    assert len(records) > 0
    record = records[-1]
    
    # Verify log record has truncated body
    assert len(record.request_body) < 1000000
    assert "... (truncated)" in record.request_body

def test_slow_request_timing(client, caplog):
    with caplog.at_level(logging.INFO, logger="sift_dev.fastapi"):
        response = client.get("/slow")
    
    assert response.status_code == 200
    
    # Find our middleware's log record (not httpx's internal logs)
    records = [r for r in caplog.records if r.name == "sift_dev.fastapi"]
    assert len(records) > 0
    record = records[-1]
    
    # Check timing information
    assert record.duration_ms >= 1000  # Should be at least 1 second

def test_status_code_tracking(client, caplog):
    with caplog.at_level(logging.INFO, logger="sift_dev.fastapi"):
        response = client.post("/users", json={"name": "test"})
    
    assert response.status_code == 201
    
    # Find our middleware's log record (not httpx's internal logs)
    records = [r for r in caplog.records if r.name == "sift_dev.fastapi"]
    assert len(records) > 0
    record = records[-1]
    
    # Verify status code is logged
    assert record.status_code == 201
    assert "201" in record.message

def test_ignored_paths(client, caplog):
    app = FastAPI()
    fastapi_logger(app, ignored_paths={"/health", "/metrics"}) 
    
    @app.get("/health")
    async def health():
        return {"status": "ok"}
    
    test_client = TestClient(app)
    
    with caplog.at_level(logging.INFO, logger="sift_dev.fastapi"):
        response = test_client.get("/health")
    
    assert response.status_code == 200
    # Verify that the ignored path wasn't logged
    records = [r for r in caplog.records if r.name == "sift_dev.fastapi"]
    assert not any("/health" in record.message for record in records)

def test_fastapi_logger(app):
    instrumented_app = fastapi_logger(app)
    assert instrumented_app is not None
    # Add more assertions 