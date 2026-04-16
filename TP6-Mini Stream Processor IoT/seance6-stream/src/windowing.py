def tumbling_window_start(event_ts: float, window_size_seconds: int) -> int:
    return int(event_ts // window_size_seconds) * window_size_seconds


def tumbling_window_end(event_ts: float, window_size_seconds: int) -> int:
    start = tumbling_window_start(event_ts, window_size_seconds)
    return start + window_size_seconds