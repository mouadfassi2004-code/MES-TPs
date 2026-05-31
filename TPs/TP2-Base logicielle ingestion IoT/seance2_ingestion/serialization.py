import json


def to_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def from_json(text: str) -> dict:
    return json.loads(text)