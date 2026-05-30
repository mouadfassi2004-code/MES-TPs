# TP4 - Mini RPC Data Service - Ingestion + Stats

## Objectif

Ce TP consiste à construire un mini service RPC en Python pour simuler l'ingestion de données capteurs IoT et le calcul de statistiques.

Le service expose plusieurs méthodes RPC :
- health.ping
- ingest.batch
- stats.daily_summary

Le TP met en pratique :
- un protocole RPC minimal inspiré de JSON-RPC ;
- un serveur HTTP multi-threadé ;
- un routeur de méthodes ;
- un client RPC avec timeout et retries ;
- des logs structurés ;
- des métriques d'exécution.

## Technologies utilisées

- Python 3
- http.server
- ThreadingHTTPServer
- urllib.request
- json
- logging
- threading
- csv

## Structure du projet

seance4_rpc_data_service/
├── logs/
│   ├── client.log
│   └── server.log
├── outputs/
│   ├── ingested_data.csv
│   ├── run_report.json
│   └── test_summary.txt
├── src/
│   ├── cli.py
│   ├── client.py
│   ├── models.py
│   ├── observability.py
│   ├── router.py
│   ├── rpc_protocol.py
│   ├── server.py
│   └── services.py
├── test_scenario.py
├── requirements.txt
├── rapport_tp4.md
└── README.md

## Installation

Aucune dépendance externe n'est nécessaire.

Vérifier Python :

python --version

## Exécution

Ouvrir deux terminaux.

Terminal 1 - Lancer le serveur :

cd "C:\Users\Utilisateur\Desktop\S6-25.26\Applications reparties\MES-TPs\TP4-Mini RPC Data Service (Ingestion + Stats)\seance4_rpc_data_service"
python .\src\server.py

Terminal 2 - Lancer le scénario de test :

cd "C:\Users\Utilisateur\Desktop\S6-25.26\Applications reparties\MES-TPs\TP4-Mini RPC Data Service (Ingestion + Stats)\seance4_rpc_data_service"
python .\test_scenario.py

## Résultats attendus

Le test exécute :
- un appel health.ping ;
- une ingestion valide avec ingest.batch ;
- un second appel avec le même batch_id pour vérifier l'idempotence ;
- une demande de statistiques avec stats.daily_summary ;
- un appel vers une méthode inconnue.

Les fichiers générés ou utilisés sont :
- logs/server.log
- logs/client.log
- outputs/ingested_data.csv
- outputs/run_report.json
- outputs/test_scenario_result.json
- outputs/test_summary.txt

## Conclusion

Ce TP m'a permis de comprendre comment passer d'une communication socket simple à une abstraction RPC plus structurée, avec méthodes nommées, routage, gestion d'erreurs, retries, logs et métriques.
