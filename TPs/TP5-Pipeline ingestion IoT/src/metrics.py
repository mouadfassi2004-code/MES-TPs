import threading
import time


class Metrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.start_time = time.time()

        self.produced = 0
        self.enqueued = 0
        self.dropped = 0
        self.processed = 0
        self.failed = 0
        self.retried = 0
        self.dead_lettered = 0

        self.total_latency = 0.0
        self.last_snapshot_time = self.start_time
        self.last_processed_count = 0

    def inc_produced(self, n: int = 1) -> None:
        with self._lock:
            self.produced += n

    def inc_enqueued(self, n: int = 1) -> None:
        with self._lock:
            self.enqueued += n

    def inc_dropped(self, n: int = 1) -> None:
        with self._lock:
            self.dropped += n

    def inc_processed(self, latency: float) -> None:
        with self._lock:
            self.processed += 1
            self.total_latency += latency

    def inc_failed(self, n: int = 1) -> None:
        with self._lock:
            self.failed += n

    def inc_retried(self, n: int = 1) -> None:
        with self._lock:
            self.retried += n

    def inc_dead_lettered(self, n: int = 1) -> None:
        with self._lock:
            self.dead_lettered += n

    def snapshot(self, backlog: int, dlq_size: int) -> dict:
        with self._lock:
            now = time.time()
            elapsed = max(now - self.start_time, 1e-9)
            delta_t = max(now - self.last_snapshot_time, 1e-9)
            delta_processed = self.processed - self.last_processed_count

            processing_rate = delta_processed / delta_t
            avg_latency = self.total_latency / self.processed if self.processed else 0.0
            error_rate = self.failed / self.processed if self.processed else 0.0

            data = {
                "uptime_sec": round(elapsed, 2),
                "produced": self.produced,
                "enqueued": self.enqueued,
                "dropped": self.dropped,
                "processed": self.processed,
                "failed": self.failed,
                "retried": self.retried,
                "dead_lettered": self.dead_lettered,
                "avg_latency_sec": round(avg_latency, 4),
                "processing_rate_msg_s": round(processing_rate, 2),
                "error_rate": round(error_rate, 4),
                "backlog": backlog,
                "dlq_size": dlq_size,
            }

            self.last_snapshot_time = now
            self.last_processed_count = self.processed
            return data