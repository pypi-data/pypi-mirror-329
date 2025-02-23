from sift_dev_logger import getLogger, SiftDevConfig, configure

def test_basic_logger():
    logger = getLogger("test")
    assert logger is not None
    assert logger.name == "test"

def test_config():
    config = SiftDevConfig(
        sift_dev_ingest_key="test-key",
        service_name="test-service"
    )
    configure(config)
    assert config.sift_dev_ingest_key == "test-key"
    assert config.service_name == "test-service" 