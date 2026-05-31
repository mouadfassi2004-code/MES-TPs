from ingestion.event_producer import produce_demo_events
from processing.stream.stream_processor import StreamProcessor
from orchestration.scheduler import Scheduler

def main() -> None:
    print("\n=== 1. Production et ingestion des événements ===")
    produce_demo_events()

    print("\n=== 2. Traitement stream temps réel ===")
    stream = StreamProcessor()
    stream.run_once()

    print("\n=== 3. Traitement batch + orchestration ===")
    scheduler = Scheduler()
    result = scheduler.run()
    print(result)

    print("\nProjet exécuté avec succès.")
    print("Regarde les dossiers storage/bronze, storage/silver et storage/gold.")

if __name__ == "__main__":
    main()