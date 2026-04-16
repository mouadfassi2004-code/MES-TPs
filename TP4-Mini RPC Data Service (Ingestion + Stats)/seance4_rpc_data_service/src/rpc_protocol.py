import json
import uuid
from datetime import datetime

from models import RpcError, RpcRequest, RpcResponse


RPC_VERSION = "1.0"


def build_request(method: str, params: dict) -> RpcRequest:
    return RpcRequest(
        rpc_version=RPC_VERSION,
        id=str(uuid.uuid4()),
        method=method,
        params=params,
        sent_at=datetime.now().isoformat(),
    )


def success_response(rpc_id: str, result):
    return RpcResponse(
        rpc_version=RPC_VERSION,
        id=rpc_id,
        result=result,
        error=None,
    )


def error_response(rpc_id: str | None, code: int, message: str, details=""):
    return RpcResponse(
        rpc_version=RPC_VERSION,
        id=rpc_id or "",
        result=None,
        error=RpcError(code=code, message=message, details=details),
    )


def encode_json(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def decode_json(raw: bytes) -> dict:
    return json.loads(raw.decode("utf-8"))


def validate_rpc_request(data: dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "Request must be a JSON object"

    required = ["rpc_version", "id", "method", "params"]
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"

    if not isinstance(data["id"], str) or not data["id"].strip():
        return False, "Field 'id' must be a non-empty string"

    if not isinstance(data["method"], str) or not data["method"].strip():
        return False, "Field 'method' must be a non-empty string"

    if not isinstance(data["params"], dict):
        return False, "Field 'params' must be an object"

    return True, ""