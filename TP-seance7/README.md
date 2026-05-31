# TP7 - Partitionnement, offsets et consumer groups

## Objectif

Ce TP consiste à simuler le fonctionnement d'un système de messagerie distribué inspiré de Kafka.

L'objectif est de comprendre :

- le partitionnement des messages ;
- le choix d'une clé de partition ;
- la notion d'offset ;
- le fonctionnement des consumer groups ;
- la répartition des partitions entre consommateurs ;
- la reprise après arrêt grâce aux offsets ;
- l'observabilité avec logs et métriques.

## Technologies utilisées

- Python 3
- json
- csv
- logging
- hashlib
- dataclasses
- fichiers locaux

## Structure du projet

TP-seance7/
├── src/
├── logs/
│   └── run.log
├── outputs/
│   ├── test_summary.txt
│   └── run_report.json
├── checkpoints/
│   └── offsets.json
├── requirements.txt
├── rapport_tp7.md
└── README.md

## Installation

Aucune dépendance externe n'est nécessaire.

Commande :

python --version

## Exécution

Depuis le dossier du TP7 :

python main.py

Si le fichier principal est dans le dossier src :

python .\src\main.py

## Fonctionnement

Le producteur envoie des messages IoT. Chaque message est affecté à une partition selon une clé, par exemple `sensor_id` ou `site_id`.

Les consommateurs appartiennent à un consumer group. Les partitions sont distribuées entre les consommateurs du groupe.

Chaque consommateur lit les messages depuis un offset précis. Après traitement, l'offset est sauvegardé afin de permettre une reprise sans retraiter tous les messages.

## Résultats attendus

Le TP doit produire :

- des messages répartis sur plusieurs partitions ;
- des offsets sauvegardés ;
- des logs d'assignation des partitions ;
- des métriques de consommation ;
- un résumé d'exécution.

## Conclusion

Ce TP m'a permis de comprendre les notions essentielles utilisées dans les systèmes distribués de streaming : partitionnement, offsets, consumer groups, reprise et observabilité.
