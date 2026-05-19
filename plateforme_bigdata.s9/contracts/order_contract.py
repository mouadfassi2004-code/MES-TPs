from dataclasses import dataclass, asdict
from typing import Any
from config import VALID_ORDER_STATUS

@dataclass
class OrderEvent:
    event_id: str
    order_id: str
    restaurant_id: str
    order_type: str
    status: str
    amount: float
    items_count: int
    event_ts: str
    source: str
    schema_version: str = "v1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def validate(data: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        required = [
            "event_id",
            "order_id",
            "restaurant_id",
            "order_type",
            "status",
            "amount",
            "items_count",
            "event_ts",
            "source",
        ]

        for field in required:
            if field not in data or data[field] in (None, ""):
                errors.append(f"Champ obligatoire manquant: {field}")

        if data.get("order_type") not in {"dine_in", "takeaway", "delivery"}:
            errors.append("order_type invalide")

        if data.get("status") not in VALID_ORDER_STATUS:
            errors.append("status invalide")

        try:
            if float(data.get("amount", 0)) <= 0:
                errors.append("amount doit être strictement positif")
        except (TypeError, ValueError):
            errors.append("amount doit être numérique")

        try:
            if int(data.get("items_count", 0)) <= 0:
                errors.append("items_count doit être >= 1")
        except (TypeError, ValueError):
            errors.append("items_count doit être entier")

        return errors