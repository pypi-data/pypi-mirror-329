def test_core_imports():
    """Test that all core dependencies can be imported"""
    import logging
    from opentelemetry import trace
    from opentelemetry.sdk import trace as trace_sdk
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.instrumentation.logging import LoggingInstrumentor

def test_flask_imports():
    """Test Flask integration dependencies"""
    from flask import Flask, Request, Response
    from flask.testing import FlaskClient
    import json
    import time
    import uuid

def test_fastapi_imports():
    """Test FastAPI integration dependencies"""
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse, Response
    from fastapi.testclient import TestClient
    from starlette.middleware.base import BaseHTTPMiddleware
    import json
    import time
    import uuid

def test_common_imports():
    """Test common utilities and configuration imports"""
    import os
    import logging
    from logging import LoggerAdapter
    import uuid
    from typing import Optional, Dict, Any 