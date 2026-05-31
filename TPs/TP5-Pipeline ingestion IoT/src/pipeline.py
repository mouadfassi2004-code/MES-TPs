import logging
import queue
import threading
import time

from metrics import Metrics
from producers import producer
from storage import Storage
from workers import worker


def monitor(
    main_queue: queue.Queue,
    dead_letter_queue: queue.Queue,
    stop_event: threading.Event,
    metrics: Metrics,
    interval: float = 2.0,
) -> None:
    logging.info("[monitor] started")

    while not stop_event.is_set():
        snapshot = metrics.snapshot(
            backlog=main_queue.qsize(),
            dlq_size=dead_letter_queue.qsize(),
        )
        logging.info(
            "[monitor] uptime=%ss produced=%s enqueued=%s dropped=%s processed=%s failed=%s retried=%s dlq=%s backlog=%s rate=%s msg/s avg_latency=%ss",
            snapshot["uptime_sec"],
            snapshot["produced"],
            snapshot["enqueued"],
            snapshot["dropped"],
            snapshot["processed"],
            snapshot["failed"],
            snapshot["retried"],
            snapshot["dead_lettered"],
            snapshot["backlog"],
            snapshot["processing_rate_msg_s"],
            snapshot["avg_latency_sec"],
        )
        time.sleep(interval)

    logging.info("[monitor] stopped")


def run_pipeline(
    runtime_sec: int = 15,
    num_producers: int = 3,
    num_workers: int = 2,
    queue_maxsize: int = 50,
    csv_path: str = "outputs/valid_readings.csv",
    dead_letter_path: str = "outputs/dead_letters.json",
) -> None:
    main_queue: queue.Queue = queue.Queue(maxsize=queue_maxsize)
    dead_letter_queue: queue.Queue = queue.Queue()

    stop_event = threading.Event()
    metrics = Metrics()
    storage = Storage(csv_path=csv_path, dead_letter_path=dead_letter_path)

    producer_threads: list[threading.Thread] = []
    worker_threads: list[threading.Thread] = []

    for i in range(num_producers):
        t = threading.Thread(
            target=producer,
            name=f"producer-{i+1}",
            args=(f"producer-{i+1}", main_queue, stop_event, metrics),
            daemon=True,
        )
        producer_threads.append(t)

    for i in range(num_workers):
        t = threading.Thread(
            target=worker,
            name=f"worker-{i+1}",
            args=(f"worker-{i+1}", main_queue, dead_letter_queue, stop_event, metrics, storage),
            daemon=True,
        )
        worker_threads.append(t)

    monitor_thread = threading.Thread(
        target=monitor,
        name="monitor",
        args=(main_queue, dead_letter_queue, stop_event, metrics),
        daemon=True,
    )

    logging.info(
        "Pipeline starting with producers=%d workers=%d queue_maxsize=%d runtime=%ds",
        num_producers,
        num_workers,
        queue_maxsize,
        runtime_sec,
    )

    for t in producer_threads:
        t.start()

    for t in worker_threads:
        t.start()

    monitor_thread.start()

    time.sleep(runtime_sec)
    stop_event.set()

    for t in producer_threads:
        t.join(timeout=2)

    main_queue.join()

    for t in worker_threads:
        t.join(timeout=2)

    monitor_thread.join(timeout=2)

    snapshot = metrics.snapshot(
        backlog=main_queue.qsize(),
        dlq_size=dead_letter_queue.qsize(),
    )

    logging.info("Pipeline finished.")
    logging.info("Final snapshot: %s", snapshot)