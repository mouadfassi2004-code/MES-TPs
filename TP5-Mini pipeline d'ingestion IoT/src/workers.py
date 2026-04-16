import logging
import queue
import random
import threading
import time

from messages import EventMessage, is_valid_reading
from metrics import Metrics
from storage import Storage


def simulate_processing() -> None:
    # ~80 msg/s par worker environ
    time.sleep(random.uniform(0.008, 0.018))


def worker(
    name: str,
    main_queue: queue.Queue,
    dead_letter_queue: queue.Queue,
    stop_event: threading.Event,
    metrics: Metrics,
    storage: Storage,
) -> None:
    logging.info("[%s] started", name)

    while True:
        if stop_event.is_set() and main_queue.empty():
            break

        try:
            msg = main_queue.get(timeout=0.5)
        except queue.Empty:
            continue

        try:
            valid, reason = is_valid_reading(msg.payload)

            if not valid:
                raise ValueError(reason)

            simulate_processing()

            latency = time.time() - msg.created_at
            storage.save_valid_message(msg)
            metrics.inc_processed(latency)

            logging.info(
                "[%s] processed msg=%s sensor=%s metric=%s value=%s",
                name,
                msg.msg_id[:8],
                msg.payload["sensor_id"],
                msg.payload["metric"],
                msg.payload["value"],
            )

        except Exception as exc:
            metrics.inc_failed()
            msg.attempts += 1

            if msg.should_retry():
                try:
                    main_queue.put(msg, timeout=0.2)
                    metrics.inc_retried()
                    logging.warning(
                        "[%s] retry msg=%s attempt=%d reason=%s",
                        name,
                        msg.msg_id[:8],
                        msg.attempts,
                        str(exc),
                    )
                except queue.Full:
                    dead_letter_queue.put(msg)
                    storage.save_dead_letter(msg, f"Main queue full during retry: {exc}")
                    metrics.inc_dead_lettered()
                    logging.error(
                        "[%s] DLQ (retry failed because queue full) msg=%s",
                        name,
                        msg.msg_id[:8],
                    )
            else:
                dead_letter_queue.put(msg)
                storage.save_dead_letter(msg, str(exc))
                metrics.inc_dead_lettered()
                logging.error(
                    "[%s] DLQ msg=%s attempts=%d reason=%s",
                    name,
                    msg.msg_id[:8],
                    msg.attempts,
                    str(exc),
                )
        finally:
            main_queue.task_done()

    logging.info("[%s] stopped", name)