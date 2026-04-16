from dataclasses import dataclass
import logging
import time

from events import Event
from windowing import tumbling_window_start, tumbling_window_end

logger = logging.getLogger(__name__)


@dataclass
class WindowState:
    count: int = 0
    sum_temp: float = 0.0
    sum_humidity: float = 0.0
    min_temp: float = float("inf")
    max_temp: float = float("-inf")

    def update(self, event: Event):
        self.count += 1
        self.sum_temp += event.temperature_c
        self.sum_humidity += event.humidity_pct
        self.min_temp = min(self.min_temp, event.temperature_c)
        self.max_temp = max(self.max_temp, event.temperature_c)

    def to_dict(self) -> dict:
        return {
            "count": self.count,
            "sum_temp": self.sum_temp,
            "sum_humidity": self.sum_humidity,
            "min_temp": self.min_temp,
            "max_temp": self.max_temp,
        }

    @property
    def avg_temp(self) -> float:
        return self.sum_temp / self.count if self.count else 0.0

    @property
    def avg_humidity(self) -> float:
        return self.sum_humidity / self.count if self.count else 0.0


class StreamProcessor:
    def __init__(
        self,
        window_size_seconds: int = 60,
        watermark_margin_seconds: int = 5,
        allowed_lateness_seconds: int = 120,
    ):
        self.window_size_seconds = window_size_seconds
        self.watermark_margin_seconds = watermark_margin_seconds
        self.allowed_lateness_seconds = allowed_lateness_seconds

        self.state: dict[tuple[str, int], WindowState] = {}
        self.max_event_time: float = 0.0
        self.events_processed: int = 0

        self.late_events: list[dict] = []
        self.dropped_events: list[dict] = []
        self.flushed_aggregates: list[dict] = []

    @property
    def watermark(self) -> float:
        return self.max_event_time - self.watermark_margin_seconds

    def classify_event(self, event: Event) -> str:
        event_ts = event.event_ts
        window_end = tumbling_window_end(event_ts, self.window_size_seconds)

        if self.watermark < window_end:
            return "on-time"

        lateness = self.watermark - window_end
        if lateness <= self.allowed_lateness_seconds:
            return "late-accepted"

        return "dropped"

    def process_event(self, event: Event) -> str:
        started = time.monotonic()

        self.max_event_time = max(self.max_event_time, event.event_ts)
        decision = self.classify_event(event)

        if decision == "dropped":
            self.dropped_events.append(event.to_dict())
            logger.warning(
                "DROP event_id=%s sensor_id=%s event_time=%s watermark=%.0f",
                event.event_id, event.sensor_id, event.event_time, self.watermark
            )
            return decision

        wk = tumbling_window_start(event.event_ts, self.window_size_seconds)
        key = (event.sensor_id, wk)

        if key not in self.state:
            self.state[key] = WindowState()

        self.state[key].update(event)
        self.events_processed += 1

        if decision == "late-accepted":
            self.late_events.append(event.to_dict())
            logger.info(
                "LATE_ACCEPT event_id=%s sensor_id=%s window_start=%s",
                event.event_id, event.sensor_id, wk
            )
        else:
            logger.info(
                "ON_TIME event_id=%s sensor_id=%s window_start=%s",
                event.event_id, event.sensor_id, wk
            )

        duration_ms = (time.monotonic() - started) * 1000
        logger.debug("Process latency %.2f ms", duration_ms)
        return decision

    def flush_closed_windows(self) -> list[dict]:
        flushed = []
        to_delete = []

        for (sensor_id, wk), ws in self.state.items():
            window_end = wk + self.window_size_seconds
            if self.watermark >= window_end:
                row = {
                    "sensor_id": sensor_id,
                    "window_start": wk,
                    "window_end": window_end,
                    "count": ws.count,
                    "avg_temp": round(ws.avg_temp, 3),
                    "avg_humidity": round(ws.avg_humidity, 3),
                    "min_temp": round(ws.min_temp, 3),
                    "max_temp": round(ws.max_temp, 3),
                }
                flushed.append(row)
                to_delete.append((sensor_id, wk))

        for key in to_delete:
            del self.state[key]

        self.flushed_aggregates.extend(flushed)
        if flushed:
            logger.info("Flush de %d fenêtre(s) closes", len(flushed))

        return flushed