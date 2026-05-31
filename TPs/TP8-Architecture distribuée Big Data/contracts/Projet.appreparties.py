from dataclasses import dataclass
from typing import Dict, Any


# Liste des statuts autorisés pour une commande.
# Cela évite les valeurs incohérentes comme "done", "finish", "livré", etc.
VALID_ORDER_STATUSES = {
    "created",
    "prepared",
    "dispatched",
    "in_delivery",
    "delivered",
    "failed",
    "cancelled"
}


@dataclass
class Order:
    """
    Classe qui représente une commande.

    Dans notre projet, Order est un contrat de données.
    Cela veut dire que toutes les commandes doivent respecter cette structure.
    """

    order_id: str
    customer_id: str
    city: str
    zone: str
    courier_id: str
    amount: float
    items_count: int
    status: str = "created"

    def validate(self) -> None:
        """
        Vérifie que la commande est correcte.

        Cette méthode empêche les données invalides d'entrer dans le système.
        Dans une application distribuée, c'est très important parce qu'une
        mauvaise donnée peut se propager vers le broker, les consumers
        et le stockage.
        """

        if not self.order_id:
            raise ValueError("order_id ne peut pas être vide.")

        if not self.customer_id:
            raise ValueError("customer_id ne peut pas être vide.")

        if not self.city:
            raise ValueError("city ne peut pas être vide.")

        if not self.zone:
            raise ValueError("zone ne peut pas être vide.")

        if not self.courier_id:
            raise ValueError("courier_id ne peut pas être vide.")

        if self.amount <= 0:
            raise ValueError("amount doit être supérieur à 0.")

        if self.items_count <= 0:
            raise ValueError("items_count doit être supérieur à 0.")

        if self.status not in VALID_ORDER_STATUSES:
            raise ValueError(f"Statut invalide : {self.status}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Order en dictionnaire Python.

        Cette méthode sera utile pour :
        - transformer la commande en JSON ;
        - envoyer la commande entre composants ;
        - sauvegarder la commande dans un fichier.
        """

        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "city": self.city,
            "zone": self.zone,
            "courier_id": self.courier_id,
            "amount": self.amount,
            "items_count": self.items_count,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        """
        Crée un objet Order à partir d'un dictionnaire.

        Cette méthode est l'inverse de to_dict().
        Elle sera utile lorsqu'on reçoit des données sous forme de dictionnaire
        ou de JSON et qu'on veut les transformer en objet Python.
        """

        order = cls(
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            city=data["city"],
            zone=data["zone"],
            courier_id=data["courier_id"],
            amount=float(data["amount"]),
            items_count=int(data["items_count"]),
            status=data.get("status", "created")
        )

        order.validate()
        return order