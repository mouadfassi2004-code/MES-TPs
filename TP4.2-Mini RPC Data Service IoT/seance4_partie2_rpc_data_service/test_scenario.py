import json

from client import RpcClient


URL = "http://127.0.0.1:8080"


def main():
    client = RpcClient(URL, default_timeout=5.0, max_retries=2)

    print("=" * 50)
    print("TEST 1 : health.ping")
    r = client.call("health.ping")
    assert r.get("error") is None, f"Erreur inattendue : {r}"
    assert r["result"]["status"] == "ok"
    print("  ✅ health.ping OK\n")

    print("=" * 50)
    print("TEST 2 : ingest.batch")
    with open("test_batch.json", "r", encoding="utf-8") as f:
        test_readings = json.load(f)

    r = client.call("ingest.batch", {
        "batch_id": "batch-001",
        "readings": test_readings
    })
    assert r.get("error") is None, f"Erreur inattendue : {r}"
    result = r["result"]
    assert result["accepted"] == 6, f"Expected 6 accepted, got {result['accepted']}"
    assert result["rejected"] == 4, f"Expected 4 rejected, got {result['rejected']}"
    print(f"  ✅ ingest.batch OK : {result['accepted']} accepted, {result['rejected']} rejected\n")

    print("=" * 50)
    print("TEST 3 : stats.daily_summary")
    r = client.call("stats.daily_summary", {"date": "2026-03-09"})
    assert r.get("error") is None
    result = r["result"]
    assert result["count"] == 6
    assert result["min"] == -5.1
    assert result["max"] == 25.3
    print(f"  ✅ daily_summary OK : count={result['count']}, avg={result['avg']}\n")

    print("=" * 50)
    print("TEST 4 : stats.top_sensors")
    r = client.call("stats.top_sensors", {"n": 3})
    assert r.get("error") is None
    result = r["result"]
    assert "sensors" in result
    assert len(result["sensors"]) >= 1
    print(f"  ✅ top_sensors OK : {result['sensors']}\n")

    print("=" * 50)
    print("TEST 5 : méthode inconnue")
    r = client.call("unknown.method")
    assert r["error"]["code"] == -32601
    print(f"  ✅ Correctement rejeté (code {r['error']['code']})\n")

    print("🎉 TOUS LES TESTS SONT PASSÉS !")


if __name__ == "__main__":
    main()