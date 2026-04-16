import json
import logging
import os
import threading


_metrics_lock = threading.Lock()
_metrics = {
    "total_calls": 0,
    "success_calls": 0,
    "error_calls": 0,
    "latencies_ms": [],
}


def setup_logger(name: str, logfile: str):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter("%(message)s")

    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def log_json(logger, **kwargs):
    logger.info(json.dumps(kwargs, ensure_ascii=False))


def record_metric(success: bool, latency_ms: float):
    with _metrics_lock:
        _metrics["total_calls"] += 1
        if success:
            _metrics["success_calls"] += 1
        else:
            _metrics["error_calls"] += 1
        _metrics["latencies_ms"].append(latency_ms)


def dump_metrics():
    os.makedirs("outputs", exist_ok=True)
    avg_latency = 0.0
    if _metrics["latencies_ms"]:
        avg_latency = sum(_metrics["latencies_ms"]) / len(_metrics["latencies_ms"])

    payload = {
        "total_calls": _metrics["total_calls"],
        "success_calls": _metrics["success_calls"],
        "error_calls": _metrics["error_calls"],
        "avg_latency_ms": round(avg_latency, 2),
    }

    with open("outputs/run_report.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)