from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class SensorMessage:
    request_id: str
    sensor_id: str
    site_id: str
    timestamp: str
    temperature: float
    humidity: float
    irrigation: str
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    ozone: Optional[float] = None
    no2: Optional[float] = None
    battery: Optional[float] = None

    def to_dict(self):
        return asdict(self)