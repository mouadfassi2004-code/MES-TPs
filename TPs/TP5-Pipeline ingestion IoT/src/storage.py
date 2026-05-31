import csv
import json
import os
import threading
from typing import Any

from messages import EventMessage


class Storage:
    def __init__(self, csv_path: str, dead_letter_path: str) -> None:
        self.csv_path = csv_path
        self.dead_letter_path = dead_letter_path
        self._csv_lock = threading.Lock()
        self._dlq_lock = threading.Lock()

        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        os.makedirs(os.path.dirname(dead_letter_path), exist_ok=True)

        self._ensure_csv_header()
        self._ensure_dead_letter_file()

    def _ensure_csv_header(self) -> None:
        if not os.path.exists(self.csv_path) or os.path.getsize(self.csv_path) == 0:
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "msg_id",
                    "sensor_id",
                    "metric",
                    "value",
                    "timestamp",
                    "created_at",
                    "attempts",
                ])

    def _ensure_dead_letter_file(self) -> None:
        if not os.path.exists(self.dead_letter_path) or os.path.getsize(self.dead_letter_path) == 0:
            with open(self.dead_letter_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def save_valid_message(self, msg: EventMessage) -> None:
        payload = msg.payload
        with self._csv_lock:
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    msg.msg_id,
                    payload.get("sensor_id"),
                    payload.get("metric"),
                    payload.get("value"),
                    payload.get("timestamp"),
                    msg.created_at,
                    msg.attempts,
                ])

    def save_dead_letter(self, msg: EventMessage, reason: str) -> None:
        entry: dict[str, Any] = {
            "reason": reason,
            **msg.to_dict(),
        }

        with self._dlq_lock:
            with open(self.dead_letter_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            data.append(entry)

            with open(self.dead_letter_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)