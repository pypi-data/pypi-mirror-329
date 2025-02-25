import logging
from sift_dev_logger import SiftDevConfig, SiftDevHandler, configure

logger = logging.getLogger("test")
logger.setLevel(logging.INFO)
configure(SiftDevConfig(
    otlp_endpoint="http://88d1ef6c-3709-48b9-9441-399b323050f8.app.trysift.dev:5301",
    sift_dev_ingest_key="test-key",
    service_name="test-logging-handler",
    service_instance_id="test-logging-handler-instance",
    env="test"
))
handler = SiftDevHandler()
logger.addHandler(handler)
logger.info("Hello, world!")
