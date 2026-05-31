from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class Event:
    event_id: str
    sensor_id: str
    site_id: str
    event_time: str
    temp_c: float
    hum_pct: float
    partition_key: str

    def to_dict(self) -> dict:
        return asdict(self)


def generate_events() -> List[Event]:
    """
    Jeu de données simple avec :
    - distribution normale sur plusieurs capteurs
    - hotspot sur sensor-HOT-01
    - quelques doublons
    """
    base = [
        Event("e-00001", "sensor-01", "SITE-01", "2026-04-20T08:00:00", 22.3, 58.2, "sensor-01"),
        Event("e-00002", "sensor-02", "SITE-01", "2026-04-20T08:01:00", 23.1, 57.0, "sensor-02"),
        Event("e-00003", "sensor-03", "SITE-02", "2026-04-20T08:02:00", 21.8, 60.5, "sensor-03"),
        Event("e-00004", "sensor-04", "SITE-02", "2026-04-20T08:03:00", 24.0, 55.3, "sensor-04"),
    ]

    hotspot = []
    for i in range(5, 15):
        hotspot.append(
            Event(
                f"e-{i:05d}",
                "sensor-HOT-01",
                "SITE-03",
                f"2026-04-20T08:{i:02d}:00",
                26.0 + (i % 3),
                50.0 + (i % 4),
                "sensor-HOT-01",
            )
        )

    duplicates = [
        Event("e-00003", "sensor-03", "SITE-02", "2026-04-20T08:02:00", 21.8, 60.5, "sensor-03"),
        Event("e-00008", "sensor-HOT-01", "SITE-03", "2026-04-20T08:08:00", 28.0, 50.0, "sensor-HOT-01"),
    ]

    return base + hotspot + duplicates