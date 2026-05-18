import json
from pathlib import Path
from typing import Dict, Any, Optional

from contracts.event import Event


class CityStatusConsumer:
    """
    Consumer A : analyse les événements par ville et par statut.

    Son rôle est de :
    - lire les événements depuis le broker ;
    - reprendre la lecture à partir du dernier offset sauvegardé ;
    - compter les événements par ville ;
    - compter les événements par statut ;
    - sauvegarder les offsets après traitement.

    Exemple :
    Fes -> created: 3, delivered: 2, failed: 1
    """

    def __init__(
        self,
        name: str = "consumer_a",
        offsets_file: str = "offsets/offsets.json",
        storage: Optional[Any] = None
    ) -> None:
        """
        Initialise le consumer.

        name :
            Nom du consumer. Il sera utilisé dans le fichier offsets.json.

        offsets_file :
            Chemin du fichier qui sauvegarde la progression du consumer.

        storage :
            Objet de stockage partitionné.
            Pour l'instant, il peut être None.
            Plus tard, on lui passera PartitionedStore.
        """

        self.name = name
        self.offsets_file = Path(offsets_file)
        self.storage = storage

        # Statistiques par ville.
        # Exemple :
        # {
        #   "Fes": 5,
        #   "Rabat": 3
        # }
        self.events_by_city: Dict[str, int] = {}

        # Statistiques par statut.
        # Exemple :
        # {
        #   "created": 10,
        #   "delivered": 4,
        #   "failed": 2
        # }
        self.events_by_status: Dict[str, int] = {}

        # Statistiques détaillées ville -> statut.
        # Exemple :
        # {
        #   "Fes": {
        #       "created": 3,
        #       "delivered": 2
        #   }
        # }
        self.city_status_stats: Dict[str, Dict[str, int]] = {}

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
        Lit tout le contenu du fichier offsets.json.

        Le fichier peut contenir les offsets de plusieurs consumers.
        Exemple :
        {
            "consumer_a": {
                "Fes": 3,
                "Rabat": 2
            },
            "consumer_b": {
                "Fes": 3,
                "Rabat": 2
            }
        }
        """

        self._ensure_offsets_file_exists()

        try:
            content = self.offsets_file.read_text(encoding="utf-8").strip()

            if not content:
                return {}

            return json.loads(content)

        except json.JSONDecodeError:
            # Si le fichier est corrompu, on repart avec un dictionnaire vide.
            return {}

    def _write_all_offsets(self, all_offsets: Dict[str, Any]) -> None:
        """
        Écrit tous les offsets dans offsets.json.
        """

        self._ensure_offsets_file_exists()

        self.offsets_file.write_text(
            json.dumps(all_offsets, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def _load_offsets(self) -> Dict[str, int]:
        """
        Charge les offsets du consumer courant.

        Si le consumer n'a jamais travaillé avant,
        il commence avec un dictionnaire vide.
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
        Traite un seul événement.

        Étapes :
        1. Transformer le dictionnaire en objet Event.
        2. Valider l'événement.
        3. Mettre à jour les statistiques.
        4. Sauvegarder l'événement dans le stockage si disponible.
        """

        event = Event.from_dict(event_data)

        city = event.city
        status = event.status

        # Compter les événements par ville.
        self.events_by_city[city] = self.events_by_city.get(city, 0) + 1

        # Compter les événements par statut.
        self.events_by_status[status] = self.events_by_status.get(status, 0) + 1

        # Compter les événements par ville et par statut.
        if city not in self.city_status_stats:
            self.city_status_stats[city] = {}

        self.city_status_stats[city][status] = (
            self.city_status_stats[city].get(status, 0) + 1
        )

        # Plus tard, quand on aura codé storage/partitioned_store.py,
        # cette partie permettra de sauvegarder les événements sur disque.
        if self.storage is not None:
            self.storage.write_event(event.to_dict())

    def poll(self, broker: Any, max_events_per_partition: Optional[int] = None) -> int:
        """
        Lit les nouveaux événements depuis le broker.

        poll signifie : vérifier s'il y a de nouveaux messages.

        Le consumer lit chaque partition à partir de son dernier offset connu.
        Après chaque événement traité, il avance son offset.
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

                # On sauvegarde le prochain offset à lire.
                # Si on vient de traiter l'offset 4,
                # la prochaine lecture commencera à 5.
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
            "events_by_city": self.events_by_city,
            "events_by_status": self.events_by_status,
            "city_status_stats": self.city_status_stats,
            "offsets": self.offsets
        }

    def print_metrics(self) -> None:
        """
        Affiche les statistiques du consumer.
        """

        print("\n========== CONSUMER A : VILLE / STATUT ==========")

        print("\nÉvénements par ville :")
        if not self.events_by_city:
            print("Aucun événement traité.")
        else:
            for city, count in self.events_by_city.items():
                print(f"  {city} : {count}")

        print("\nÉvénements par statut :")
        if not self.events_by_status:
            print("Aucun événement traité.")
        else:
            for status, count in self.events_by_status.items():
                print(f"  {status} : {count}")

        print("\nDétail ville -> statut :")
        if not self.city_status_stats:
            print("Aucun détail disponible.")
        else:
            for city, stats in self.city_status_stats.items():
                print(f"  {city} :")
                for status, count in stats.items():
                    print(f"    {status} : {count}")

        print("\nOffsets sauvegardés :")
        if not self.offsets:
            print("Aucun offset sauvegardé.")
        else:
            for partition, offset in self.offsets.items():
                print(f"  {partition} -> prochain offset : {offset}")

        print("=================================================\n")