import argparse
import json
from client import RpcClient


def main():
    parser = argparse.ArgumentParser(description="Client RPC Data Service")
    parser.add_argument("method", choices=["health.ping", "ingest.batch", "stats.daily_summary"])
    parser.add_argument("--endpoint", default="http://127.0.0.1:8080/rpc")
    args = parser.parse_args()

    client = RpcClient(args.endpoint)

    if args.method == "health.ping":
        response = client.call("health.ping", {})
    elif args.method == "ingest.batch":
        response = client.call(
            "ingest.batch",
            {
                "batch_id": "batch-001",
                "readings": [
                    {"sensor_id": "S01", "ts": "2026-03-09T10:00:00", "value": 23.5},
                    {"sensor_id": "S02", "ts": "2026-03-09T10:00:00", "value": 18.2},
                    {"sensor_id": "", "ts": "2026-03-09T10:00:00", "value": 99.0}
                ],
            },
        )
    else:
        response = client.call(
            "stats.daily_summary",
            {"date": "2026-03-09"},
        )

    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()