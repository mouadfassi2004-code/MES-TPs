from dataclasses import dataclass, field, asdict
from typing import Any
import time
import uuid
import math


@dataclass
class EventMessage:
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    msg_type: str = "sensor_reading"
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    attempts: int = 0
    max_attempts: int = 3

    def should_retry(self) -> bool:
        return self.attempts < self.max_attempts

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


VALID_METRICS = {"temperature", "humidity", "luminosity"}


def is_valid_reading(payload: dict[str, Any]) -> tuple[bool, str]:
    required_fields = {"sensor_id", "metric", "value", "timestamp"}
    missing = required_fields - payload.keys()
    if missing:
        return False, f"Missing fields: {sorted(missing)}"

    sensor_id = payload.get("sensor_id")
    metric = payload.get("metric")
    value = payload.get("value")
    timestamp = payload.get("timestamp")

    if not isinstance(sensor_id, str) or not sensor_id.strip():
        return False, "Invalid sensor_id"

    if metric not in VALID_METRICS:
        return False, f"Invalid metric: {metric}"

    if not isinstance(timestamp, (int, float)):
        return False, "Invalid timestamp"

    if not isinstance(value, (int, float)):
        return False, "Value must be numeric"

    if math.isnan(value) or math.isinf(value):
        return False, "Value is NaN/Inf"

    if metric == "temperature":
        if not (-50.0 <= value <= 80.0):
            return False, "Temperature out of range"
    elif metric == "humidity":
        if not (0.0 <= value <= 100.0):
            return False, "Humidity out of range"
    elif metric == "luminosity":
        if not (0.0 <= value <= 2000.0):
            return False, "Luminosity out of range"

    return True, "OK"