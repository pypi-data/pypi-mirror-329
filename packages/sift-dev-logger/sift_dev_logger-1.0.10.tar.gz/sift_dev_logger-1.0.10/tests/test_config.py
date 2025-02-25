from sift_dev_logger import configure, get_current_config as get_config, SiftDevConfig
import os

def test_default_config_from_env(monkeypatch):
    # Set environment variables temporarily:
    monkeypatch.setenv("OTLP_ENDPOINT", "http://localhost:4317")
    monkeypatch.setenv("SIFT_DEV_INGEST_KEY", "test-key")
    
    config = SiftDevConfig()
    # If no values are passed, it should read from ENV
    assert config.otlp_endpoint == "http://localhost:4317"
    assert config.sift_dev_ingest_key == "test-key"

def test_config_override():
    custom_config = SiftDevConfig(
        service_name="test-service",
        otlp_endpoint="http://custom-endpoint",
        sift_dev_ingest_key="custom-key",
        env="testing",
        batch_delay_millis=2000,
    )
    configure(custom_config)
    config = get_config()
    assert config.service_name == "test-service"
    assert config.otlp_endpoint == "http://custom-endpoint"
    assert config.sift_dev_ingest_key == "custom-key"
    assert config.env == "testing"
    assert config.batch_delay_millis == 2000 