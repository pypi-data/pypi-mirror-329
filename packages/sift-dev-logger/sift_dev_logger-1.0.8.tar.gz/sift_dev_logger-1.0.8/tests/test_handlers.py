import pytest
import logging
from logging.config import dictConfig
from sift_dev_logger import SiftDevConfig, SiftDevHandler

@pytest.fixture(autouse=True)
def cleanup_logging():
    """Clean up logging configuration after each test"""
    yield
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        handler.close()
        root_logger.removeHandler(handler)
    logging.shutdown()

@pytest.fixture
def basic_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'json': {
                'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
            }
        },
        'handlers': {
            'siftdev': {
                '()': 'sift_dev_logger.handlers.SiftDevHandler.from_dict',
                'formatter': 'json',
                'level': 'INFO',
                'config': {
                    'service_name': 'test-service',
                    'service_instance_id': 'test-instance',
                    'otlp_endpoint': None  # Disable actual OTLP export for tests
                }
            }
        },
        'loggers': {
            'testapp': {
                'handlers': ['siftdev'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }

@pytest.fixture
def test_logger():
    """Create a test logger that's cleaned up after the test"""
    logger = logging.getLogger('test_logger')
    yield logger
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

def test_handler_creation():
    config = SiftDevConfig(
        service_name="test-service",
        service_instance_id="test-instance",
        otlp_endpoint=None  # Disable actual OTLP export for tests
    )
    handler = SiftDevHandler(config)
    assert isinstance(handler, logging.Handler)
    assert handler.level == logging.NOTSET
    handler.close()

def test_handler_from_dict(basic_config):
    dictConfig(basic_config)
    logger = logging.getLogger('testapp')
    
    # Verify handler was created and attached
    siftdev_handlers = [h for h in logger.handlers if isinstance(h, SiftDevHandler)]
    assert len(siftdev_handlers) == 1
    
    handler = siftdev_handlers[0]
    assert handler.formatter is not None
    assert isinstance(handler.formatter, logging.Formatter)

def test_handler_formatting(basic_config, caplog):
    dictConfig(basic_config)
    logger = logging.getLogger('testapp')
    
    with caplog.at_level(logging.INFO):
        logger.info("Test message", extra={'user': 'test_user'})
        
        for record in caplog.records:
            assert record.levelname == "INFO"
            assert "Test message" in record.message
            assert hasattr(record, 'user')
            assert record.user == 'test_user'

def test_multiple_handlers():
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO'
            },
            'siftdev1': {
                '()': 'sift_dev_logger.handlers.SiftDevHandler.from_dict',
                'level': 'INFO',
                'config': {
                    'service_name': 'service-1',
                    'service_instance_id': 'instance-1',
                    'otlp_endpoint': None
                }
            },
            'siftdev2': {
                '()': 'sift_dev_logger.handlers.SiftDevHandler.from_dict',
                'level': 'DEBUG',
                'config': {
                    'service_name': 'service-2',
                    'service_instance_id': 'instance-2',
                    'otlp_endpoint': None
                }
            }
        },
        'loggers': {
            'multiapp': {
                'handlers': ['console', 'siftdev1', 'siftdev2'],
                'level': 'DEBUG',
            }
        }
    }
    
    dictConfig(config)
    logger = logging.getLogger('multiapp')
    
    handlers = logger.handlers
    assert len(handlers) == 3
    assert len([h for h in handlers if isinstance(h, SiftDevHandler)]) == 2
    assert len([h for h in handlers if isinstance(h, logging.StreamHandler)]) == 1

def test_handler_levels(caplog, test_logger):
    config = SiftDevConfig(
        service_name="test-service",
        service_instance_id="test-instance",
        otlp_endpoint=None
    )
    handler = SiftDevHandler(config)
    test_logger.addHandler(handler)
    
    with caplog.at_level(logging.INFO):
        # Set handler to INFO
        handler.setLevel(logging.INFO)
        
        # DEBUG shouldn't be logged
        test_logger.debug("Debug message")
        assert not any("Debug message" in r.message for r in caplog.records)
        
        # INFO should be logged
        test_logger.info("Info message")
        assert any("Info message" in r.message for r in caplog.records)

def test_handler_flush_and_close():
    config = SiftDevConfig(
        service_name="test-service",
        service_instance_id="test-instance",
        otlp_endpoint=None
    )
    handler = SiftDevHandler(config)
    
    handler.flush()
    handler.close() 