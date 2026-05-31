import json
from pathlib import Path
from typing import Dict, Any, List

from broker import MiniBroker
from producers import EventProducer
from service import OrderService
from consumers import CityStatusConsumer, CourierZoneConsumer
from storage import PartitionedStore
from dashboard import Dashboard


def reset_environment() -> None:
    """
    Remet l'environnement à zéro avant chaque exécution.
    """

    offsets_dir = Path("offsets")
    offsets_dir.mkdir(parents=True, exist_ok=True)

    offsets_file = offsets_dir / "offsets.json"
    offsets_file.write_text("{}", encoding="utf-8")

    store = PartitionedStore()
    store.clear()


def create_demo_orders(service: OrderService) -> List[Dict[str, Any]]:
    """
    Crée plusieurs commandes de démonstration.
    """

    demo_orders = [
        {
            "customer_id": "CUST-001",
            "city": "Fes",
            "zone": "Atlas",
            "courier_id": "COURIER-001",
            "amount": 150.0,
            "items_count": 2
        },
        {
            "customer_id": "CUST-002",
            "city": "Casablanca",
            "zone": "Maarif",
            "courier_id": "COURIER-002",
            "amount": 250.0,
            "items_count": 4
        },
        {
            "customer_id": "CUST-003",
            "city": "Rabat",
            "zone": "Agdal",
            "courier_id": "COURIER-003",
            "amount": 90.0,
            "items_count": 1
        },
        {
            "customer_id": "CUST-004",
            "city": "Fes",
            "zone": "Narjiss",
            "courier_id": "COURIER-001",
            "amount": 320.0,
            "items_count": 5
        },
        {
            "customer_id": "CUST-005",
            "city": "Marrakech",
            "zone": "Gueliz",
            "courier_id": "COURIER-004",
            "amount": 180.0,
            "items_count": 3
        },
        {
            "customer_id": "CUST-006",
            "city": "Tanger",
            "zone": "Malabata",
            "courier_id": "COURIER-005",
            "amount": 210.0,
            "items_count": 2
        }
    ]

    created_orders = []

    print("\nCréation des commandes via le service synchrone...\n")

    for order_data in demo_orders:
        response = service.create_order(**order_data)

        if response["success"]:
            order = response["order"]
            created_orders.append(order)

            print(
                f"Commande créée : {order['order_id']} | "
                f"Ville : {order['city']} | "
                f"Statut : {order['status']}"
            )
        else:
            print("Erreur :", response["message"])

    return created_orders


def simulate_order_lifecycle(
    service: OrderService,
    created_orders: List[Dict[str, Any]]
) -> None:
    """
    Simule le cycle de vie des commandes.
    """

    print("\nSimulation du cycle de vie des commandes...\n")

    order_1 = created_orders[0]["order_id"]
    service.update_order_status(order_1, "prepared")
    service.update_order_status(order_1, "dispatched")
    service.update_order_status(order_1, "in_delivery")
    service.update_order_status(order_1, "delivered")
    print(f"{order_1} livrée avec succès.")

    order_2 = created_orders[1]["order_id"]
    service.update_order_status(order_2, "prepared")
    service.update_order_status(order_2, "dispatched")
    service.update_order_status(order_2, "in_delivery")
    service.update_order_status(order_2, "delivered")
    print(f"{order_2} livrée avec succès.")

    order_3 = created_orders[2]["order_id"]
    service.update_order_status(order_3, "prepared")
    service.update_order_status(order_3, "dispatched")
    service.update_order_status(order_3, "in_delivery")
    service.fail_order(order_3)
    print(f"{order_3} marquée comme échouée.")

    order_4 = created_orders[3]["order_id"]
    service.update_order_status(order_4, "prepared")
    service.update_order_status(order_4, "dispatched")
    print(f"{order_4} est en cours d'expédition.")

    order_5 = created_orders[4]["order_id"]
    service.cancel_order(order_5)
    print(f"{order_5} annulée.")

    order_6 = created_orders[5]["order_id"]
    print(f"{order_6} reste au statut created.")


def run_consumers(
    broker: MiniBroker,
    storage: PartitionedStore
) -> Dict[str, Dict[str, Any]]:
    """
    Lance les consumers.
    """

    print("\nLancement des consumers...\n")

    consumer_a = CityStatusConsumer(storage=storage)
    consumer_b = CourierZoneConsumer()

    processed_a = consumer_a.poll(broker)
    processed_b = consumer_b.poll(broker)

    print(f"Consumer A a traité {processed_a} événements.")
    print(f"Consumer B a traité {processed_b} événements.")

    return {
        "consumer_a": consumer_a.get_metrics(),
        "consumer_b": consumer_b.get_metrics()
    }


def generate_final_report(
    broker: MiniBroker,
    storage: PartitionedStore,
    metrics: Dict[str, Dict[str, Any]],
    output_file: str = "rapport_final.json"
) -> None:
    """
    Génère un rapport final JSON.
    """

    report = {
        "broker": {
            "total_events": broker.size(),
            "partitions": broker.get_partitions()
        },
        "storage": {
            "total_stored_events": storage.count_events(),
            "partitions": storage.get_partitions()
        },
        "metrics": metrics
    }

    Path(output_file).write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"\nRapport final généré : {output_file}")


def main() -> None:
    """
    Fonction principale du projet.
    """

    print("DÉMARRAGE DE LA PLATEFORME DISTRIBUÉE DE LIVRAISON")

    reset_environment()

    broker = MiniBroker(partition_key="city")
    producer = EventProducer(broker)
    service = OrderService(producer)
    storage = PartitionedStore(base_dir="data", partition_key="city")
    dashboard = Dashboard()

    created_orders = create_demo_orders(service)

    simulate_order_lifecycle(service, created_orders)

    print("\nÉtat des commandes dans le service :")
    service.print_orders()

    print("\nÉtat du broker avant consommation :")
    broker.print_state()

    metrics = run_consumers(broker, storage)

    print("\nÉtat du stockage après consommation :")
    storage.print_state()

    dashboard.render(
        broker=broker,
        consumer_a_metrics=metrics["consumer_a"],
        consumer_b_metrics=metrics["consumer_b"]
    )

    generate_final_report(
        broker=broker,
        storage=storage,
        metrics=metrics
    )

    print("\nEXÉCUTION TERMINÉE AVEC SUCCÈS")


if __name__ == "__main__":
    main()