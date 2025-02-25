from sift_dev_logger import SiftDevConfig, configure, getLogger
from dotenv import load_dotenv
load_dotenv()

# Test basic logging
config = SiftDevConfig(
    service_name="test-service",
    service_instance_id="test-1"
)
configure(config)

logger = getLogger("test")
logger.info("Basic logging works!")

# Test Flask integration (if installed)
try:
    from flask import Flask
    from sift_dev_logger import flask_logger
    
    app = Flask(__name__)
    flask_logger(app)
    print("✅ Flask integration works!")
except ImportError:
    print("⚠️ Flask not installed")

# Test FastAPI integration (if installed)
try:
    from fastapi import FastAPI
    from sift_dev_logger import fastapi_logger
    
    app = FastAPI()
    fastapi_logger(app)
    print("✅ FastAPI integration works!")
except ImportError:
    print("⚠️ FastAPI not installed")

print("🎉 Installation test complete!") 