from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime
import uuid


# Liste des types d'événements autorisés dans notre système.
# Chaque événement décrit une action qui s'est produite sur une commande.
VALID_EVENT_TYPES = {
    "order_created",
    "order_prepared",
    "order_dispatched",
    "order_in_delivery",
    "order_delivered",
    "order_failed",
    "order_cancelled"
}

@dataclass
class Event:
    """
    Classe qui représente un événement métier.

    Un événement décrit quelque chose qui s'est produit dans le système.
    Exemple :
    - une commande a été créée ;
    - une commande a été préparée ;
    - une commande a été livrée ;
    - une commande a échoué.
    """

    event_id: str
    order_id: str
    event_type: str
    timestamp: str
    city: str
    zone: str
    courier_id: str
    status: str

    def validate(self) -> None:
        """
        Vérifie que l'événement est correct.

        Cette validation évite de publier dans le broker des événements
        incomplets ou incohérents.
        """

        if not self.event_id:
            raise ValueError("event_id ne peut pas être vide.")

        if not self.order_id:
            raise ValueError("order_id ne peut pas être vide.")

        if self.event_type not in VALID_EVENT_TYPES:
            raise ValueError(f"Type d'événement invalide : {self.event_type}")

        if not self.timestamp:
            raise ValueError("timestamp ne peut pas être vide.")

        if not self.city:
            raise ValueError("city ne peut pas être vide.")

        if not self.zone:
            raise ValueError("zone ne peut pas être vide.")

        if not self.courier_id:
            raise ValueError("courier_id ne peut pas être vide.")

        if not self.status:
            raise ValueError("status ne peut pas être vide.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Event en dictionnaire Python.

        Cette méthode sera utilisée avant :
        - la publication dans le broker ;
        - l'écriture dans un fichier ;
        - l'affichage dans le dashboard.
        """

        return {
            "event_id": self.event_id,
            "order_id": self.order_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "city": self.city,
            "zone": self.zone,
            "courier_id": self.courier_id,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """
        Crée un objet Event à partir d'un dictionnaire.

        Cette méthode est utile quand on lit un événement depuis le broker
        ou depuis un fichier JSON.
        """

        event = cls(
            event_id=data["event_id"],
            order_id=data["order_id"],
            event_type=data["event_type"],
            timestamp=data["timestamp"],
            city=data["city"],
            zone=data["zone"],
            courier_id=data["courier_id"],
            status=data["status"]
        )

        event.validate()
        return event

    @classmethod
    def create(
        cls,
        order_id: str,
        event_type: str,
        city: str,
        zone: str,
        courier_id: str,
        status: str
    ) -> "Event":
        """
        Crée automatiquement un nouvel événement.

        Cette méthode génère automatiquement :
        - un event_id unique ;
        - un timestamp actuel.

        Comme ça, on évite d'écrire manuellement ces informations
        à chaque création d'événement.
        """

        event = cls(
            event_id=str(uuid.uuid4()),
            order_id=order_id,
            event_type=event_type,
            timestamp=datetime.now().isoformat(timespec="seconds"),
            city=city,
            zone=zone,
            courier_id=courier_id,
            status=status
        )

        event.validate()
        return event