from ingestion.api_service import IngestionService
from utils.storage import utc_now_iso

def produce_demo_events() -> None:
    service = IngestionService()
    now = utc_now_iso()

    orders = [
        {
            "event_id": "EVT-001",
            "order_id": "ORD-001",
            "restaurant_id": "R001",
            "order_type": "dine_in",
            "status": "received",
            "amount": 120.0,
            "items_count": 3,
            "event_ts": now,
            "source": "cash_register",
        },
        {
            "event_id": "EVT-002",
            "order_id": "ORD-001",
            "restaurant_id": "R001",
            "order_type": "dine_in",
            "status": "in_preparation",
            "amount": 120.0,
            "items_count": 3,
            "event_ts": now,
            "source": "cash_register",
        },
        {
            "event_id": "EVT-003",
            "order_id": "ORD-002",
            "restaurant_id": "R002",
            "order_type": "delivery",
            "status": "received",
            "amount": 95.5,
            "items_count": 2,
            "event_ts": now,
            "source": "mobile_app",
        },
        {
            "event_id": "EVT-004",
            "order_id": "ORD-003",
            "restaurant_id": "R999",
            "order_type": "delivery",
            "status": "received",
            "amount": 80.0,
            "items_count": 1,
            "event_ts": now,
            "source": "mobile_app",
        },
    ]

    payments = [
        {
            "payment_id": "PAY-001",
            "order_id": "ORD-001",
            "restaurant_id": "R001",
            "amount": 120.0,
            "payment_method": "card",
            "payment_status": "accepted",
            "event_ts": now,
        }
    ]

    snapshots = [
        {
            "snapshot_id": "SNP-001",
            "restaurant_id": "R001",
            "event_ts": now,
            "orders_in_progress": 5,
            "avg_prep_time_seconds": 900,
            "backlog_orders": 2,
            "active_staff": 6,
        }
    ]

    for event in orders:
        print(service.ingest_order(event))

    for event in payments:
        print(service.ingest_payment(event))

    for event in snapshots:
        print(service.ingest_snapshot(event))

if __name__ == "__main__":
    produce_demo_events()