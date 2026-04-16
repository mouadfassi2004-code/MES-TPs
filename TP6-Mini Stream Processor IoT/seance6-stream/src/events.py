from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Event:
    event_id: str
    sensor_id: str
    site_id: str
    event_time: str
    temperature_c: float
    humidity_pct: float
    soil_moisture: float

    @property
    def event_ts(self) -> float:
        return datetime.fromisoformat(self.event_time).timestamp()

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "sensor_id": self.sensor_id,
            "site_id": self.site_id,
            "event_time": self.event_time,
            "temperature_c": self.temperature_c,
            "humidity_pct": self.humidity_pct,
            "soil_moisture": self.soil_moisture,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Event":
        return cls(
            event_id=str(data["event_id"]),
            sensor_id=str(data["sensor_id"]),
            site_id=str(data["site_id"]),
            event_time=str(data["event_time"]),
            temperature_c=float(data["temperature_c"]),
            humidity_pct=float(data["humidity_pct"]),
            soil_moisture=float(data["soil_moisture"]),
        )