from utils.storage import utc_now_iso

class StreamMetrics:
    def __init__(self):
        self.events_processed = 0
        self.invalid_events = 0
        self.late_events = 0

    def inc_processed(self) -> None:
        self.events_processed += 1

    def inc_invalid(self) -> None:
        self.invalid_events += 1

    def inc_late(self) -> None:
        self.late_events += 1

    def snapshot(self) -> dict:
        return {
            "timestamp": utc_now_iso(),
            "events_processed": self.events_processed,
            "invalid_events": self.invalid_events,
            "late_events": self.late_events,
        }