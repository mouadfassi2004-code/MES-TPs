# TP4.2 - Mini RPC Data Service IoT

## Objectif

Ce TP consiste à implémenter un mini service RPC en Python pour gérer l'ingestion de données IoT et produire des statistiques simples.

Le service expose plusieurs méthodes RPC :
- health.ping
- ingest.batch
- stats.daily_summary
- stats.top_sensors

## Technologies utilisées

- Python 3
- http.server
- ThreadingHTTPServer
- urllib.request
- json
- logging
- csv

## Structure du projet

seance4_partie2_rpc_data_service/
├── client.py
├── models.py
├── router.py
├── rpc_protocol.py
├── server.py
├── services.py
├── test_batch.json
├── test_scenario.py
├── requirements.txt
├── rapport_tp4_2.md
├── logs/
└── outputs/

## Exécution

Ouvrir deux terminaux.

Terminal 1 :

python .\server.py

Terminal 2 :

python .\test_scenario.py

## Résultats

Les résultats sont disponibles dans :
- outputs/ingested_data.csv
- outputs/test_summary.txt
- outputs/run_report.json
- logs/server.log
- logs/client.log

## Conclusion

Ce TP m'a permis de comprendre le fonctionnement d'un service RPC appliqué aux données IoT, avec ingestion, validation, statistiques, idempotence et observabilité.
