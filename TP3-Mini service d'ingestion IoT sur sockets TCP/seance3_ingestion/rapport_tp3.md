# Rapport TP3 - Mini service d'ingestion IoT sur sockets TCP

## Objectif

L'objectif de ce TP est de transformer la base logicielle locale du TP2 en un service distribué utilisant le réseau. Le client envoie une requête contenant des mesures IoT, et le serveur reçoit, valide et répond à travers un socket TCP.

## Architecture

Le projet est organisé autour de plusieurs composants :

- models.py : définit les objets métier comme SensorReading, IngestRequest et IngestResponse.
- validators.py : contient les règles de validation des mesures.
- protocol.py : gère l'encodage, le décodage et le framing des messages JSON.
- server.py : lance le serveur TCP et traite les requêtes entrantes.
- client.py : construit et envoie les requêtes au serveur.
- main_demo.py : point d'entrée pour exécuter le client de démonstration.

## Protocole utilisé

Le protocole applicatif repose sur des messages JSON encodés en UTF-8. Chaque message contient un type, un request_id, une date d'envoi et un payload. Le framing est réalisé par un retour à la ligne afin de distinguer les messages dans le flux TCP.

## Fonctionnement

Le serveur écoute sur une adresse locale et attend les connexions entrantes.  
Le client lit les données depuis le fichier data/sample_readings.json, construit une requête d'ingestion, l'envoie au serveur et attend une réponse.

Le serveur décode la requête, applique les règles de validation, construit une réponse JSON puis l'envoie au client.

## Robustesse

Le code utilise des timeouts côté client et côté serveur. Il gère aussi les erreurs comme la connexion refusée, le timeout ou les messages invalides. Les logs permettent de suivre chaque requête grâce au request_id.

## Résultats

Le client lit les mesures depuis data/sample_readings.json, les envoie au serveur, reçoit une réponse JSON et sauvegarde le résultat dans outputs. Le serveur produit également ses logs dans logs/server.log.

## Difficultés rencontrées

Les principales difficultés concernent la séparation des messages dans le flux TCP, la gestion des erreurs réseau, la validation des données reçues et la traçabilité des requêtes avec request_id.

## Conclusion

Ce TP m'a permis de mieux comprendre la communication réseau bas niveau dans une application distribuée, ainsi que l'importance du protocole applicatif, de la validation, de la corrélation des messages et des logs.
