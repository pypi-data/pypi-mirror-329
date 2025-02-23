import logging
from sift_dev_logger import SiftDevConfig, SiftDevHandler

logger = logging.getLogger("test")
logger.setLevel(logging.INFO)
handler = SiftDevHandler(SiftDevConfig(
    otlp_endpoint="http://35.188.170.83:5301",
    sift_dev_ingest_key="test-key",
    service_name="test-logging-handler",
    service_instance_id="test-logging-handler-instance",
    env="test"
))
logger.addHandler(handler)
logger.info("Hello, world!")
