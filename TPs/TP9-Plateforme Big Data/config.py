from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
BROKER_DIR = BASE_DIR / "broker_data"

BRONZE_DIR = STORAGE_DIR / "bronze"
SILVER_DIR = STORAGE_DIR / "silver"
GOLD_DIR = STORAGE_DIR / "gold"
CHECKPOINT_DIR = STORAGE_DIR / "checkpoints"

TOPICS = {
    "orders": "orders.events.v1",
    "payments": "payments.events.v1",
    "snapshots": "restaurant.snapshots.v1",
    "kpi": "kpi.realtime.v1",
    "invalid": "invalid.events.v1",
}

RESTAURANTS = {
    "R001": {"name": "Restaurant Fes Centre", "city": "Fes"},
    "R002": {"name": "Restaurant Rabat Agdal", "city": "Rabat"},
    "R003": {"name": "Restaurant Casablanca Maarif", "city": "Casablanca"},
}

VALID_ORDER_STATUS = {
    "received",
    "in_preparation",
    "ready",
    "served",
    "delivered",
    "paid",
    "cancelled",
}

VALID_TRANSITIONS = {
    None: {"received"},
    "received": {"in_preparation", "cancelled"},
    "in_preparation": {"ready", "cancelled"},
    "ready": {"served", "delivered", "cancelled"},
    "served": {"paid"},
    "delivered": {"paid"},
    "paid": set(),
    "cancelled": set(),
}