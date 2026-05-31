# Séance 4 Partie 2 - RPC Data Service IoT

Ce dossier contient l'implémentation du service RPC IoT.

## Méthodes disponibles

- health.ping
- ingest.batch
- stats.daily_summary
- stats.top_sensors

## Lancement

Serveur :

python .\server.py

Client / scénario de test :

python .\test_scenario.py

## Fichiers principaux

- server.py : serveur RPC.
- client.py : client RPC.
- rpc_protocol.py : protocole JSON-RPC.
- router.py : routage des méthodes.
- services.py : logique métier.
- models.py : modèle de données.
- test_batch.json : données de test.
- test_scenario.py : scénario de test.
