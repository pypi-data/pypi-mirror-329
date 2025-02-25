import logging
from sift_dev_logger import SiftDevConfig, configure, getLogger

def test_get_logger_returns_logger():
    logger = getLogger("test_logger")
    assert isinstance(logger, logging.Logger)
    # When extra is provided, we expect a LoggerAdapter to be returned.
    logger_with_extra = getLogger("test_logger", extra={"key": "value"})
    from logging import LoggerAdapter
    assert isinstance(logger_with_extra, LoggerAdapter)

def test_logger_creation():
    logger = getLogger("test")
    assert logger.name == "test"

def test_configuration():
    config = SiftDevConfig(sift_dev_ingest_key="test", service_name="test")
    configure(config)
    assert config.sift_dev_ingest_key == "test"
    assert config.service_name == "test"
