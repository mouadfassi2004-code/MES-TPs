# TP6 - Mini Stream Processor IoT

## Objectif

Ce TP consiste à construire un mini processeur de flux IoT en Python.

L'objectif est de traiter des événements en continu, de les organiser par fenêtres temporelles et de produire des agrégations.

Le TP met en pratique :

- le stream processing ;
- les fenêtres temporelles ;
- les événements en retard ;
- le watermark ;
- les checkpoints ;
- les agrégations ;
- les logs et métriques.

## Technologies utilisées

- Python 3
- json
- csv
- logging
- datetime
- collections

## Structure du projet

TP6-Mini Stream Processor IoT/
├── src/
├── data/
├── outputs/
│   ├── aggregates.csv
│   ├── late_events.json
│   ├── dropped_events.json
│   ├── run_report.json
│   └── test_summary.txt
├── logs/
│   └── stream_processor.log
├── checkpoints/
│   └── state.json
├── requirements.txt
├── rapport_tp6.md
└── README.md

## Installation

Aucune dépendance externe n'est nécessaire.

Commande :

python --version

## Exécution

Depuis le dossier TP6 :

python main.py

Si le fichier principal est dans src :

python .\src\main.py

## Fonctionnement

Le programme lit des événements IoT, les trie selon leur timestamp, puis les traite dans des fenêtres temporelles.

Les événements trop en retard sont séparés dans un fichier spécifique. Les événements invalides sont enregistrés dans un fichier de rejet.

Les agrégations finales sont exportées dans le dossier outputs.

## Résultats attendus

Le TP produit :

- outputs/aggregates.csv : agrégations par fenêtre ;
- outputs/late_events.json : événements arrivés en retard ;
- outputs/dropped_events.json : événements rejetés ;
- outputs/run_report.json : rapport d'exécution ;
- checkpoints/state.json : état sauvegardé ;
- logs/stream_processor.log : logs d'exécution.

## Conclusion

Ce TP m'a permis de comprendre le traitement de flux, les fenêtres temporelles, la notion de watermark, la gestion des événements en retard et la sauvegarde d'état avec checkpoints.
