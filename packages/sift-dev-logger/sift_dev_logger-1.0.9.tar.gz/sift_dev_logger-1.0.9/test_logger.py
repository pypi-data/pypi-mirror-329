# from fastapi import FastAPI
# from flask import Flask
# from sift_dev_logger.config import SiftDevConfig, configure
# from sift_dev_logger.fastapi import fastapi_logger
# from sift_dev_logger.flask import flask_logger

# # Test FastAPI integration
# app_fastapi = FastAPI()
# fastapi_logger(app_fastapi)
# print("✅ FastAPI integration works!")

# # Test Flask integration
# app_flask = Flask(__name__)
# flask_logger(app_flask)
# print("✅ Flask integration works!")

# # Test basic logging
# config = SiftDevConfig(
#     service_name="test-service",
#     service_instance_id="test-1"
# )
# configure(config)
# print("✅ Configuration works!")

# print("🎉 All imports and basic setup successful!") 

from fastapi import FastAPI
from flask import Flask, jsonify
from sift_dev_logger.config import SiftDevConfig, configure
from sift_dev_logger.fastapi import fastapi_logger
from sift_dev_logger.flask import flask_logger
import logging
import uvicorn
from threading import Thread
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)
load_dotenv()

# Configure Sift logger
config = SiftDevConfig(
    # otlp_endpoint="http://88d1ef6c-3709-48b9-9441-399b323050f8.app.trysift.dev:5301/",
    # sift_dev_ingest_key="fake-key-val",
    service_name="test-service",
    service_instance_id="test-1",
    capture_response_body=True
)
configure(config)

# FastAPI app
app_fastapi = FastAPI()
fastapi_logger(app_fastapi)

@app_fastapi.get("/fastapi/hello")
async def fastapi_hello():
    logger.info("Received request on FastAPI endpoint")
    return {"message": "Hello from FastAPI!"}

@app_fastapi.get("/fastapi/error")
async def fastapi_error():
    logger.error("This is a test error in FastAPI")
    return {"message": "Error logged in FastAPI"}

# Flask app
app_flask = Flask(__name__)
flask_logger(app_flask)

@app_flask.route("/flask/hello")
def flask_hello():
    logger.info("Received request on Flask endpoint")
    return jsonify({"message": "Hello from Flask!"})

@app_flask.route("/flask/error")
def flask_error():
    logger.error("This is a test error in Flask")
    return jsonify({"message": "Error logged in Flask"})

# Run both servers in separate threads
def run_fastapi():
    uvicorn.run(app_fastapi, host="127.0.0.1", port=8000)

def run_flask():
    # Suppress werkzeug logger
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.CRITICAL)
    
    app_flask.run(host="127.0.0.1", port=5004)

if __name__ == "__main__":
    # Start FastAPI in a separate thread
    fastapi_thread = Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()

    # Run Flask in the main thread
    run_flask()