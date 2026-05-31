import csv
import os
import threading
from datetime import datetime

from models import SensorReading


class DataStore:
    def __init__(self):
        self._readings = []
        self._batch_ids = set()
        self._lock = threading.Lock()

    def ingest_batch(self, batch_id: str, readings: list[dict]) -> dict:
        if not batch_id:
            raise ValueError("batch_id manquant")

        with self._lock:
            if batch_id in self._batch_ids:
                return {
                    "accepted": 0,
                    "rejected": 0,
                    "duplicate": True,
                    "message": "batch déjà traité"
                }

            accepted = 0
            rejected = 0

            for item in readings:
                try:
                    reading = SensorReading.from_dict(item)

                    if not reading.sensor_id.strip():
                        raise ValueError("sensor_id vide")
                    if not reading.ts.strip():
                        raise ValueError("ts vide")

                    datetime.fromisoformat(reading.ts)

                    self._readings.append(reading.to_dict())
                    accepted += 1
                except Exception:
                    rejected += 1

            self._batch_ids.add(batch_id)
            self._save_csv()

            return {
                "accepted": accepted,
                "rejected": rejected,
                "duplicate": False,
            }

    def daily_summary(self, date_str: str) -> dict:
        with self._lock:
            selected = []
            for r in self._readings:
                if str(r["ts"]).startswith(date_str):
                    selected.append(r)

            if not selected:
                return {
                    "date": date_str,
                    "count": 0,
                    "avg": None,
                    "min": None,
                    "max": None,
                }

            values = [float(x["value"]) for x in selected]
            return {
                "date": date_str,
                "count": len(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
            }

    def ping(self) -> dict:
        return {"status": "ok"}

    def _save_csv(self):
        os.makedirs("outputs", exist_ok=True)
        path = "outputs/ingested_data.csv"
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["sensor_id", "ts", "value"])
            writer.writeheader()
            writer.writerows(self._readings)