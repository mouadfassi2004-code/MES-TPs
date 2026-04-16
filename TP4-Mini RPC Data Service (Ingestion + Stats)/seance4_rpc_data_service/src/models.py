from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class SensorReading:
    sensor_id: str
    ts: str
    value: float

    def to_dict(self) -> dict:
        return {
            "sensor_id": self.sensor_id,
            "ts": self.ts,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SensorReading":
        return cls(
            sensor_id=str(data.get("sensor_id", "")),
            ts=str(data.get("ts", "")),
            value=float(data.get("value", 0.0)),
        )


@dataclass
class RpcError:
    code: int
    message: str
    details: Any = ""

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


@dataclass
class RpcRequest:
    rpc_version: str
    id: str
    method: str
    params: dict
    sent_at: str

    def to_dict(self) -> dict:
        return {
            "rpc_version": self.rpc_version,
            "id": self.id,
            "method": self.method,
            "params": self.params,
            "sent_at": self.sent_at,
        }


@dataclass
class RpcResponse:
    rpc_version: str
    id: str
    result: Optional[Any] = None
    error: Optional[RpcError] = None

    def to_dict(self) -> dict:
        return {
            "rpc_version": self.rpc_version,
            "id": self.id,
            "result": self.result,
            "error": None if self.error is None else self.error.to_dict(),
        }