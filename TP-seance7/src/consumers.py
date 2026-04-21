from typing import Dict, List, Set
from src.broker import MiniBroker
from src.offsets import OffsetStore
from src.storage import PartitionedStorage


class ConsumerGroup:
    def __init__(self, group_name: str, consumers: List[str], num_partitions: int):
        self.group_name = group_name
        self.consumers = consumers
        self.num_partitions = num_partitions
        self.assignment = self._assign_round_robin()

    def _assign_round_robin(self) -> Dict[str, List[int]]:
        assignment = {c: [] for c in self.consumers}
        for partition in range(self.num_partitions):
            consumer = self.consumers[partition % len(self.consumers)]
            assignment[consumer].append(partition)
        return assignment

    def rebalance(self, consumers: List[str]) -> None:
        self.consumers = consumers
        self.assignment = self._assign_round_robin()

    def show_assignment(self) -> None:
        print(f"\nAssignation du consumer group '{self.group_name}' :")
        for consumer, partitions in self.assignment.items():
            print(f"  {consumer} -> partitions {partitions}")


class ConsumerRunner:
    def __init__(
        self,
        broker: MiniBroker,
        store: OffsetStore,
        storage: PartitionedStorage,
        group: ConsumerGroup,
    ):
        self.broker = broker
        self.store = store
        self.storage = storage
        self.group = group
        self.processed_ids: Set[str] = set()

    def process_partition(self, consumer_name: str, partition: int) -> None:
        events = self.broker.get_partition_events(partition)
        start_offset = self.store.get(self.group.group_name, partition)

        print(f"\n[{consumer_name}] lecture partition {partition} depuis offset {start_offset}")

        for offset in range(start_offset, len(events)):
            event = events[offset]

            # Idempotence simple sur event_id
            if event.event_id in self.processed_ids:
                print(f"[{consumer_name}] doublon ignoré : {event.event_id}")
                self.store.commit(self.group.group_name, partition, offset + 1)
                continue

            # Traitement
            print(
                f"[{consumer_name}] traite {event.event_id} "
                f"(sensor={event.sensor_id}, site={event.site_id})"
            )

            self.storage.write_event(event, partition)
            self.processed_ids.add(event.event_id)

            # Commit APRÈS traitement
            self.store.commit(self.group.group_name, partition, offset + 1)

    def run_once(self) -> None:
        for consumer_name, partitions in self.group.assignment.items():
            for partition in partitions:
                self.process_partition(consumer_name, partition)