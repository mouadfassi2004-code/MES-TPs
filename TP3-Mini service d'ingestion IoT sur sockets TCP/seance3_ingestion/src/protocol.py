import json
import uuid
from datetime import datetime


PROTOCOL_VERSION = "v1"


def build_message(message_type: str, payload: dict, request_id: str | None = None) -> dict:
    return {
        "version": PROTOCOL_VERSION,
        "type": message_type,
        "request_id": request_id or str(uuid.uuid4()),
        "sent_at": datetime.now().isoformat(),
        "payload": payload,
    }


def encode_message(message: dict) -> bytes:
    return (json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8")


def decode_message(line: bytes) -> dict:
    return json.loads(line.decode("utf-8").strip())


def recv_ndjson_message(conn) -> dict | None:
    buffer = b""

    while True:
        chunk = conn.recv(4096)
        if not chunk:
            if not buffer:
                return None
            break
        buffer += chunk
        if b"\n" in buffer:
            line, _rest = buffer.split(b"\n", 1)
            return decode_message(line)

    return decode_message(buffer)