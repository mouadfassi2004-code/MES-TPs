from typing import Any, Dict, List, Optional

from contracts.order import Order, VALID_ORDER_STATUSES
from contracts.event import Event


class EventProducer:
    """
    EventProducer est responsable de la création et de la publication
    des événements métier.

    Son rôle est de :
    - recevoir une commande ;
    - créer un événement correspondant à son état ;
    - publier cet événement dans le broker.

    Exemple :
    Une commande passe de "created" à "delivered".
    Le producer crée alors un événement "order_delivered"
    et l'envoie au broker.
    """

    def __init__(self, broker: Any, name: str = "event_producer") -> None:
        """
        Initialise le producer.

        broker :
            Le broker dans lequel les événements seront publiés.

        name :
            Le nom du producer, utile pour l'affichage et le suivi.
        """

        self.broker = broker
        self.name = name

    def _status_to_event_type(self, status: str) -> str:
        """
        Transforme un statut de commande en type d'événement.

        Exemple :
        status = "created"
        event_type = "order_created"
        """

        mapping = {
            "created": "order_created",
            "prepared": "order_prepared",
            "dispatched": "order_dispatched",
            "in_delivery": "order_in_delivery",
            "delivered": "order_delivered",
            "failed": "order_failed",
            "cancelled": "order_cancelled"
        }

        if status not in mapping:
            raise ValueError(f"Impossible de créer un événement pour le statut : {status}")

        return mapping[status]

    def _publish_event(
        self,
        order_id: str,
        event_type: str,
        city: str,
        zone: str,
        courier_id: str,
        status: str
    ) -> Dict[str, Any]:
        """
        Crée un événement puis le publie dans le broker.

        Cette méthode est interne.
        Elle évite de répéter le même code plusieurs fois.
        """

        event = Event.create(
            order_id=order_id,
            event_type=event_type,
            city=city,
            zone=zone,
            courier_id=courier_id,
            status=status
        )

        publication_result = self.broker.publish(event)

        return {
            "producer": self.name,
            "partition": publication_result["partition"],
            "offset": publication_result["offset"],
            "event_id": publication_result["event_id"],
            "event_type": publication_result["event_type"],
            "order_id": order_id,
            "status": status
        }

    def publish_order_created(self, order: Order) -> Dict[str, Any]:
        """
        Publie l'événement de création d'une commande.

        Cet événement est généralement créé juste après
        la validation de la commande.
        """

        order.validate()

        return self._publish_event(
            order_id=order.order_id,
            event_type="order_created",
            city=order.city,
            zone=order.zone,
            courier_id=order.courier_id,
            status=order.status
        )

    def publish_status_update(self, order: Order, new_status: str) -> Dict[str, Any]:
        """
        Change le statut d'une commande et publie l'événement correspondant.

        Exemple :
        new_status = "delivered"
        événement créé = "order_delivered"
        """

        if new_status not in VALID_ORDER_STATUSES:
            raise ValueError(f"Statut invalide : {new_status}")

        order.status = new_status
        order.validate()

        event_type = self._status_to_event_type(new_status)

        return self._publish_event(
            order_id=order.order_id,
            event_type=event_type,
            city=order.city,
            zone=order.zone,
            courier_id=order.courier_id,
            status=order.status
        )

    def publish_lifecycle(
        self,
        order: Order,
        statuses: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Publie plusieurs événements pour simuler le cycle de vie d'une commande.

        Exemple de cycle :
        prepared -> dispatched -> in_delivery -> delivered

        Cette méthode est utile pour tester le système rapidement.
        """

        if statuses is None:
            statuses = ["prepared", "dispatched", "in_delivery", "delivered"]

        results = []

        for status in statuses:
            result = self.publish_status_update(order, status)
            results.append(result)

        return results

    def publish_failed_order(self, order: Order) -> Dict[str, Any]:
        """
        Publie un événement indiquant qu'une commande a échoué.

        Exemple :
        livraison impossible, client absent, problème logistique, etc.
        """

        return self.publish_status_update(order, "failed")

    def publish_cancelled_order(self, order: Order) -> Dict[str, Any]:
        """
        Publie un événement indiquant qu'une commande a été annulée.
        """

        return self.publish_status_update(order, "cancelled")