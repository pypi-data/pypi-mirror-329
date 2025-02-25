from sift_dev_logger import getLogger, configure, SiftDevConfig
import logging

configure(SiftDevConfig(
    otlp_endpoint="http://35.188.170.83:5301",
))
logger = getLogger(name="test", extra={"extra-early": "extra-early-val"})
oglogger = logging.getLogger("test")
oglogger.info("Hello, world but from the old logger!")

logger = getLogger("test", extra={"extra-early": "extra-early-val"})
complex_extra = {
    "user": {
        "id": 123,
        "details": {
            "name": "John Doe",
            "role": "admin"
        }
    },
    "request": {
        "path": "/api/v1/users",
        "method": "POST",
        "headers": {
            "content-type": "application/json",
            "x-request-id": "abc-123"
        }
    },
    "metadata": {
        "timestamp": 1698765432,
        "environment": "staging"
    }
}
logger.info("Hello, world from sift_dev_logger!", extra=complex_extra)
logger.info("Hello, world from sift_dev_logger again!", extra={
    "user": "bob",
    "ip": "10.0.0.1",
    "action": "login",
    "session_id": "123"  # Additional attributes are included
})

from test_only_logger2 import test_second_logger
test_second_logger()