import logging
import queue
import random
import threading
import time

from messages import EventMessage
from metrics import Metrics


SENSORS = ["sensor-A1", "sensor-B3", "sensor-C7", "sensor-D2", "sensor-E9"]
METRICS = ["temperature", "humidity", "luminosity"]


def generate_value(metric: str) -> float:
    roll = random.random()

    if roll < 0.05:
        return float("nan")
    if roll < 0.10:
        return -999.0

    if metric == "temperature":
        return round(random.uniform(10.0, 40.0), 2)
    if metric == "humidity":
        return round(random.uniform(20.0, 95.0), 2)
    return round(random.uniform(100.0, 1200.0), 2)


def producer(
    name: str,
    main_queue: queue.Queue,
    stop_event: threading.Event,
    metrics: Metrics,
    burst_size: int = 30,
    pause_between_bursts: float = 0.4,
    put_timeout: float = 0.2,
    max_attempts: int = 3,
) -> None:
    logging.info("[%s] started", name)

    while not stop_event.is_set():
        for _ in range(burst_size):
            if stop_event.is_set():
                break

            metric = random.choice(METRICS)
            msg = EventMessage(
                msg_type="sensor_reading",
                payload={
                    "sensor_id": random.choice(SENSORS),
                    "metric": metric,
                    "value": generate_value(metric),
                    "timestamp": time.time(),
                },
                max_attempts=max_attempts,
            )

            metrics.inc_produced()

            try:
                main_queue.put(msg, timeout=put_timeout)
                metrics.inc_enqueued()
            except queue.Full:
                metrics.inc_dropped()
                logging.warning("[%s] queue full -> message dropped: %s", name, msg.msg_id[:8])

            time.sleep(0.01)

        time.sleep(pause_between_bursts)

    logging.info("[%s] stopped", name)