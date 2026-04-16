import json


def serialize_message(message: dict) -> bytes:
    """
    JSON + framing par saut de ligne.
    """
    return (json.dumps(message) + "\n").encode("utf-8")


def deserialize_message(raw: str) -> dict:
    return json.loads(raw)