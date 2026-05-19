from typing import Any
from config import BRONZE_DIR, TOPICS, RESTAURANTS
from contracts.order_contract import OrderEvent
from contracts.payment_contract import PaymentEvent
from contracts.snapshot_contract import RestaurantSnapshot
from messaging.simple_broker import SimpleBroker
from utils.storage import append_jsonl, today_partition, utc_now_iso

class IngestionService:
    """
    Service d'ingestion synchrone simplifié.
    Dans un vrai projet, ce fichier serait une API HTTP.
    Ici, on simule les endpoints avec des méthodes Python.
    """

    def __init__(self):
        self.broker = SimpleBroker()

    def _write_bronze(self, category: str, event: dict[str, Any]) -> None:
        date = today_partition()
        path = BRONZE_DIR / category / f"date={date}" / "events.jsonl"
        append_jsonl(path, event)

    def _reject(
        self,
        event_type: str,
        data: dict[str, Any],
        errors: list[str],
    ) -> dict[str, Any]:
        rejected = {
            "event_type": event_type,
            "server_ts": utc_now_iso(),
            "errors": errors,
            "raw_event": data,
        }

        self._write_bronze("rejected", rejected)
        self.broker.publish(TOPICS["invalid"], rejected)

        return {
            "status": 400,
            "message": "rejected",
            "errors": errors,
        }

    def ingest_order(self, data: dict[str, Any]) -> dict[str, Any]:
        errors = OrderEvent.validate(data)

        if data.get("restaurant_id") not in RESTAURANTS:
            errors.append("restaurant_id inconnu")

        if errors:
            return self._reject("order", data, errors)

        enriched = dict(data)
        enriched["server_ts"] = utc_now_iso()
        enriched["schema_version"] = "v1"

        self._write_bronze("orders", enriched)
        offset = self.broker.publish(TOPICS["orders"], enriched)

        return {
            "status": 202,
            "message": "order accepted",
            "topic": TOPICS["orders"],
            "offset": offset,
        }

    def ingest_payment(self, data: dict[str, Any]) -> dict[str, Any]:
        errors = PaymentEvent.validate(data)

        if data.get("restaurant_id") not in RESTAURANTS:
            errors.append("restaurant_id inconnu")

        if errors:
            return self._reject("payment", data, errors)

        enriched = dict(data)
        enriched["server_ts"] = utc_now_iso()
        enriched["schema_version"] = "v1"

        self._write_bronze("payments", enriched)
        offset = self.broker.publish(TOPICS["payments"], enriched)

        return {
            "status": 202,
            "message": "payment accepted",
            "topic": TOPICS["payments"],
            "offset": offset,
        }

    def ingest_snapshot(self, data: dict[str, Any]) -> dict[str, Any]:
        errors = RestaurantSnapshot.validate(data)

        if data.get("restaurant_id") not in RESTAURANTS:
            errors.append("restaurant_id inconnu")

        if errors:
            return self._reject("snapshot", data, errors)

        enriched = dict(data)
        enriched["server_ts"] = utc_now_iso()
        enriched["schema_version"] = "v1"

        self._write_bronze("snapshots", enriched)
        offset = self.broker.publish(TOPICS["snapshots"], enriched)

        return {
            "status": 202,
            "message": "snapshot accepted",
            "topic": TOPICS["snapshots"],
            "offset": offset,
        }