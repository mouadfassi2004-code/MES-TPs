# TP3 - Mini service d'ingestion IoT sur sockets TCP

## Objectif

Ce TP consiste à implémenter un mini service d'ingestion IoT basé sur une communication réseau TCP.

L'objectif est de faire communiquer un client et un serveur en utilisant :
- des sockets TCP ;
- des messages JSON ;
- un protocole applicatif simple ;
- un framing par retour à la ligne ;
- un identifiant de corrélation request_id ;
- des logs côté client et serveur.

## Technologies utilisées

- Python 3
- socket
- json
- logging
- dataclasses
- fichiers JSON

## Structure du projet

seance3_ingestion/
├── data/
│   └── sample_readings.json
├── logs/
│   ├── client.log
│   └── server.log
├── outputs/
│   └── test_summary.txt
├── src/
│   ├── client.py
│   ├── models.py
│   ├── protocol.py
│   ├── server.py
│   └── validators.py
├── main_demo.py
├── requirements.txt
└── rapport_tp3.md

## Installation

Aucune dépendance externe n'est nécessaire.

Vérifier la version de Python :

python --version

## Exécution

Ouvrir deux terminaux.

Terminal 1 - Lancer le serveur :

cd "C:\Users\Utilisateur\Desktop\S6-25.26\Applications reparties\MES-TPs\TP3-Mini service d'ingestion IoT sur sockets TCP\seance3_ingestion"
python .\src\server.py

Terminal 2 - Lancer le client :

cd "C:\Users\Utilisateur\Desktop\S6-25.26\Applications reparties\MES-TPs\TP3-Mini service d'ingestion IoT sur sockets TCP\seance3_ingestion"
python .\main_demo.py

## Résultats attendus

Après l'exécution, le serveur reçoit une requête d'ingestion envoyée par le client.  
Le serveur valide les mesures IoT, renvoie une réponse JSON et sauvegarde le résultat dans le dossier outputs.

Les fichiers utiles sont :
- logs/server.log
- logs/client.log
- outputs/test_summary.txt
- outputs/response_<request_id>.json si généré par le serveur
- outputs/client_response_<request_id>.json si généré par le client

## Conclusion

Ce TP m'a permis de comprendre le rôle des sockets TCP dans les applications distribuées, la sérialisation JSON, le framing des messages, la gestion des erreurs réseau et l'observabilité par les logs.
