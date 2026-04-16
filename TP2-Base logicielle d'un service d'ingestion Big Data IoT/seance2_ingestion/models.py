from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
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
    timestamp: str
    site_id: str
    sensor_id: str
    temperature_c: float
    humidity_pct: float
    soil_moisture: Optional[float] = None
    pump_status: str = "off"
    irrigation_l_min: float = 0.0

    def __post_init__(self):
        if not isinstance(self.sensor_id, str) or self.sensor_id.strip() == "":
            raise ValueError("sensor_id ne doit pas être vide")

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "site_id": self.site_id,
            "sensor_id": self.sensor_id,
            "temperature_c": self.temperature_c,
            "humidity_pct": self.humidity_pct,
            "soil_moisture": self.soil_moisture,
            "pump_status": self.pump_status,
            "irrigation_l_min": self.irrigation_l_min,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SensorReading":
        return cls(
            timestamp=data.get("timestamp", ""),
            site_id=data.get("site_id", ""),
            sensor_id=data.get("sensor_id", ""),
            temperature_c=float(data.get("temperature_c", 0.0)),
            humidity_pct=float(data.get("humidity_pct", 0.0)),
            soil_moisture=data.get("soil_moisture"),
            pump_status=data.get("pump_status", "off"),
            irrigation_l_min=float(data.get("irrigation_l_min", 0.0)),
        )


@dataclass
class IngestRequest:
    request_id: str
    api_key: str
    readings: List[SensorReading] = field(default_factory=list)
    sent_at: str = ""

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "api_key": self.api_key,
            "readings": [r.to_dict() for r in self.readings],
            "sent_at": self.sent_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IngestRequest":
        readings_data = data.get("readings", [])
        readings = [SensorReading.from_dict(r) for r in readings_data]

        return cls(
            request_id=data.get("request_id", ""),
            api_key=data.get("api_key", ""),
            readings=readings,
            sent_at=data.get("sent_at", ""),
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