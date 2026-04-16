import csv
import os
import threading
import time
from collections import defaultdict
from statistics import mean

from models import SensorReading


class DataStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._readings = []
        self._processed_batches = set()

    def save_csv(self):
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/ingested_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["sensor_id", "ts", "value"])
            writer.writeheader()
            writer.writerows(self._readings)

    def health_ping(self, params: dict):
        return {
            "status": "ok",
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
        }

    def ingest_batch(self, params: dict):
        readings = params.get("readings", [])
        batch_id = params.get("batch_id", "")

        if not isinstance(readings, list):
            raise ValueError("readings doit être une liste")

        with self._lock:
            if batch_id:
                if batch_id in self._processed_batches:
                    return {
                        "accepted": 0,
                        "rejected": 0,
                        "errors": [],
                        "duplicate": True,
                        "message": "batch déjà traité"
                    }

            accepted = 0
            rejected = 0
            errors = []

            for i, item in enumerate(readings):
                try:
                    sr = SensorReading(
                        sensor_id=item.get("sensor_id", ""),
                        ts=item.get("ts", ""),
                        value=item.get("value", 0.0),
                    )
                    v = sr.validate()
                    if v:
                        rejected += 1
                        errors.append({"index": i, "errors": v})
                    else:
                        self._readings.append({
                            "sensor_id": sr.sensor_id,
                            "ts": sr.ts,
                            "value": sr.value
                        })
                        accepted += 1
                except Exception as e:
                    rejected += 1
                    errors.append({"index": i, "errors": [str(e)]})

            if batch_id:
                self._processed_batches.add(batch_id)

            self.save_csv()

            return {
                "accepted": accepted,
                "rejected": rejected,
                "errors": errors,
                "duplicate": False,
            }

    def daily_summary(self, params: dict):
        date_str = params.get("date", "")
        if not date_str:
            raise ValueError("date manquante")

        with self._lock:
            selected = [r for r in self._readings if r["ts"].startswith(date_str)]

        if not selected:
            return {
                "date": date_str,
                "count": 0,
                "avg": None,
                "min": None,
                "max": None,
            }

        values = [float(r["value"]) for r in selected]
        return {
            "date": date_str,
            "count": len(values),
            "avg": mean(values),
            "min": min(values),
            "max": max(values),
        }

    def top_sensors(self, params: dict):
        n = params.get("n", 5)
        try:
            n = int(n)
        except Exception:
            raise ValueError("n doit être un entier")

        with self._lock:
            grouped = defaultdict(list)
            for r in self._readings:
                grouped[r["sensor_id"]].append(float(r["value"]))

        result = []
        for sensor_id, values in grouped.items():
            result.append({
                "sensor_id": sensor_id,
                "avg": mean(values)
            })

        result.sort(key=lambda x: x["avg"], reverse=True)
        return {"sensors": result[:n]}