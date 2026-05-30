# Rapport TP4 - Mini RPC Data Service - Ingestion + Stats

## Objectif

L'objectif de ce TP est de construire un mini service RPC dans un contexte Big Data. Le service simule l'ingestion de données capteurs IoT et le calcul de statistiques à distance.

Contrairement au TP3 basé sur les sockets TCP, ce TP introduit une abstraction plus haut niveau : le RPC. Le client n'envoie plus seulement un message brut, il appelle une méthode nommée avec des paramètres.

## Architecture

Le projet est organisé autour des composants suivants :

- `rpc_protocol.py` : construit et valide les messages RPC.
- `router.py` : associe les noms de méthodes aux fonctions Python.
- `server.py` : expose le serveur HTTP-RPC avec ThreadingHTTPServer.
- `client.py` : envoie les appels RPC avec timeout et retries.
- `services.py` : contient la logique métier d'ingestion et de statistiques.
- `observability.py` : gère les logs structurés et les métriques.
- `test_scenario.py` : exécute un scénario complet de test.

## Protocole RPC

Le protocole utilise des messages JSON avec les champs principaux :

- `rpc_version`
- `id`
- `method`
- `params`
- `sent_at`

La réponse contient soit un champ `result`, soit un champ `error`.

## Méthodes implémentées

### health.ping

Cette méthode permet de vérifier que le serveur est disponible.

### ingest.batch

Cette méthode reçoit un lot de mesures IoT. Chaque lecture contient :
- sensor_id
- ts
- value

Les lectures valides sont acceptées et enregistrées dans `outputs/ingested_data.csv`. Les lectures invalides sont rejetées.

### stats.daily_summary

Cette méthode calcule un résumé statistique pour une date donnée :
- count
- avg
- min
- max

## Robustesse

Le client RPC utilise un timeout et des retries avec backoff. Cela permet de gérer les erreurs temporaires de communication ou les indisponibilités du serveur.

Le serveur retourne des erreurs structurées lorsque :
- le JSON est invalide ;
- la requête RPC est mal formée ;
- la méthode demandée n'existe pas ;
- les paramètres sont invalides.

## Observabilité

Les logs client et serveur sont écrits dans le dossier `logs`. Les métriques d'exécution sont sauvegardées dans `outputs/run_report.json`.

Les logs contiennent notamment :
- rpc_id ;
- méthode appelée ;
- statut ;
- latence ;
- tentative côté client.

## Résultats

Le scénario de test vérifie :
1. la disponibilité du serveur avec `health.ping` ;
2. l'ingestion d'un batch avec données valides et invalides ;
3. l'idempotence avec un batch_id déjà traité ;
4. le calcul des statistiques quotidiennes ;
5. la réponse à une méthode inconnue.

Les résultats sont sauvegardés dans :
- `outputs/ingested_data.csv`
- `outputs/run_report.json`
- `outputs/test_scenario_result.json`
- `outputs/test_summary.txt`

## Conclusion

Ce TP m'a permis de comprendre l'intérêt du RPC dans les applications distribuées. Il montre comment exposer des méthodes distantes, router les appels, gérer les erreurs, assurer la robustesse côté client et suivre l'exécution grâce aux logs et métriques.
