from typing import Dict, List, Any, Optional
from threading import Lock

from contracts.event import Event


class MiniBroker:
    """
    MiniBroker simule un broker d'événements.

    Son rôle est de :
    - recevoir des événements ;
    - les ranger dans des partitions ;
    - attribuer un offset à chaque événement ;
    - permettre aux consumers de lire les événements à partir d'un offset précis.

    Dans un vrai système Big Data, ce rôle est souvent joué par Apache Kafka.
    Ici, on le simule avec des listes Python.
    """

    def __init__(self, partition_key: str = "city") -> None:
        """
        Initialise le broker.

        partition_key indique le champ utilisé pour choisir la partition.
        Dans notre projet, on utilise par défaut la ville.
        Exemple :
        - city = "Fes" va dans la partition "Fes"
        - city = "Casablanca" va dans la partition "Casablanca"
        """

        self.partition_key = partition_key

        # Dictionnaire qui contient les partitions.
        # Exemple :
        # {
        #   "Fes": [
        #       {"offset": 0, "event": {...}},
        #       {"offset": 1, "event": {...}}
        #   ],
        #   "Rabat": [
        #       {"offset": 0, "event": {...}}
        #   ]
        # }
        self.partitions: Dict[str, List[Dict[str, Any]]] = {}

        # Lock permet d'éviter les problèmes si plusieurs parties
        # publient ou lisent des événements en même temps.
        self.lock = Lock()

    def _event_to_dict(self, event: Any) -> Dict[str, Any]:
        """
        Convertit un événement en dictionnaire.

        Le broker accepte :
        - un objet Event ;
        - ou directement un dictionnaire.

        Cela rend le broker plus flexible.
        """

        if isinstance(event, Event):
            event.validate()
            return event.to_dict()

        if isinstance(event, dict):
            event_obj = Event.from_dict(event)
            return event_obj.to_dict()

        raise TypeError("Le broker accepte seulement un Event ou un dictionnaire.")

    def _get_partition_name(self, event_data: Dict[str, Any]) -> str:
        """
        Détermine le nom de la partition à partir de la clé de partition.

        Par défaut, la clé de partition est city.
        Donc si event_data['city'] = 'Fes',
        l'événement sera rangé dans la partition 'Fes'.
        """

        if self.partition_key not in event_data:
            raise ValueError(
                f"La clé de partition '{self.partition_key}' est absente de l'événement."
            )

        partition_value = event_data[self.partition_key]

        if not partition_value:
            raise ValueError("La valeur de la partition ne peut pas être vide.")

        return str(partition_value)

    def publish(self, event: Any) -> Dict[str, Any]:
        """
        Publie un événement dans le broker.

        Étapes :
        1. Convertir l'événement en dictionnaire.
        2. Trouver la bonne partition.
        3. Calculer l'offset.
        4. Ajouter l'événement dans la partition.
        5. Retourner les informations de publication.
        """

        event_data = self._event_to_dict(event)
        partition_name = self._get_partition_name(event_data)

        with self.lock:
            if partition_name not in self.partitions:
                self.partitions[partition_name] = []

            offset = len(self.partitions[partition_name])

            record = {
                "offset": offset,
                "event": event_data
            }

            self.partitions[partition_name].append(record)

        return {
            "partition": partition_name,
            "offset": offset,
            "event_id": event_data["event_id"],
            "event_type": event_data["event_type"]
        }

    def consume(
        self,
        partition: str,
        offset: int = 0,
        max_events: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Lit les événements d'une partition à partir d'un offset donné.

        Exemple :
        consume("Fes", offset=2)

        Cela signifie :
        lire les événements de la partition Fes à partir de l'offset 2.
        """

        if offset < 0:
            raise ValueError("L'offset ne peut pas être négatif.")

        with self.lock:
            if partition not in self.partitions:
                return []

            events = self.partitions[partition][offset:]

            if max_events is not None:
                events = events[:max_events]

            # On retourne une copie pour éviter qu'un consumer modifie
            # directement les données internes du broker.
            return [record.copy() for record in events]

    def consume_all(
        self,
        offsets: Optional[Dict[str, int]] = None,
        max_events_per_partition: Optional[int] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Lit les événements de toutes les partitions.

        offsets permet de préciser à partir de quel offset lire
        pour chaque partition.

        Exemple :
        offsets = {
            "Fes": 2,
            "Rabat": 0
        }
        """

        if offsets is None:
            offsets = {}

        result = {}

        with self.lock:
            partition_names = list(self.partitions.keys())

        for partition in partition_names:
            start_offset = offsets.get(partition, 0)

            result[partition] = self.consume(
                partition=partition,
                offset=start_offset,
                max_events=max_events_per_partition
            )

        return result

    def get_partitions(self) -> List[str]:
        """
        Retourne la liste des partitions existantes.
        """

        with self.lock:
            return list(self.partitions.keys())

    def get_latest_offset(self, partition: str) -> int:
        """
        Retourne le prochain offset disponible dans une partition.

        Si la partition contient 3 événements :
        offsets existants : 0, 1, 2
        prochain offset : 3

        Ce nombre correspond aussi au nombre total d'événements
        dans cette partition.
        """

        with self.lock:
            if partition not in self.partitions:
                return 0

            return len(self.partitions[partition])

    def size(self, partition: Optional[str] = None) -> int:
        """
        Retourne le nombre d'événements dans le broker.

        Si partition est précisée, on retourne la taille de cette partition.
        Sinon, on retourne le total de toutes les partitions.
        """

        with self.lock:
            if partition is not None:
                return len(self.partitions.get(partition, []))

            total = 0

            for events in self.partitions.values():
                total += len(events)

            return total

    def is_empty(self) -> bool:
        """
        Vérifie si le broker ne contient aucun événement.
        """

        return self.size() == 0

    def print_state(self) -> None:
        """
        Affiche l'état actuel du broker.

        Cette méthode est utile pour comprendre ce qui se passe
        pendant les tests ou pendant la présentation.
        """

        print("\n========== ÉTAT DU BROKER ==========")

        if self.is_empty():
            print("Le broker ne contient aucun événement.")
            print("====================================\n")
            return

        with self.lock:
            for partition, records in self.partitions.items():
                print(f"Partition : {partition}")
                print(f"Nombre d'événements : {len(records)}")

                for record in records:
                    event = record["event"]
                    print(
                        f"  Offset {record['offset']} | "
                        f"{event['event_type']} | "
                        f"Order {event['order_id']} | "
                        f"Status {event['status']}"
                    )

        print("====================================\n")