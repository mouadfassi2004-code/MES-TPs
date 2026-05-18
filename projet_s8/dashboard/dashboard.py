from typing import Dict, Any, Optional
from datetime import datetime


class Dashboard:
    """
    Dashboard représente le tableau de bord du projet.

    Son rôle est d'afficher :
    - l'état du broker ;
    - les statistiques du consumer A ;
    - les statistiques du consumer B ;
    - les offsets sauvegardés ;
    - les commandes échouées.

    Dans un vrai système Big Data, le dashboard pourrait être une interface web.
    Ici, on fait un dashboard simple dans le terminal.
    """

    def __init__(self, title: str = "Plateforme distribuée de suivi de commandes") -> None:
        """
        Initialise le dashboard.

        title :
            Titre affiché en haut du tableau de bord.
        """

        self.title = title

    def _print_separator(self) -> None:
        """
        Affiche une ligne de séparation.
        """

        print("=" * 75)

    def _print_section(self, title: str) -> None:
        """
        Affiche le titre d'une section.
        """

        print()
        print("-" * 75)
        print(title)
        print("-" * 75)

    def _print_dict(self, data: Dict[str, Any], empty_message: str = "Aucune donnée.") -> None:
        """
        Affiche proprement un dictionnaire simple.

        Exemple :
        {
            "Fes": 4,
            "Rabat": 2
        }
        """

        if not data:
            print(empty_message)
            return

        for key, value in data.items():
            print(f"  {key} : {value}")

    def _print_nested_dict(
        self,
        data: Dict[str, Dict[str, int]],
        empty_message: str = "Aucune donnée détaillée."
    ) -> None:
        """
        Affiche un dictionnaire imbriqué.

        Exemple :
        {
            "Fes": {
                "created": 3,
                "delivered": 1
            }
        }
        """

        if not data:
            print(empty_message)
            return

        for main_key, sub_data in data.items():
            print(f"  {main_key} :")

            if not sub_data:
                print("    Aucune donnée.")
            else:
                for sub_key, value in sub_data.items():
                    print(f"    {sub_key} : {value}")

    def _get_total_from_dict(self, data: Dict[str, int]) -> int:
        """
        Calcule le total des valeurs d'un dictionnaire.

        Exemple :
        {"Fes": 3, "Rabat": 2} donne 5.
        """

        return sum(data.values())

    def _get_top_item(self, data: Dict[str, int]) -> Optional[tuple]:
        """
        Retourne l'élément ayant la valeur la plus élevée.

        Exemple :
        {"Fes": 3, "Rabat": 7} donne ("Rabat", 7).
        """

        if not data:
            return None

        return max(data.items(), key=lambda item: item[1])

    def show_header(self) -> None:
        """
        Affiche l'en-tête du dashboard.
        """

        self._print_separator()
        print(self.title.upper())
        print(f"Date d'affichage : {datetime.now().isoformat(timespec='seconds')}")
        self._print_separator()

    def show_broker_state(self, broker: Any) -> None:
        """
        Affiche l'état général du broker.

        On affiche :
        - le nombre total d'événements ;
        - les partitions existantes ;
        - le dernier offset de chaque partition.
        """

        self._print_section("ÉTAT DU BROKER")

        total_events = broker.size()
        partitions = broker.get_partitions()

        print(f"Nombre total d'événements dans le broker : {total_events}")

        if not partitions:
            print("Aucune partition disponible.")
            return

        print("\nPartitions :")
        for partition in partitions:
            latest_offset = broker.get_latest_offset(partition)
            partition_size = broker.size(partition)

            print(
                f"  Partition {partition} | "
                f"événements : {partition_size} | "
                f"prochain offset : {latest_offset}"
            )

    def show_consumer_a_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Affiche les métriques du Consumer A.

        Consumer A analyse :
        - les événements par ville ;
        - les événements par statut ;
        - les statistiques ville -> statut ;
        - les offsets.
        """

        self._print_section("CONSUMER A — ANALYSE VILLE / STATUT")

        events_by_city = metrics.get("events_by_city", {})
        events_by_status = metrics.get("events_by_status", {})
        city_status_stats = metrics.get("city_status_stats", {})
        offsets = metrics.get("offsets", {})

        total_events = self._get_total_from_dict(events_by_city)

        print(f"Total des événements traités par Consumer A : {total_events}")

        top_city = self._get_top_item(events_by_city)
        top_status = self._get_top_item(events_by_status)

        if top_city is not None:
            print(f"Ville la plus active : {top_city[0]} avec {top_city[1]} événements")

        if top_status is not None:
            print(f"Statut le plus fréquent : {top_status[0]} avec {top_status[1]} événements")

        print("\nÉvénements par ville :")
        self._print_dict(events_by_city, "Aucun événement par ville.")

        print("\nÉvénements par statut :")
        self._print_dict(events_by_status, "Aucun événement par statut.")

        print("\nDétail ville -> statut :")
        self._print_nested_dict(city_status_stats)

        print("\nOffsets du Consumer A :")
        self._print_dict(offsets, "Aucun offset sauvegardé.")

    def show_consumer_b_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Affiche les métriques du Consumer B.

        Consumer B analyse :
        - les événements par livreur ;
        - les événements par zone ;
        - les statistiques livreur -> zone ;
        - les commandes échouées ;
        - les offsets.
        """

        self._print_section("CONSUMER B — ANALYSE LIVREUR / ZONE")

        events_by_courier = metrics.get("events_by_courier", {})
        events_by_zone = metrics.get("events_by_zone", {})
        courier_zone_stats = metrics.get("courier_zone_stats", {})
        failed_orders = metrics.get("failed_orders", [])
        offsets = metrics.get("offsets", {})

        total_events = self._get_total_from_dict(events_by_courier)

        print(f"Total des événements traités par Consumer B : {total_events}")

        top_courier = self._get_top_item(events_by_courier)
        top_zone = self._get_top_item(events_by_zone)

        if top_courier is not None:
            print(
                f"Livreur le plus actif : {top_courier[0]} "
                f"avec {top_courier[1]} événements"
            )

        if top_zone is not None:
            print(f"Zone la plus active : {top_zone[0]} avec {top_zone[1]} événements")

        print("\nÉvénements par livreur :")
        self._print_dict(events_by_courier, "Aucun événement par livreur.")

        print("\nÉvénements par zone :")
        self._print_dict(events_by_zone, "Aucun événement par zone.")

        print("\nDétail livreur -> zone :")
        self._print_nested_dict(courier_zone_stats)

        print("\nCommandes échouées :")
        if not failed_orders:
            print("Aucune commande échouée.")
        else:
            for event in failed_orders:
                print(
                    f"  Order {event['order_id']} | "
                    f"Ville {event['city']} | "
                    f"Zone {event['zone']} | "
                    f"Livreur {event['courier_id']} | "
                    f"Statut {event['status']}"
                )

        print("\nOffsets du Consumer B :")
        self._print_dict(offsets, "Aucun offset sauvegardé.")

    def show_global_summary(
        self,
        consumer_a_metrics: Dict[str, Any],
        consumer_b_metrics: Dict[str, Any]
    ) -> None:
        """
        Affiche un résumé global du système.
        """

        self._print_section("RÉSUMÉ GLOBAL")

        events_by_city = consumer_a_metrics.get("events_by_city", {})
        events_by_status = consumer_a_metrics.get("events_by_status", {})
        failed_orders = consumer_b_metrics.get("failed_orders", [])

        total_events = self._get_total_from_dict(events_by_city)
        delivered_count = events_by_status.get("delivered", 0)
        failed_count = events_by_status.get("failed", 0)
        created_count = events_by_status.get("created", 0)

        print(f"Total des événements traités : {total_events}")
        print(f"Commandes créées : {created_count}")
        print(f"Commandes livrées : {delivered_count}")
        print(f"Commandes échouées : {failed_count}")
        print(f"Nombre d'échecs détectés par Consumer B : {len(failed_orders)}")

        top_city = self._get_top_item(events_by_city)

        if top_city is not None:
            print(f"Ville la plus active : {top_city[0]}")

        if total_events > 0:
            failure_rate = (failed_count / total_events) * 100
            print(f"Taux d'échec approximatif : {failure_rate:.2f}%")
        else:
            print("Taux d'échec approximatif : 0.00%")

    def render(
        self,
        broker: Any,
        consumer_a_metrics: Dict[str, Any],
        consumer_b_metrics: Dict[str, Any]
    ) -> None:
        """
        Affiche le dashboard complet.

        Cette méthode sera appelée dans main.py.
        """

        self.show_header()
        self.show_broker_state(broker)
        self.show_consumer_a_metrics(consumer_a_metrics)
        self.show_consumer_b_metrics(consumer_b_metrics)
        self.show_global_summary(consumer_a_metrics, consumer_b_metrics)

        print()
        self._print_separator()
        print("FIN DU DASHBOARD")
        self._print_separator()