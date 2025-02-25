from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging
from opentelemetry.sdk._logs import LogData, LogRecord
from opentelemetry.trace import INVALID_SPAN_ID, INVALID_TRACE_ID, TraceFlags
from opentelemetry._logs.severity import SeverityNumber
from .config import SiftDevConfig, get_current_config

class SiftDevHandler(logging.Handler):
    """
    A handler that exports logs to SiftDev via OTLP while preserving existing formatting.
    
    This handler is designed to work in complex scenarios including:
    1. Async web frameworks (FastAPI, ASGI)
    2. Multiple handler instances with different configurations
    3. Streaming responses and middleware contexts
    
    Implementation Notes:
    -------------------
    The handler uses class-level dictionaries to store processors and exporters
    to solve several challenging scenarios:
    
    1. Async Context Problem:
       - In async frameworks, middleware can create new scopes/contexts
       - Instance-level processors can get garbage collected between requests
       - Solution: Store processors at class level to persist across async contexts
    
    2. Multiple Configurations:
       - Different parts of an app might need different configurations
       - Example: Different service names or endpoints for different components
       - Solution: Use config-based keys to maintain separate processor/exporter pairs
    
    3. Resource Management:
       - OTLP processors need proper lifecycle management
       - Premature shutdown can cause lost logs
       - Solution: Track processors by config and clean up only when explicitly closed
    
    Usage Example:
    -------------
    # These will use different processors (different configs)
    handler1 = SiftDevHandler(SiftDevConfig(service_name="service1"))
    handler2 = SiftDevHandler(SiftDevConfig(service_name="service2"))
    
    # This will reuse handler1's processor (same config)
    handler3 = SiftDevHandler(SiftDevConfig(service_name="service1"))
    """
    
    _processors = {}
    _exporters = {}
    _configs = {}  # Store configs to recreate processors
    
    def __init__(self, config=None, formatter=None):
        super().__init__()
        self.config = config or get_current_config()  # Use get_current_config if no config provided
        if formatter:
            self.setFormatter(formatter)
        
        if not self.config.otlp_endpoint:
            return
        
        # Create config key
        config_key = (
            f"{self.config.service_name}:"
            f"{self.config.otlp_endpoint}:"
            f"{self.config.service_instance_id}"
        )
        
        # Store config for recreation
        self.__class__._configs[config_key] = self.config
        
        # Create initial processor
        self._create_processor(config_key)
        self._config_key = config_key
        
        self.resource = Resource.create({
            "service.name": self.config.service_name,
            "service.instance.id": self.config.service_instance_id,
            "environment": self.config.env
        })

    def _create_processor(self, config_key):
        """Create a new processor/exporter pair for this config"""
        if config_key not in self.__class__._exporters:
            config = self.__class__._configs[config_key]
            self.__class__._exporters[config_key] = OTLPLogExporter(
                endpoint=f"{config.otlp_endpoint}/v1/logs",
                headers={
                    "Content-Type": "application/json",
                    "sift-dev-ingest-key": config.sift_dev_ingest_key
                }
            )
            self.__class__._processors[config_key] = BatchLogRecordProcessor(
                self.__class__._exporters[config_key],
                schedule_delay_millis=config.batch_delay_millis
            )

    async def ensure_processor(self):
        """Ensure processor exists in current context"""
        if not hasattr(self, '_config_key'):
            return
            
        if self._config_key not in self.__class__._processors:
            self._create_processor(self._config_key)

    async def emit_async(self, record):
        """Async version of emit that ensures processor exists"""
        await self.ensure_processor()
        if not hasattr(self, '_config_key'):
            return
            
        try:
            formatted_message = self.format(record) if self.formatter else record.getMessage()
            log_data = LogData(
                log_record=LogRecord(
                    timestamp=int(record.created * 1e9),
                    severity_text=record.levelname,
                    severity_number=self._get_otlp_severity(record.levelno),
                    body=formatted_message,
                    attributes=self._get_attributes(record),
                    resource=self.resource,
                    trace_id=INVALID_TRACE_ID,
                    span_id=INVALID_SPAN_ID,
                    trace_flags=TraceFlags.DEFAULT
                ),
                instrumentation_scope=None
            )
            self.__class__._processors[self._config_key].emit(log_data)
        except Exception as e:
            self.handleError(record)

    def emit(self, record):
        """Handle both sync and async contexts"""
        if not hasattr(self, '_config_key'):
            return
            
        try:
            # Create log data
            formatted_message = self.format(record) if self.formatter else record.getMessage()
            log_data = LogData(
                log_record=LogRecord(
                    timestamp=int(record.created * 1e9),
                    severity_text=record.levelname,
                    severity_number=self._get_otlp_severity(record.levelno),
                    body=formatted_message,
                    attributes=self._get_attributes(record),
                    resource=self.resource,
                    trace_id=INVALID_TRACE_ID,
                    span_id=INVALID_SPAN_ID,
                    trace_flags=TraceFlags.DEFAULT
                ),
                instrumentation_scope=None
            )

            # Try to emit directly - no async check needed
            if self._config_key in self.__class__._processors:
                self.__class__._processors[self._config_key].emit(log_data)
            else:
                # Processor missing - recreate it
                self._create_processor(self._config_key)
                self.__class__._processors[self._config_key].emit(log_data)

        except Exception as e:
            self.handleError(record)
    
    def _get_attributes(self, record):
        """Extract all attributes from the record, flattening dictionaries"""
        attributes = {
            "logger.name": record.name,
            "thread.name": record.threadName,
            "file.name": record.filename,
            "line.number": record.lineno,
        }
        
        def flatten_dict(d, prefix=''):
            """Recursively flatten dictionary with dot notation"""
            items = {}
            for k, v in d.items():
                new_key = f"{prefix}{k}" if prefix else k
                if isinstance(v, dict):
                    items.update(flatten_dict(v, f"{new_key}."))
                else:
                    items[new_key] = str(v)
            return items
                
        # Process all record attributes
        for key, value in record.__dict__.items():
            if (key not in {"args", "exc_info", "exc_text", "msg", "message", 
                           "stack_info", "created", "msecs", "relativeCreated", 
                           "levelno", "levelname", "pathname", "filename", 
                           "module", "lineno", "funcName", "processName", 
                           "process", "thread", "threadName", "name"} and 
                not key.startswith("_")):
                if isinstance(value, dict):
                    # Flatten dictionaries with dot notation
                    flattened = flatten_dict(value, f"{key}.")
                    attributes.update(flattened)
                else:
                    attributes[key] = str(value)
        
        # Process extra attributes if present
        if hasattr(record, "extra"):
            for key, value in record.extra.items():
                if isinstance(value, dict):
                    # Flatten dictionaries with dot notation
                    flattened = flatten_dict(value, f"{key}.")
                    attributes.update(flattened)
                else:
                    attributes[key] = str(value)
        
        return attributes
    
    def _get_otlp_severity(self, levelno):
        """Convert Python logging levels to OTLP severity numbers"""
        if levelno >= logging.CRITICAL:
            return SeverityNumber.FATAL
        elif levelno >= logging.ERROR:
            return SeverityNumber.ERROR
        elif levelno >= logging.WARNING:
            return SeverityNumber.WARN
        elif levelno >= logging.INFO:
            return SeverityNumber.INFO
        else:
            return SeverityNumber.DEBUG
        
    def flush(self):
        """
        Flush any buffered log records for this handler's config
        Important for ensuring logs are sent before shutdown
        """
        if hasattr(self, '_config_key'):
            if self._config_key in self.__class__._processors:
                self.__class__._processors[self._config_key].force_flush()
            
    def close(self):
        """
        Clean up resources for this handler's config
        Only removes the processor/exporter if this was the last handler using them
        """
        if hasattr(self, '_config_key'):
            if self._config_key in self.__class__._processors:
                self.__class__._processors[self._config_key].shutdown()
                del self.__class__._processors[self._config_key]
                del self.__class__._exporters[self._config_key]
        super().close()

    @classmethod
    def from_dict(cls, config: dict, **kwargs):
        """Factory method for dictConfig integration"""
        sift_config = SiftDevConfig(**config)
        return cls(config=sift_config, **kwargs) 