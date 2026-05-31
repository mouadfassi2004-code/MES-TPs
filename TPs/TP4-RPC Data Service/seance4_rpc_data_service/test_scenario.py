import json
import sys
from pathlib import Path
from datetime import datetime

# Permet d'importer les modules du dossier src
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from client import RpcClient


ENDPOINT = "http://127.0.0.1:8080/rpc"


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    client = RpcClient(endpoint=ENDPOINT, timeout=3.0, max_retries=3)

    results = {
        "executed_at": datetime.now().isoformat(),
        "endpoint": ENDPOINT,
        "tests": {}
    }

    print("1. Test health.ping")
    ping_response = client.call("health.ping", {})
    results["tests"]["health_ping"] = ping_response
    print(json.dumps(ping_response, ensure_ascii=False, indent=2))

    print("\n2. Test ingest.batch")
    batch = [
        {"sensor_id": "S01", "ts": "2026-03-09T10:00:00", "value": 23.5},
        {"sensor_id": "S02", "ts": "2026-03-09T10:00:00", "value": 18.2},
        {"sensor_id": "S03", "ts": "2026-03-09T10:05:00", "value": -5.1},
        {"sensor_id": "", "ts": "2026-03-09T10:10:00", "value": 22.0},
        {"sensor_id": "S04", "ts": "", "value": 30.0},
        {"sensor_id": "S05", "ts": "date-invalide", "value": 19.0}
    ]

    ingest_response = client.call(
        "ingest.batch",
        {
            "batch_id": "batch-test-001",
            "readings": batch
        }
    )
    results["tests"]["ingest_batch"] = ingest_response
    print(json.dumps(ingest_response, ensure_ascii=False, indent=2))

    print("\n3. Test idempotence avec le même batch_id")
    duplicate_response = client.call(
        "ingest.batch",
        {
            "batch_id": "batch-test-001",
            "readings": batch
        }
    )
    results["tests"]["duplicate_batch"] = duplicate_response
    print(json.dumps(duplicate_response, ensure_ascii=False, indent=2))

    print("\n4. Test stats.daily_summary")
    stats_response = client.call(
        "stats.daily_summary",
        {
            "date": "2026-03-09"
        }
    )
    results["tests"]["daily_summary"] = stats_response
    print(json.dumps(stats_response, ensure_ascii=False, indent=2))

    print("\n5. Test méthode inconnue")
    unknown_response = client.call("unknown.method", {})
    results["tests"]["unknown_method"] = unknown_response
    print(json.dumps(unknown_response, ensure_ascii=False, indent=2))

    output_path = BASE_DIR / "outputs" / "test_scenario_result.json"
    save_json(output_path, results)

    print("\nScénario terminé.")
    print(f"Résultats sauvegardés dans : {output_path}")


if __name__ == "__main__":
    main()
