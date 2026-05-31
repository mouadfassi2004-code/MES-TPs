# Séance 4 - RPC Data Service

## Objectif

Ce projet implémente un mini service RPC pour l'ingestion de données IoT et le calcul de statistiques simples.

Le service repose sur un protocole JSON-RPC minimal avec les champs :
- rpc_version
- id
- method
- params
- sent_at
- result
- error

## Méthodes RPC disponibles

### health.ping

Vérifie que le serveur est actif.

Paramètres :

{}

Réponse attendue :

{"status": "ok"}

### ingest.batch

Ingère un lot de lectures capteurs.

Paramètres :

{
  "batch_id": "batch-001",
  "readings": [
    {"sensor_id": "S01", "ts": "2026-03-09T10:00:00", "value": 23.5}
  ]
}

Réponse attendue :

{
  "accepted": 1,
  "rejected": 0,
  "duplicate": false
}

### stats.daily_summary

Retourne un résumé statistique pour une date.

Paramètres :

{"date": "2026-03-09"}

Réponse attendue :

{
  "date": "2026-03-09",
  "count": 2,
  "avg": 20.85,
  "min": 18.2,
  "max": 23.5
}

## Lancer le serveur

Depuis le dossier seance4_rpc_data_service :

python .\src\server.py

## Lancer les tests

Dans un deuxième terminal :

python .\test_scenario.py

## Résultats

Les résultats sont visibles dans :
- outputs/ingested_data.csv
- outputs/run_report.json
- outputs/test_scenario_result.json
- logs/server.log
- logs/client.log
