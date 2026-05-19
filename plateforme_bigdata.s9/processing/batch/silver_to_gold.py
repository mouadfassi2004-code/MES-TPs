from collections import defaultdict
from config import SILVER_DIR, GOLD_DIR
from observability.batch_metrics import BatchMetrics
from utils.storage import read_jsonl, write_json, today_partition, utc_now_iso

def compute_daily_report(date: str | None = None) -> dict:
    date = date or today_partition()

    metrics = BatchMetrics("compute_daily_report")

    orders = read_jsonl(
        SILVER_DIR / "orders_clean" / f"date={date}" / "events.jsonl"
    )

    payments = read_jsonl(
        SILVER_DIR / "payments_clean" / f"date={date}" / "events.jsonl"
    )

    snapshots = read_jsonl(
        SILVER_DIR / "snapshots_clean" / f"date={date}" / "events.jsonl"
    )

    metrics.rows_read = len(orders) + len(payments) + len(snapshots)

    orders_by_restaurant = defaultdict(int)
    revenue_by_restaurant = defaultdict(float)
    backlog_by_restaurant = {}

    for order in orders:
        restaurant_id = order["restaurant_id"]

        if order["status"] == "received":
            orders_by_restaurant[restaurant_id] += 1

    for payment in payments:
        if payment["payment_status"] == "accepted":
            restaurant_id = payment["restaurant_id"]
            revenue_by_restaurant[restaurant_id] += float(payment["amount"])

    for snapshot in snapshots:
        restaurant_id = snapshot["restaurant_id"]
        backlog_by_restaurant[restaurant_id] = snapshot["backlog_orders"]

    restaurants = (
        set(orders_by_restaurant)
        | set(revenue_by_restaurant)
        | set(backlog_by_restaurant)
    )

    report = []

    for restaurant_id in sorted(restaurants):
        total_orders = orders_by_restaurant.get(restaurant_id, 0)
        total_revenue = revenue_by_restaurant.get(restaurant_id, 0.0)

        if total_orders:
            avg_basket = round(total_revenue / total_orders, 2)
        else:
            avg_basket = 0.0

        report.append(
            {
                "date": date,
                "restaurant_id": restaurant_id,
                "total_orders": total_orders,
                "total_revenue": round(total_revenue, 2),
                "avg_basket": avg_basket,
                "last_backlog": backlog_by_restaurant.get(restaurant_id, 0),
            }
        )

    output = {
        "generated_at": utc_now_iso(),
        "date": date,
        "rows": report,
    }

    write_json(
        GOLD_DIR / "daily_reports" / f"date={date}" / "report.json",
        output,
    )

    metrics.rows_written = len(report)

    write_json(
        GOLD_DIR / "_metrics" / f"compute_daily_report_{date}.json",
        metrics.snapshot("success"),
    )

    return output