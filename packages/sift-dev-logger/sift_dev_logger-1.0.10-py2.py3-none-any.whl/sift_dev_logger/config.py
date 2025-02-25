from typing import Optional
import os

# Module-level storage for current config
_current_config = None

class SiftDevConfig:
    """Initialize SiftDev configuration with values from args or environment."""
    def __init__(
        self,
        service_name: str = None,
        service_instance_id: str = None,
        otlp_endpoint: Optional[str] = None,
        sift_dev_ingest_key: Optional[str] = None,
        env: str = None,
        batch_delay_millis: int = 5000,
    ):
        self.service_name = service_name or os.getenv("SIFT_DEV_SERVICE_NAME", "python-app")
        self.service_instance_id = service_instance_id or os.getenv("SIFT_DEV_SERVICE_INSTANCE_ID", "instance-1")
        self.otlp_endpoint = otlp_endpoint or os.getenv("OTLP_ENDPOINT")
        self.sift_dev_ingest_key = sift_dev_ingest_key or os.getenv("SIFT_DEV_INGEST_KEY")
        self.env = env or os.getenv("ENV", "unspecified")
        self.batch_delay_millis = batch_delay_millis
        self.validate_config()
    
    def validate_config(self):
        """Validate configuration and emit appropriate warnings."""
        from warnings import warn
        if not self.otlp_endpoint:
            warn("OTLP endpoint not provided. OTLP handler & logging will be disabled.", stacklevel=2)
        elif not self.sift_dev_ingest_key:
            warn("Sift Dev ingest key not provided. If using Sift Dev, please set the SIFT_DEV_INGEST_KEY environment variable.", stacklevel=2)

def configure(config: SiftDevConfig) -> None:
    """Configure SiftDev logging with the given config."""
    global _current_config
    _current_config = config

def get_current_config() -> SiftDevConfig:
    """
    Get the current SiftDev configuration.
    Returns a new default config if configure() hasn't been called.
    """
    global _current_config
    if _current_config is None:
        _current_config = SiftDevConfig()  # Create default config
    return _current_config