# Rapport TP4.2 - Mini RPC Data Service IoT

## Objectif

L'objectif de ce TP est de réaliser un mini service RPC pour l'ingestion de données IoT et le calcul de statistiques. Le service permet à un client d'appeler des méthodes distantes à travers un protocole JSON sur HTTP.

## Architecture

Le projet contient :
- server.py : serveur RPC ;
- client.py : client RPC ;
- rpc_protocol.py : construction des requêtes/réponses ;
- router.py : routage des méthodes ;
- services.py : logique métier ;
- models.py : modèles de données ;
- test_scenario.py : scénario de test.

## Méthodes implémentées

Le service expose les méthodes suivantes :

- health.ping : vérifie que le serveur fonctionne ;
- ingest.batch : ingère un lot de lectures capteurs ;
- stats.daily_summary : calcule les statistiques journalières ;
- stats.top_sensors : retourne les capteurs les plus importants.

## Résultats

Le scénario de test vérifie l'appel au serveur, l'ingestion des données, le calcul des statistiques et la gestion des erreurs.

Les fichiers produits sont :
- outputs/ingested_data.csv ;
- outputs/test_summary.txt ;
- outputs/run_report.json ;
- logs/server.log ;
- logs/client.log.

## Conclusion

Ce TP m'a permis de comprendre le fonctionnement d'un service RPC simple avec ingestion, statistiques, validation, gestion d'erreurs et logs.
