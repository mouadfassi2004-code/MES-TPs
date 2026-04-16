import logging
import os
import queue
import threading
import time

from source import produce_events
from processor import StreamProcessor
from checkpoint import save_checkpoint, load_checkpoint
from sink import write_csv_rows
from metrics import Metrics, save_run_report


WINDOW_SIZE_SECONDS = 60
WATERMARK_MARGIN_SECONDS = 5
ALLOWED_LATENESS_SECONDS = 120
CHECKPOINT_INTERVAL_SECONDS = 2

AGGREGATES_PATH = "outputs/aggregates.csv"
LATE_EVENTS_PATH = "outputs/late_events.csv"
DROPPED_EVENTS_PATH = "outputs/dropped_events.csv"
RUN_REPORT_PATH = "outputs/run_report.json"
CHECKPOINT_PATH = "checkpoints/state.json"
LOG_PATH = "logs/pipeline.log"


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def main():
    setup_logging()
    logger = logging.getLogger("main")

    q: queue.Queue = queue.Queue()
    metrics = Metrics()

    processor = StreamProcessor(
        window_size_seconds=WINDOW_SIZE_SECONDS,
        watermark_margin_seconds=WATERMARK_MARGIN_SECONDS,
        allowed_lateness_seconds=ALLOWED_LATENESS_SECONDS,
    )

    load_checkpoint(processor, CHECKPOINT_PATH)

    producer_thread = threading.Thread(target=produce_events, args=(q,), daemon=True)
    producer_thread.start()

    last_checkpoint = time.monotonic()

    while True:
        item = q.get()

        if item is None:
            logger.info("Fin du flux reçue.")
            break

        started = time.monotonic()
        decision = processor.process_event(item)
        latency_ms = (time.monotonic() - started) * 1000

        metrics.record_latency(latency_ms)
        metrics.processed += 1

        if decision == "on-time":
            metrics.on_time += 1
        elif decision == "late-accepted":
            metrics.late_accepted += 1
        elif decision == "dropped":
            metrics.dropped += 1

        flushed = processor.flush_closed_windows()
        metrics.flushed_windows += len(flushed)

        now = time.monotonic()
        if now - last_checkpoint >= CHECKPOINT_INTERVAL_SECONDS:
            save_checkpoint(processor, CHECKPOINT_PATH)
            last_checkpoint = now

    final_flushed = processor.flush_closed_windows()
    metrics.flushed_windows += len(final_flushed)

    save_checkpoint(processor, CHECKPOINT_PATH)

    write_csv_rows(AGGREGATES_PATH, processor.flushed_aggregates)
    write_csv_rows(LATE_EVENTS_PATH, processor.late_events)
    write_csv_rows(DROPPED_EVENTS_PATH, processor.dropped_events)
    save_run_report(metrics, RUN_REPORT_PATH)

    logger.info("Traitement terminé.")
    logger.info("Aggregates: %s", AGGREGATES_PATH)
    logger.info("Late events: %s", LATE_EVENTS_PATH)
    logger.info("Dropped events: %s", DROPPED_EVENTS_PATH)
    logger.info("Run report: %s", RUN_REPORT_PATH)


if __name__ == "__main__":
    main()