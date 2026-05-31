import json
import uuid
import time

MAX_PAYLOAD = 1_000_000


def build_request(method: str, params: dict = None) -> dict:
    return {
        "rpc_version": "1.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": params or {},
        "sent_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def build_response(rpc_id: str, result) -> dict:
    return {
        "rpc_version": "1.0",
        "id": rpc_id,
        "result": result,
        "error": None,
    }


def build_error_response(rpc_id: str, code: int, message: str, details: str = "") -> dict:
    return {
        "rpc_version": "1.0",
        "id": rpc_id or "",
        "result": None,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }


def validate_rpc_request(raw_bytes: bytes) -> tuple[dict | None, dict | None]:
    if len(raw_bytes) > MAX_PAYLOAD:
        return None, build_error_response("", 1002, "Payload too large")

    try:
        data = json.loads(raw_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return None, build_error_response("", -32700, "Parse error", str(e))

    if not isinstance(data, dict):
        return None, build_error_response("", -32600, "Must be a JSON object")

    rpc_id = data.get("id", "")

    for f in ("id", "method", "params", "rpc_version"):
        if f not in data:
            return None, build_error_response(rpc_id, -32600, f"Missing field: {f}")

    if not isinstance(data["method"], str) or not data["method"].strip():
        return None, build_error_response(rpc_id, -32600, "Field 'method' invalide")

    if not isinstance(data["params"], dict):
        return None, build_error_response(rpc_id, -32600, "Field 'params' doit être un objet JSON")

    return data, None