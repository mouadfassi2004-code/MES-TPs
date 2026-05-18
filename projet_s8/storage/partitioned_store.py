import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from contracts.event import Event


class PartitionedStore:
    """
    PartitionedStore représente le stockage partitionné du projet.

    Son rôle est de sauvegarder les événements traités dans des dossiers
    organisés selon une clé de partition.

    Par défaut, on partitionne par ville.

    Exemple :
    data/
    ├── city=Fes/
    │   └── events.jsonl
    ├── city=Casablanca/
    │   └── events.jsonl
    └── city=Rabat/
        └── events.jsonl

    Le format utilisé est JSON Lines :
    - chaque ligne du fichier contient un événement au format JSON ;
    - c'est pratique pour ajouter des événements sans réécrire tout le fichier.
    """

    def __init__(
        self,
        base_dir: str = "data",
        partition_key: str = "city",
        file_name: str = "events.jsonl"
    ) -> None:
        """
        Initialise le stockage partitionné.

        base_dir :
            Dossier principal où les données seront stockées.

        partition_key :
            Champ utilisé pour créer les partitions.
            Par défaut : city.

        file_name :
            Nom du fichier dans chaque partition.
        """

        self.base_dir = Path(base_dir)
        self.partition_key = partition_key
        self.file_name = file_name

        # Création du dossier data s'il n'existe pas.
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _event_to_dict(self, event: Any) -> Dict[str, Any]:
        """
        Convertit un événement en dictionnaire.

        Le stockage accepte :
        - un objet Event ;
        - ou directement un dictionnaire.
        """

        if isinstance(event, Event):
            event.validate()
            return event.to_dict()

        if isinstance(event, dict):
            event_obj = Event.from_dict(event)
            return event_obj.to_dict()

        raise TypeError("Le stockage accepte seulement un Event ou un dictionnaire.")

    def _get_partition_value(self, event_data: Dict[str, Any]) -> str:
        """
        Récupère la valeur de partition.

        Exemple :
        si partition_key = "city"
        et event_data["city"] = "Fes",
        alors la valeur de partition est "Fes".
        """

        if self.partition_key not in event_data:
            raise ValueError(
                f"La clé de partition '{self.partition_key}' est absente de l'événement."
            )

        partition_value = event_data[self.partition_key]

        if not partition_value:
            raise ValueError("La valeur de partition ne peut pas être vide.")

        return str(partition_value)

    def _get_partition_dir(self, partition_value: str) -> Path:
        """
        Retourne le chemin du dossier de partition.

        Exemple :
        partition_key = "city"
        partition_value = "Fes"

        chemin :
        data/city=Fes
        """

        return self.base_dir / f"{self.partition_key}={partition_value}"

    def _get_partition_file(self, partition_value: str) -> Path:
        """
        Retourne le chemin du fichier events.jsonl d'une partition.
        """

        partition_dir = self._get_partition_dir(partition_value)
        return partition_dir / self.file_name

    def write_event(self, event: Any) -> Dict[str, Any]:
        """
        Sauvegarde un événement dans la bonne partition.

        Étapes :
        1. Convertir l'événement en dictionnaire.
        2. Trouver la valeur de partition.
        3. Créer le dossier de partition.
        4. Ajouter l'événement dans events.jsonl.
        5. Retourner les informations d'écriture.
        """

        event_data = self._event_to_dict(event)
        partition_value = self._get_partition_value(event_data)

        partition_dir = self._get_partition_dir(partition_value)
        partition_dir.mkdir(parents=True, exist_ok=True)

        partition_file = self._get_partition_file(partition_value)

        with partition_file.open("a", encoding="utf-8") as file:
            json_line = json.dumps(event_data, ensure_ascii=False)
            file.write(json_line + "\n")

        return {
            "partition": partition_value,
            "file": str(partition_file),
            "event_id": event_data["event_id"],
            "event_type": event_data["event_type"],
            "order_id": event_data["order_id"]
        }

    def write_events(self, events: List[Any]) -> List[Dict[str, Any]]:
        """
        Sauvegarde plusieurs événements.

        Cette méthode appelle write_event pour chaque événement.
        """

        results = []

        for event in events:
            result = self.write_event(event)
            results.append(result)

        return results

    def read_partition(self, partition_value: str) -> List[Dict[str, Any]]:
        """
        Lit tous les événements d'une partition.

        Exemple :
        read_partition("Fes")
        lit le fichier :
        data/city=Fes/events.jsonl
        """

        partition_file = self._get_partition_file(partition_value)

        if not partition_file.exists():
            return []

        events = []

        with partition_file.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line:
                    events.append(json.loads(line))

        return events

    def read_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Lit toutes les partitions disponibles.

        Retourne un dictionnaire :
        {
            "Fes": [...],
            "Casablanca": [...]
        }
        """

        result: Dict[str, List[Dict[str, Any]]] = {}

        if not self.base_dir.exists():
            return result

        prefix = f"{self.partition_key}="

        for partition_dir in self.base_dir.iterdir():
            if partition_dir.is_dir() and partition_dir.name.startswith(prefix):
                partition_value = partition_dir.name.replace(prefix, "", 1)
                result[partition_value] = self.read_partition(partition_value)

        return result

    def get_partitions(self) -> List[str]:
        """
        Retourne la liste des partitions présentes dans le stockage.

        Exemple :
        ["Fes", "Casablanca", "Rabat"]
        """

        if not self.base_dir.exists():
            return []

        partitions = []
        prefix = f"{self.partition_key}="

        for partition_dir in self.base_dir.iterdir():
            if partition_dir.is_dir() and partition_dir.name.startswith(prefix):
                partition_value = partition_dir.name.replace(prefix, "", 1)
                partitions.append(partition_value)

        return partitions

    def count_events(self, partition_value: Optional[str] = None) -> int:
        """
        Compte le nombre d'événements stockés.

        Si partition_value est donné :
        on compte seulement cette partition.

        Sinon :
        on compte toutes les partitions.
        """

        if partition_value is not None:
            return len(self.read_partition(partition_value))

        total = 0

        for partition in self.get_partitions():
            total += len(self.read_partition(partition))

        return total

    def clear(self) -> None:
        """
        Supprime toutes les données stockées dans le dossier data.

        Cette méthode est utile pour recommencer un test proprement.
        """

        if not self.base_dir.exists():
            return

        for partition_dir in self.base_dir.iterdir():
            if partition_dir.is_dir():
                for file in partition_dir.iterdir():
                    if file.is_file():
                        file.unlink()

                partition_dir.rmdir()

    def print_state(self) -> None:
        """
        Affiche l'état du stockage partitionné.

        Cette méthode est utile pendant les tests et la présentation.
        """

        print("\n========== STOCKAGE PARTITIONNÉ ==========")

        partitions = self.get_partitions()

        if not partitions:
            print("Aucune donnée stockée.")
            print("==========================================\n")
            return

        total_events = self.count_events()
        print(f"Nombre total d'événements stockés : {total_events}")

        for partition in partitions:
            events_count = self.count_events(partition)
            partition_file = self._get_partition_file(partition)

            print(
                f"Partition {partition} | "
                f"événements : {events_count} | "
                f"fichier : {partition_file}"
            )

        print("==========================================\n")