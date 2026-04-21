from typing import Dict, List
from src.partitioner import partition_of
from src.events import Event


class MiniBroker:
    def __init__(self, num_partitions: int):
        self.num_partitions = num_partitions
        self.partitions: Dict[int, List[Event]] = {i: [] for i in range(num_partitions)}

    def publish(self, event: Event) -> int:
        p = partition_of(event.partition_key, self.num_partitions)
        self.partitions[p].append(event)
        return p

    def get_partition_events(self, partition: int) -> List[Event]:
        return self.partitions[partition]

    def partition_size(self, partition: int) -> int:
        return len(self.partitions[partition])

    def all_partition_sizes(self) -> Dict[int, int]:
        return {p: len(events) for p, events in self.partitions.items()}