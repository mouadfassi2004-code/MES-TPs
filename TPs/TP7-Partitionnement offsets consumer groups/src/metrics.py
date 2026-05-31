from typing import Dict
from src.broker import MiniBroker
from src.offsets import OffsetStore


def compute_lag(broker: MiniBroker, store: OffsetStore, group: str) -> Dict[int, int]:
    result = {}
    for p in range(broker.num_partitions):
        total = broker.partition_size(p)
        consumed = store.get(group, p)
        result[p] = total - consumed
    return result


def compute_backlog(broker: MiniBroker) -> Dict[int, int]:
    return broker.all_partition_sizes()