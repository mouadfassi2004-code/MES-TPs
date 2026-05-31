import json
import os
from collections import Counter
from src.config import METRICS_FILE


class RunMetrics:
    def __init__(self):
        self.received = 0
        self.accepted = 0
        self.rejected = 0
        self.processing_times = []
        self.reject_reasons = Counter()

    def add_received(self):
        self.received += 1

    def add_accepted(self, processing_time):
        self.accepted += 1
        self.processing_times.append(processing_time)

    def add_rejected(self, errors, processing_time):
        self.rejected += 1
        self.processing_times.append(processing_time)
        for err in errors:
            self.reject_reasons[err] += 1

    def save(self):
        avg_time = (
            sum(self.processing_times) / len(self.processing_times)
            if self.processing_times else 0
        )

        data = {
            "messages_received": self.received,
            "messages_accepted": self.accepted,
            "messages_rejected": self.rejected,
            "average_processing_time_ms": round(avg_time * 1000, 2),
            "top_reject_reasons": dict(self.reject_reasons)
        }

        os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
        with open(METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)