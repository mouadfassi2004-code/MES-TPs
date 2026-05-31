import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from contracts.event import Event


class CourierZoneConsumer:
    """
    Consumer B : analyse les événements par livreur et par zone.

    Son rôle est de :
    - lire les événements depuis le broker ;
    - reprendre à partir du dernier offset sauvegardé ;
    - compter les événements par livreur ;
    - compter les événements par zone ;
    - détecter les commandes échouées ;
    - sauvegarder les offsets après traitement.
    """

    def __init__(
        self,
        name: str = "consumer_b",
        offsets_file: str = "offsets/offsets.json"
    ) -> None:
        """
        Initialise le consumer.

        name :
            Nom utilisé pour sauvegarder les offsets de ce consumer.

        offsets_file :
            Fichier qui stocke les offsets.
        """

        self.name = name
        self.offsets_file = Path(offsets_file)

        # Statistiques par livreur.
        # Exemple :
        # {
        #   "COURIER-001": 4,
        #   "COURIER-002": 2
        # }
        self.events_by_courier: Dict[str, int] = {}

        # Statistiques par zone.
        # Exemple :
        # {
        #   "Atlas": 3,
        #   "Maarif": 5
        # }
        self.events_by_zone: Dict[str, int] = {}

        # Liste des événements échoués.
        self.failed_orders: List[Dict[str, Any]] = []

        # Statistiques détaillées livreur -> zone.
        # Exemple :
        # {
        #   "COURIER-001": {
        #       "Atlas": 3,
        #       "Narjiss": 2
        #   }
        # }
        self.courier_zone_stats: Dict[str, Dict[str, int]] = {}

        # Chargement des offsets sauvegardés.
        self.offsets = self._load_offsets()

    def _ensure_offsets_file_exists(self) -> None:
        """
        Crée le dossier offsets et le fichier offsets.json s'ils n'existent pas.
        """

        self.offsets_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.offsets_file.exists():
            self.offsets_file.write_text("{}", encoding="utf-8")

    def _read_all_offsets(self) -> Dict[str, Any]:
        """
        Lit le fichier offsets.json.
        """

        self._ensure_offsets_file_exists()

        try:
            content = self.offsets_file.read_text(encoding="utf-8").strip()

            if not content:
                return {}

            return json.loads(content)

        except json.JSONDecodeError:
            return {}

    def _write_all_offsets(self, all_offsets: Dict[str, Any]) -> None:
        """
        Écrit les offsets dans offsets.json.
        """

        self._ensure_offsets_file_exists()

        self.offsets_file.write_text(
            json.dumps(all_offsets, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def _load_offsets(self) -> Dict[str, int]:
        """
        Charge les offsets du consumer courant.
        """

        all_offsets = self._read_all_offsets()
        consumer_offsets = all_offsets.get(self.name, {})

        return {
            str(partition): int(offset)
            for partition, offset in consumer_offsets.items()
        }

    def _save_offsets(self) -> None:
        """
        Sauvegarde les offsets du consumer courant.
        """

        all_offsets = self._read_all_offsets()
        all_offsets[self.name] = self.offsets
        self._write_all_offsets(all_offsets)

    def _process_event(self, event_data: Dict[str, Any]) -> None:
        """
        Traite un événement.

        Ce consumer se concentre sur :
        - le livreur ;
        - la zone ;
        - les commandes échouées.
        """

        event = Event.from_dict(event_data)

        courier_id = event.courier_id
        zone = event.zone

        # Compter les événements par livreur.
        self.events_by_courier[courier_id] = (
            self.events_by_courier.get(courier_id, 0) + 1
        )

        # Compter les événements par zone.
        self.events_by_zone[zone] = self.events_by_zone.get(zone, 0) + 1

        # Compter livreur -> zone.
        if courier_id not in self.courier_zone_stats:
            self.courier_zone_stats[courier_id] = {}

        self.courier_zone_stats[courier_id][zone] = (
            self.courier_zone_stats[courier_id].get(zone, 0) + 1
        )

        # Détection des commandes échouées.
        if event.status == "failed" or event.event_type == "order_failed":
            self.failed_orders.append(event.to_dict())

    def poll(self, broker: Any, max_events_per_partition: Optional[int] = None) -> int:
        """
        Lit les nouveaux événements depuis le broker.

        Le consumer utilise ses offsets pour ne pas relire les anciens messages.
        """

        total_processed = 0

        records_by_partition = broker.consume_all(
            offsets=self.offsets,
            max_events_per_partition=max_events_per_partition
        )

        for partition, records in records_by_partition.items():
            for record in records:
                event_data = record["event"]
                offset = record["offset"]

                self._process_event(event_data)

                # Si on traite l'offset 2,
                # le prochain offset à lire est 3.
                self.offsets[partition] = offset + 1

                total_processed += 1

        self._save_offsets()

        return total_processed

    def get_metrics(self) -> Dict[str, Any]:
        """
        Retourne les statistiques calculées par le consumer.
        """

        return {
            "consumer": self.name,
            "events_by_courier": self.events_by_courier,
            "events_by_zone": self.events_by_zone,
            "courier_zone_stats": self.courier_zone_stats,
            "failed_orders": self.failed_orders,
            "offsets": self.offsets
        }

    def print_metrics(self) -> None:
        """
        Affiche les statistiques du consumer.
        """

        print("\n========== CONSUMER B : LIVREUR / ZONE ==========")

        print("\nÉvénements par livreur :")
        if not self.events_by_courier:
            print("Aucun événement traité.")
        else:
            for courier_id, count in self.events_by_courier.items():
                print(f"  {courier_id} : {count}")

        print("\nÉvénements par zone :")
        if not self.events_by_zone:
            print("Aucun événement traité.")
        else:
            for zone, count in self.events_by_zone.items():
                print(f"  {zone} : {count}")

        print("\nDétail livreur -> zone :")
        if not self.courier_zone_stats:
            print("Aucun détail disponible.")
        else:
            for courier_id, stats in self.courier_zone_stats.items():
                print(f"  {courier_id} :")
                for zone, count in stats.items():
                    print(f"    {zone} : {count}")

        print("\nCommandes échouées :")
        if not self.failed_orders:
            print("Aucune commande échouée.")
        else:
            for event in self.failed_orders:
                print(
                    f"  Order {event['order_id']} | "
                    f"Ville {event['city']} | "
                    f"Zone {event['zone']} | "
                    f"Livreur {event['courier_id']}"
                )

        print("\nOffsets sauvegardés :")
        if not self.offsets:
            print("Aucun offset sauvegardé.")
        else:
            for partition, offset in self.offsets.items():
                print(f"  {partition} -> prochain offset : {offset}")

        print("=================================================\n")