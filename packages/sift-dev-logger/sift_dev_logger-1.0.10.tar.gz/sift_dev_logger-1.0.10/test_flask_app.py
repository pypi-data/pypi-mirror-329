from flask import Flask
from sift_dev_logger import SiftDevConfig, configure, flask_logger, getLogger
from dotenv import load_dotenv
import logging

load_dotenv()

config = SiftDevConfig(
    sift_dev_ingest_key="test-key",
    service_name="test-flask"
)

configure(config)  # This stores the config globally

app = Flask(__name__)

# Create and configure loggers
logger = getLogger("test")
logger2 = getLogger("test2")

flask_logger(app)  # Uses config from configure()

@app.route('/')
def hello():
    logger.info("Received request")
    logger2.info("Received request 2")
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, port=6000) 