from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ValidationError:
    field: str
    code: str
    message: str

    def to_dict(self) -> dict:
        return {
            "field": self.field,
            "code": self.code,
            "message": self.message,
        }


@dataclass
class SensorReading:
    sensor_id: str
    type: str
    value: float
    unit: str
    timestamp: str
    pump_status: Optional[str] = None
    irrigation_mm: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "sensor_id": self.sensor_id,
            "type": self.type,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp,
            "pump_status": self.pump_status,
            "irrigation_mm": self.irrigation_mm,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SensorReading":
        return cls(
            sensor_id=str(data.get("sensor_id", "")),
            type=str(data.get("type", "")),
            value=float(data.get("value", 0.0)),
            unit=str(data.get("unit", "")),
            timestamp=str(data.get("timestamp", "")),
            pump_status=data.get("pump_status"),
            irrigation_mm=data.get("irrigation_mm"),
        )


@dataclass
class IngestRequest:
    source: str
    readings: List[SensorReading] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "readings": [r.to_dict() for r in self.readings],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IngestRequest":
        readings = [SensorReading.from_dict(x) for x in data.get("readings", [])]
        return cls(
            source=str(data.get("source", "unknown_source")),
            readings=readings,
        )


@dataclass
class IngestResponse:
    status: str
    accepted_count: int
    rejected_count: int
    errors: List[ValidationError] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "accepted_count": self.accepted_count,
            "rejected_count": self.rejected_count,
            "errors": [e.to_dict() for e in self.errors],
        }