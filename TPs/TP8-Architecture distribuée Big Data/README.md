# TP8 - Intégration des concepts d'applications distribuées Big Data

## Objectif

Ce TP est une synthèse des notions vues durant les séances précédentes. Il met en place une mini architecture distribuée orientée événements dans un contexte Big Data.

Le projet regroupe :

- un service de réception des commandes ;
- des contrats de données ;
- un broker local ;
- des producteurs d'événements ;
- des consumers ;
- du partitionnement ;
- la gestion des offsets ;
- un stockage partitionné ;
- un dashboard de synthèse.

## Technologies utilisées

- Python 3
- JSON
- JSONL
- Logging
- Architecture événementielle
- Partitionnement local
- Offsets locaux

## Structure du projet

projet_s8/
├── broker/
├── consumers/
├── contracts/
├── dashboard/
├── data/
├── docs/
├── logs/
├── offsets/
├── outputs/
├── producers/
├── service/
├── state/
├── storage/
├── main.py
└── rapport_final.json

## Exécution

Depuis le dossier du projet :

python main.py

## Fonctionnement

Le système simule une architecture Big Data distribuée.

Le service reçoit des commandes, les valide et produit des événements.  
Les événements sont publiés dans un broker local, puis répartis dans des partitions.  
Les consumers lisent les événements, sauvegardent les offsets et mettent à jour les résultats.  
Le stockage est organisé par ville et par statut pour faciliter les analyses.

## Résultats

Les résultats importants sont disponibles dans :

- rapport_final.json
- outputs/dashboard_report.json
- outputs/test_summary.txt
- logs/recovery_demo.log
- offsets/offsets.json

## Conclusion

Ce TP permet de relier les notions de service synchrone, broker, événements, partitionnement, offsets, consumers, stockage partitionné, reprise après panne et reporting.
