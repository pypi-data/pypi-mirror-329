import pytest

# Skip all tests in this module if Flask isn't installed
pytest.importorskip("flask")

from flask import Flask, jsonify, request
from sift_dev_logger import SiftDevConfig, configure, flask_logger
import logging
import json

@pytest.fixture
def app():
    app = Flask(__name__)
    config = SiftDevConfig(
        service_name="flask-app",
        service_instance_id="flask-app-1",
        otlp_endpoint="http://35.188.170.83:5301",
        sift_dev_ingest_key="your-sift-dev-ingest-key",
    )
    configure(config)

    # Instrument logging in the Flask app
    flask_logger(app)
    
    @app.route('/')
    def index():
        return jsonify(message="Hello, world!")
    
    @app.route("/error")
    def error():
        raise ValueError("Test error")
    
    @app.route("/echo", methods=['POST'])
    def echo():
        return jsonify(headers=dict(request.headers),
                      json=request.get_json())
    
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_flask_logging(app, caplog):
    client = app.test_client()
    with caplog.at_level(logging.INFO):
        response = client.get('/')
    # Check that the request was logged. caplog.records gives you LogRecord objects.
    assert response.status_code == 200
    # Here, you can check that a log record with expected keywords is present.
    assert any("GET /" in record.message for record in caplog.records) 

def test_successful_request(client, caplog):
    with caplog.at_level(logging.INFO):
        response = client.get('/')
        
    assert response.status_code == 200
    assert response.json == {"message": "Hello, world!"}
    
    # Check log record
    assert len(caplog.records) > 0
    record = caplog.records[-1]
    assert record.levelname == "INFO"
    assert "GET /" in record.message
    assert hasattr(record, "duration_ms")
    assert record.duration_ms > 0

def test_error_request(client, caplog):
    with caplog.at_level(logging.ERROR):
        response = client.get('/error')
        
    assert response.status_code == 500
    
    # Check error log - look for both logs
    error_records = [r for r in caplog.records if r.levelname == "ERROR"]
    assert len(error_records) > 0
    
    # First record should be the exception
    assert any("Exception on" in record.message for record in error_records)
    
    # Last record should be our completion message
    assert "GET /error 500 completed" in error_records[-1].message

def test_post_request_with_json(client, caplog):
    test_data = {"name": "test", "value": 123}
    with caplog.at_level(logging.INFO):
        response = client.post('/echo',
                             json=test_data,
                             headers={"Custom-Header": "test"})
    
    assert response.status_code == 200
    response_data = response.json
    
    # Verify response contains our data
    assert response_data["json"] == test_data
    assert response_data["headers"]["Custom-Header"] == "test"
    
    # Check log record
    record = caplog.records[-1]
    assert record.request_body == json.dumps(test_data)
    assert "Custom-Header" in record.request_headers

def test_large_request_body(client, caplog):
    large_data = {"data": "x" * 1000000}  # 1MB of data
    with caplog.at_level(logging.INFO):
        response = client.post('/echo', json=large_data)
    
    assert response.status_code == 200
    
    # Verify log record has truncated body
    record = caplog.records[-1]
    assert len(record.request_body) < 1000000
    assert "... (truncated)" in record.request_body 

def test_flask_logger(app):
    instrumented_app = flask_logger(app)
    assert instrumented_app is not None
    # Add more assertions 