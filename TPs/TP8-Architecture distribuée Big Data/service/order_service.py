import uuid
from threading import Lock
from typing import Dict, Any, List

from contracts.order import Order, VALID_ORDER_STATUSES
from producers import EventProducer


class OrderService:
    """
    OrderService représente le service synchrone de gestion des commandes.

    Son rôle est de :
    - recevoir une demande de création de commande ;
    - valider les données ;
    - créer un objet Order ;
    - stocker la commande en mémoire ;
    - publier un événement dans le broker via EventProducer ;
    - retourner une réponse immédiate au client.

    Dans un vrai système, ce service pourrait être une API HTTP.
    Ici, on le simule avec une classe Python.
    """

    def __init__(self, producer: EventProducer) -> None:
        """
        Initialise le service de commande.

        producer :
            Objet EventProducer utilisé pour publier les événements
            dans le broker.
        """

        self.producer = producer

        # Stockage temporaire des commandes en mémoire.
        # Exemple :
        # {
        #   "ORD-001": Order(...),
        #   "ORD-002": Order(...)
        # }
        self.orders: Dict[str, Order] = {}

        # Lock pour éviter les problèmes si plusieurs actions arrivent
        # en même temps.
        self.lock = Lock()

    def _generate_order_id(self) -> str:
        """
        Génère un identifiant unique pour une commande.

        Exemple :
        ORD-7F3A21B9
        """

        unique_part = str(uuid.uuid4())[:8].upper()
        return f"ORD-{unique_part}"

    def create_order(
        self,
        customer_id: str,
        city: str,
        zone: str,
        courier_id: str,
        amount: float,
        items_count: int
    ) -> Dict[str, Any]:
        """
        Crée une nouvelle commande.

        Cette méthode représente une action synchrone :
        le client envoie les informations de la commande
        et reçoit immédiatement une réponse.

        Étapes :
        1. Générer un order_id.
        2. Créer un objet Order.
        3. Valider la commande.
        4. Stocker la commande.
        5. Publier un événement order_created.
        6. Retourner une réponse au client.
        """

        order_id = self._generate_order_id()

        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            city=city,
            zone=zone,
            courier_id=courier_id,
            amount=amount,
            items_count=items_count,
            status="created"
        )

        order.validate()

        with self.lock:
            self.orders[order_id] = order

        publication_result = self.producer.publish_order_created(order)

        return {
            "success": True,
            "message": "Commande créée avec succès.",
            "order": order.to_dict(),
            "event_publication": publication_result
        }

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Retourne les informations d'une commande.

        Cette méthode est aussi synchrone :
        on demande l'état actuel d'une commande et on reçoit
        une réponse immédiate.
        """

        with self.lock:
            order = self.orders.get(order_id)

        if order is None:
            return {
                "success": False,
                "message": f"Aucune commande trouvée avec l'id {order_id}."
            }

        return {
            "success": True,
            "order": order.to_dict()
        }

    def update_order_status(self, order_id: str, new_status: str) -> Dict[str, Any]:
        """
        Met à jour le statut d'une commande.

        Exemple :
        created -> prepared
        prepared -> dispatched
        dispatched -> in_delivery
        in_delivery -> delivered

        Après chaque changement de statut, un événement est publié
        dans le broker.
        """

        if new_status not in VALID_ORDER_STATUSES:
            return {
                "success": False,
                "message": f"Statut invalide : {new_status}"
            }

        with self.lock:
            order = self.orders.get(order_id)

        if order is None:
            return {
                "success": False,
                "message": f"Aucune commande trouvée avec l'id {order_id}."
            }

        if order.status in {"delivered", "failed", "cancelled"}:
            return {
                "success": False,
                "message": (
                    f"Impossible de modifier la commande {order_id}, "
                    f"car son statut final est déjà '{order.status}'."
                )
            }

        publication_result = self.producer.publish_status_update(order, new_status)

        return {
            "success": True,
            "message": f"Statut de la commande mis à jour vers '{new_status}'.",
            "order": order.to_dict(),
            "event_publication": publication_result
        }

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Annule une commande.

        Une commande peut être annulée seulement si elle n'est pas déjà :
        - livrée ;
        - échouée ;
        - annulée.
        """

        with self.lock:
            order = self.orders.get(order_id)

        if order is None:
            return {
                "success": False,
                "message": f"Aucune commande trouvée avec l'id {order_id}."
            }

        if order.status in {"delivered", "failed", "cancelled"}:
            return {
                "success": False,
                "message": (
                    f"Impossible d'annuler la commande {order_id}, "
                    f"car son statut actuel est '{order.status}'."
                )
            }

        publication_result = self.producer.publish_cancelled_order(order)

        return {
            "success": True,
            "message": "Commande annulée avec succès.",
            "order": order.to_dict(),
            "event_publication": publication_result
        }

    def fail_order(self, order_id: str) -> Dict[str, Any]:
        """
        Marque une commande comme échouée.

        Exemple :
        - client absent ;
        - adresse incorrecte ;
        - problème logistique.
        """

        with self.lock:
            order = self.orders.get(order_id)

        if order is None:
            return {
                "success": False,
                "message": f"Aucune commande trouvée avec l'id {order_id}."
            }

        if order.status in {"delivered", "failed", "cancelled"}:
            return {
                "success": False,
                "message": (
                    f"Impossible de marquer la commande {order_id} comme échouée, "
                    f"car son statut actuel est '{order.status}'."
                )
            }

        publication_result = self.producer.publish_failed_order(order)

        return {
            "success": True,
            "message": "Commande marquée comme échouée.",
            "order": order.to_dict(),
            "event_publication": publication_result
        }

    def list_orders(self) -> List[Dict[str, Any]]:
        """
        Retourne toutes les commandes stockées dans le service.
        """

        with self.lock:
            return [order.to_dict() for order in self.orders.values()]

    def count_orders(self) -> int:
        """
        Retourne le nombre total de commandes.
        """

        with self.lock:
            return len(self.orders)

    def print_orders(self) -> None:
        """
        Affiche toutes les commandes dans le terminal.

        Cette méthode est utile pour les tests et pour la présentation.
        """

        print("\n========== COMMANDES DANS LE SERVICE ==========")

        with self.lock:
            if not self.orders:
                print("Aucune commande enregistrée.")
                print("===============================================\n")
                return

            for order_id, order in self.orders.items():
                print(
                    f"{order_id} | "
                    f"Client {order.customer_id} | "
                    f"Ville {order.city} | "
                    f"Zone {order.zone} | "
                    f"Livreur {order.courier_id} | "
                    f"Montant {order.amount} DH | "
                    f"Statut {order.status}"
                )

        print("===============================================\n")