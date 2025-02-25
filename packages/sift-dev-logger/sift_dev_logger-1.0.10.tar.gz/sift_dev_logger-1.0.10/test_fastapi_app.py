from fastapi import FastAPI
import uvicorn
from sift_dev_logger import SiftDevConfig, configure, fastapi_logger, getLogger
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

logger = getLogger("test")

config = SiftDevConfig(
    sift_dev_ingest_key="test-key",
    service_name="test-fastapi",
)
configure(config)
fastapi_logger(app)

@app.get("/")
async def root():
    logger.info("Received request from fastapi")
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 