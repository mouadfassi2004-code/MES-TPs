from dataclasses import dataclass, field, asdict
from typing import Any
import uuid
import time
import json


@dataclass
class SensorReading:
    sensor_id: str
    ts: str
    value: float

    def validate(self) -> list[str]:
        errors = []
        if not self.sensor_id:
            errors.append("sensor_id est vide")
        if not self.ts:
            errors.append("ts est vide")
        if not isinstance(self.value, (int, float)) or isinstance(self.value, bool):
            errors.append(f"value non numérique: {self.value}")
        elif abs(self.value) > 1000:
            errors.append(f"value aberrante: {self.value}")
        return errors


@dataclass
class RpcRequest:
    method: str
    params: dict = field(default_factory=dict)
    rpc_version: str = "1.0"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sent_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


@dataclass
class RpcResponse:
    id: str
    result: Any = None
    error: dict | None = None
    rpc_version: str = "1.0"

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)