import time
import uuid


def make_response(request_id: str, status: str, errors=None, message=None):
    return {
        "request_id": request_id,
        "response_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "errors": errors or [],
        "message": message or ""
    }


def make_health_response():
    return {
        "request_id": str(uuid.uuid4()),
        "response_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "OK",
        "errors": [],
        "message": "Server is healthy"
    }