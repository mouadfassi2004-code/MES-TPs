import json
import pathlib
import time


class Metrics:
    def __init__(self):
        self.start_time = time.monotonic()
        self.processed = 0
        self.on_time = 0
        self.late_accepted = 0
        self.dropped = 0
        self.flushed_windows = 0
        self.processing_latencies_ms: list[float] = []

    def record_latency(self, ms: float):
        self.processing_latencies_ms.append(ms)

    def to_dict(self) -> dict:
        elapsed = time.monotonic() - self.start_time
        avg_latency = (
            sum(self.processing_latencies_ms) / len(self.processing_latencies_ms)
            if self.processing_latencies_ms else 0.0
        )
        throughput = self.processed / elapsed if elapsed > 0 else 0.0

        return {
            "processed": self.processed,
            "on_time": self.on_time,
            "late_accepted": self.late_accepted,
            "dropped": self.dropped,
            "flushed_windows": self.flushed_windows,
            "avg_latency_ms": round(avg_latency, 2),
            "throughput_eps": round(throughput, 2),
            "elapsed_seconds": round(elapsed, 2),
        }


def save_run_report(metrics: Metrics, path: str):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(metrics.to_dict(), indent=2), encoding="utf-8")