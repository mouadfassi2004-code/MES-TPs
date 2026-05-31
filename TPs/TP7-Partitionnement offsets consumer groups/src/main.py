from src.events import generate_events
from src.broker import MiniBroker
from src.offsets import OffsetStore
from src.storage import PartitionedStorage
from src.consumers import ConsumerGroup, ConsumerRunner
from src.metrics import compute_backlog, compute_lag


def main():
    num_partitions = 4
    group_name = "agri-stats"

    # 1) Génération des événements
    events = generate_events()

    # 2) Création du broker
    broker = MiniBroker(num_partitions=num_partitions)

    # 3) Publication dans les partitions
    print("=== Publication des événements ===")
    for event in events:
        p = broker.publish(event)
        print(f"{event.event_id} -> partition {p} (key={event.partition_key})")

    # 4) Affichage distribution
    print("\n=== Distribution par partition ===")
    sizes = broker.all_partition_sizes()
    for p, size in sizes.items():
        print(f"Partition {p}: {size} événement(s)")

    # 5) Consumer group
    group = ConsumerGroup(
        group_name=group_name,
        consumers=["consumer-A", "consumer-B"],
        num_partitions=num_partitions,
    )
    group.show_assignment()

    # 6) Offset store + storage
    store = OffsetStore("state/offsets.json")
    storage = PartitionedStorage("outputs")

    # 7) Run consumers
    runner = ConsumerRunner(broker, store, storage, group)

    print("\n=== Premier run ===")
    runner.run_once()

    print("\n=== Offsets après run ===")
    print(store.dump())

    print("\n=== Lag après run ===")
    lag = compute_lag(broker, store, group_name)
    for p, value in lag.items():
        print(f"Partition {p}: lag={value}")

    # 8) Simulation de rebalance
    print("\n=== Rebalance : ajout d'un 3e consumer ===")
    group.rebalance(["consumer-A", "consumer-B", "consumer-C"])
    group.show_assignment()

    print("\n=== Reprise après rebalance ===")
    runner.run_once()

    print("\n=== Offsets finaux ===")
    print(store.dump())


if __name__ == "__main__":
    main()