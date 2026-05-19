from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class PaymentEvent:
    payment_id: str
    order_id: str
    restaurant_id: str
    amount: float
    payment_method: str
    payment_status: str
    event_ts: str
    schema_version: str = "v1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def validate(data: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        required = [
            "payment_id",
            "order_id",
            "restaurant_id",
            "amount",
            "payment_method",
            "payment_status",
            "event_ts",
        ]

        for field in required:
            if field not in data or data[field] in (None, ""):
                errors.append(f"Champ obligatoire manquant: {field}")

        if data.get("payment_method") not in {"cash", "card", "app"}:
            errors.append("payment_method invalide")

        if data.get("payment_status") not in {"accepted", "refused", "refunded"}:
            errors.append("payment_status invalide")

        try:
            if float(data.get("amount", 0)) <= 0:
                errors.append("amount doit être strictement positif")
        except (TypeError, ValueError):
            errors.append("amount doit être numérique")

        return errors