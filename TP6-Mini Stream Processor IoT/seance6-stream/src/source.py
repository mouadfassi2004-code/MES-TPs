import queue
import time
from events import Event


def sample_events() -> list[Event]:
    return [
        Event("evt-001", "sensor_A", "site_1", "2025-06-01T10:00:05", 22.5, 65.0, 0.42),
        Event("evt-002", "sensor_B", "site_1", "2025-06-01T10:00:12", 19.3, 70.2, 0.51),
        Event("evt-003", "sensor_A", "site_1", "2025-06-01T10:00:35", 23.1, 64.8, 0.40),
        Event("evt-004", "sensor_A", "site_1", "2025-06-01T10:01:10", 24.0, 63.5, 0.39),
        Event("evt-005", "sensor_B", "site_1", "2025-06-01T10:01:22", 20.1, 69.1, 0.50),
        Event("evt-006", "sensor_A", "site_1", "2025-06-01T10:00:50", 22.9, 65.2, 0.41),
        Event("evt-007", "sensor_B", "site_1", "2025-06-01T10:03:20", 21.5, 68.0, 0.49),
        Event("evt-008", "sensor_A", "site_1", "2025-06-01T10:00:20", 22.0, 66.0, 0.43),
    ]


def produce_events(out_queue: queue.Queue, delay_seconds: float = 0.2):
    for event in sample_events():
        out_queue.put(event)
        time.sleep(delay_seconds)

    out_queue.put(None)