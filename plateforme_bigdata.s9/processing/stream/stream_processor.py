from config import TOPICS, GOLD_DIR
from messaging.simple_broker import SimpleBroker
from observability.stream_metrics import StreamMetrics
from utils.storage import append_jsonl, utc_now_iso, write_json

class StreamProcessor:
    """
    Processor temps réel simplifié.
    Il lit les topics, maintient un état en mémoire,
    puis écrit des KPIs temps réel dans la zone gold.
    """

    def __init__(self):
        self.broker = SimpleBroker()
        self.consumer_group = "stream_processor_group"
        self.metrics = StreamMetrics()

        self.order_status: dict[str, str] = {}
        self.orders_in_progress_by_restaurant: dict[str, int] = {}
        self.revenue_by_restaurant: dict[str, float] = {}

    def process_orders(self) -> None:
        messages = self.broker.consume(
            TOPICS["orders"],
            self.consumer_group,
        )

        for msg in messages:
            event = msg["value"]

            order_id = event["order_id"]
            restaurant_id = event["restaurant_id"]
            status = event["status"]

            previous_status = self.order_status.get(order_id)
            self.order_status[order_id] = status

            if previous_status is None and status == "received":
                self.orders_in_progress_by_restaurant[restaurant_id] = (
                    self.orders_in_progress_by_restaurant.get(restaurant_id, 0) + 1
                )

            if (
                status in {"served", "delivered", "paid", "cancelled"}
                and previous_status not in {"served", "delivered", "paid", "cancelled"}
            ):
                self.orders_in_progress_by_restaurant[restaurant_id] = max(
                    0,
                    self.orders_in_progress_by_restaurant.get(restaurant_id, 0) - 1,
                )

            self.metrics.inc_processed()
            self.broker.commit(
                TOPICS["orders"],
                self.consumer_group,
                msg["offset"],
            )

    def process_payments(self) -> None:
        messages = self.broker.consume(
            TOPICS["payments"],
            self.consumer_group,
        )

        for msg in messages:
            event = msg["value"]

            if event["payment_status"] == "accepted":
                restaurant_id = event["restaurant_id"]
                self.revenue_by_restaurant[restaurant_id] = (
                    self.revenue_by_restaurant.get(restaurant_id, 0.0)
                    + float(event["amount"])
                )

            self.metrics.inc_processed()
            self.broker.commit(
                TOPICS["payments"],
                self.consumer_group,
                msg["offset"],
            )

    def write_realtime_kpis(self) -> None:
        result = {
            "timestamp": utc_now_iso(),
            "orders_in_progress_by_restaurant": self.orders_in_progress_by_restaurant,
            "revenue_by_restaurant": self.revenue_by_restaurant,
            "metrics": self.metrics.snapshot(),
        }

        write_json(
            GOLD_DIR / "kpis" / "realtime_kpis.json",
            result,
        )

        append_jsonl(
            GOLD_DIR / "kpis" / "realtime_kpis_history.jsonl",
            result,
        )

    def run_once(self) -> None:
        self.process_orders()
        self.process_payments()
        self.write_realtime_kpis()

        print("Stream processor terminé. KPIs temps réel écrits dans storage/gold/kpis/")