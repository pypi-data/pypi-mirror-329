# SIFT dev-logger

A Python logging SDK that provides structured logging for Flask and FastAPI applications.

---

## Installation

### Using `pip`

```bash
pip install sift-dev-logger
```

**With optional Flask support:**

```bash
pip install "sift-dev-logger[flask]"
```

**With optional FastAPI support:**

```bash
pip install "sift-dev-logger[fastapi]"
```

**With all library support:**

```bash
pip install "sift-dev-logger[all]"
```

---

## Usage

### Flask Application

```python
from flask import Flask
from sift_dev_logger.config import SiftDevConfig, configure
from sift_dev_logger.flask import instrument_logging_middleware

app = Flask(__name__)

# Configure the SDK
config = SiftDevConfig(
   service_name="my-flask-app",
   service_instance="my-instance",
   sift_dev_logging_project_key="my-project-key"
)
configure(config)

# Add logging middleware
instrument_logging_middleware(app)
```

### FastAPI Application

```python
from fastapi import FastAPI
from sift_dev_logger.config import SiftDevConfig, configure
from sift_dev_logger.fastapi import instrument_logging_middleware

app = FastAPI()

# Configure the SDK
config = SiftDevConfig(
   service_name="my-fastapi-app",
   service_instance="my-instance",
   sift_dev_logging_project_key="my-project-key"
)
configure(config)

# Add logging middleware
instrument_logging_middleware(app)
```

---

## How to build and publish

1. **Install build tools**:

    ```bash
    pip install build
    ```

2. **Build the package**:

    ```bash
    python -m build
    ```

3. **Test the package locally**:

    ```bash
    pip install sift_dev_logger-0.1.0.tar.gz
    ```

4. **Upload to PyPI** (you’ll need to create an account first):

    ```bash
    python -m twine upload dist/*
    ```

---

## Key Features

1. **Optional Dependencies**: Users can install just what they need (core, Flask, or FastAPI support).  
2. **Modern Build System**: Uses `hatchling` for a clean, modern build.  
3. **Clear Documentation**: README shows installation and basic usage.  
4. **Version Management**: Easy to update version in one place.  
5. **Development Tooling**: Development dependencies separated from runtime requirements.

---