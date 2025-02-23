import logging
from .config import SiftDevConfig
from .handlers import SiftDevHandler

# Module-level storage for current config
_current_config = None

def configure(config: SiftDevConfig) -> None:
    """
    Configure SiftDev logging with the given config.
    Must be called before using getLogger() if you want to configure that logger.
    """
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

def getLogger(name: str = "", extra: dict = None) -> logging.Logger:
    """Get a logger configured with SiftDev handler."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Only add handler if one isn't already present
    if not any(isinstance(h, SiftDevHandler) for h in logger.handlers):
        handler = SiftDevHandler(get_current_config())
        logger.addHandler(handler)
    
        # Create a custom Formatter class to handle extra attributes
        stream_handler = logging.StreamHandler()
        class CustomFormatter(logging.Formatter):
            # Standard LogRecord attributes that we want to exclude
            STANDARD_ATTRS = {
                'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
                'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated',
                'stack_info', 'thread', 'threadName', 'taskName'
            }
            
            def format(self, record):
                # Get only the custom extras (excluding standard LogRecord attributes)
                extras = {
                    key: value for key, value in record.__dict__.items()
                    if key not in self.STANDARD_ATTRS and not key.startswith('_')
                }
                
                # Only show extras if they exist
                if extras:
                    record.extras_str = str(extras)
                else:
                    record.extras_str = ''
                return super().format(record)
        
        formatter = CustomFormatter('%(levelname)s: %(message)s  %(extras_str)s')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    if extra:
        # Create custom adapter that properly merges extras
        class CustomAdapter(logging.LoggerAdapter):
            def __init__(self, logger, extra):
                super().__init__(logger, extra)
                
            def process(self, msg, kwargs):
                # Merge the adapter's extra with any extras passed to the log call
                if 'extra' in kwargs:
                    kwargs['extra'] = {**self.extra, **kwargs['extra']}
                else:
                    kwargs['extra'] = self.extra
                return msg, kwargs
        
        logger = CustomAdapter(logger, extra)
    
    return logger

def flush_logs():
    """
    Flush all outstanding logs from all handlers.
    
    This ensures any buffered logs are sent before the application exits.
    """
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if hasattr(handler, "flush"):
            handler.flush()