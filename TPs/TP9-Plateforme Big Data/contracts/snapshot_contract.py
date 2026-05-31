from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class RestaurantSnapshot:
    snapshot_id: str
    restaurant_id: str
    event_ts: str
    orders_in_progress: int
    avg_prep_time_seconds: int
    backlog_orders: int
    active_staff: int = 0
    schema_version: str = "v1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def validate(data: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        required = [
            "snapshot_id",
            "restaurant_id",
            "event_ts",
            "orders_in_progress",
            "avg_prep_time_seconds",
            "backlog_orders",
        ]

        for field in required:
            if field not in data or data[field] in (None, ""):
                errors.append(f"Champ obligatoire manquant: {field}")

        for field in [
            "orders_in_progress",
            "avg_prep_time_seconds",
            "backlog_orders",
            "active_staff",
        ]:
            if field in data:
                try:
                    if int(data[field]) < 0:
                        errors.append(f"{field} doit être >= 0")
                except (TypeError, ValueError):
                    errors.append(f"{field} doit être entier")

        return errors