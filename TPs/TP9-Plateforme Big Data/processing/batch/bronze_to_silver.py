from config import BRONZE_DIR, SILVER_DIR, RESTAURANTS, VALID_TRANSITIONS
from observability.batch_metrics import BatchMetrics
from utils.storage import read_jsonl, append_jsonl, write_json, today_partition

def _read_category(category: str, date: str) -> list[dict]:
    return read_jsonl(
        BRONZE_DIR / category / f"date={date}" / "events.jsonl"
    )

def clean_orders(date: str | None = None) -> dict:
    date = date or today_partition()

    metrics = BatchMetrics("clean_orders")
    rows = _read_category("orders", date)
    metrics.rows_read = len(rows)

    seen_events: set[str] = set()
    last_status_by_order: dict[str, str | None] = {}

    for row in rows:
        event_id = row.get("event_id")
        order_id = row.get("order_id")
        restaurant_id = row.get("restaurant_id")
        status = row.get("status")

        if event_id in seen_events:
            metrics.rows_rejected += 1
            continue

        seen_events.add(event_id)

        if restaurant_id not in RESTAURANTS:
            metrics.rows_rejected += 1
            continue

        previous = last_status_by_order.get(order_id)

        if status not in VALID_TRANSITIONS.get(previous, set()):
            metrics.rows_rejected += 1
            continue

        last_status_by_order[order_id] = status

        clean = dict(row)
        clean["city"] = RESTAURANTS[restaurant_id]["city"]
        clean["restaurant_name"] = RESTAURANTS[restaurant_id]["name"]

        append_jsonl(
            SILVER_DIR / "orders_clean" / f"date={date}" / "events.jsonl",
            clean,
        )

        metrics.rows_written += 1

    write_json(
        SILVER_DIR / "_metrics" / f"clean_orders_{date}.json",
        metrics.snapshot("success"),
    )

    return metrics.snapshot("success")

def clean_payments(date: str | None = None) -> dict:
    date = date or today_partition()

    metrics = BatchMetrics("clean_payments")
    rows = _read_category("payments", date)
    metrics.rows_read = len(rows)

    seen: set[str] = set()

    for row in rows:
        payment_id = row.get("payment_id")
        restaurant_id = row.get("restaurant_id")

        if payment_id in seen or restaurant_id not in RESTAURANTS:
            metrics.rows_rejected += 1
            continue

        seen.add(payment_id)

        clean = dict(row)
        clean["city"] = RESTAURANTS[restaurant_id]["city"]
        clean["restaurant_name"] = RESTAURANTS[restaurant_id]["name"]

        append_jsonl(
            SILVER_DIR / "payments_clean" / f"date={date}" / "events.jsonl",
            clean,
        )

        metrics.rows_written += 1

    write_json(
        SILVER_DIR / "_metrics" / f"clean_payments_{date}.json",
        metrics.snapshot("success"),
    )

    return metrics.snapshot("success")

def clean_snapshots(date: str | None = None) -> dict:
    date = date or today_partition()

    metrics = BatchMetrics("clean_snapshots")
    rows = _read_category("snapshots", date)
    metrics.rows_read = len(rows)

    for row in rows:
        restaurant_id = row.get("restaurant_id")

        if restaurant_id not in RESTAURANTS:
            metrics.rows_rejected += 1
            continue

        clean = dict(row)
        clean["city"] = RESTAURANTS[restaurant_id]["city"]
        clean["restaurant_name"] = RESTAURANTS[restaurant_id]["name"]

        append_jsonl(
            SILVER_DIR / "snapshots_clean" / f"date={date}" / "events.jsonl",
            clean,
        )

        metrics.rows_written += 1

    write_json(
        SILVER_DIR / "_metrics" / f"clean_snapshots_{date}.json",
        metrics.snapshot("success"),
    )

    return metrics.snapshot("success")