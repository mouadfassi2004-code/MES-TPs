# TP5 - Mini pipeline d'ingestion IoT

## Objectif

Ce TP consiste à implémenter un mini pipeline asynchrone d'ingestion IoT en Python.

L'objectif est de passer d'une logique synchrone de type RPC à une architecture orientée messages :

producteur → file de messages → consommateurs → stockage

Le TP met en pratique :

- une file de messages avec `queue.Queue` ;
- des producteurs de messages IoT ;
- des workers consommateurs ;
- la gestion des retries ;
- une dead-letter queue ;
- des métriques de traitement ;
- l'observation du backlog, de la latence et de la backpressure.

## Technologies utilisées

- Python 3
- queue
- threading
- dataclasses
- json
- csv
- logging
- time

## Structure du projet

```text
TP5-Mini pipeline d'ingestion IoT/
├── src/
├── logs/
│   └── pipeline.log
├── outputs/
│   ├── accepted_messages.csv
│   ├── dead_letter_queue.jsonl
│   ├── metrics_snapshot.json
│   ├── run_report.json
│   └── test_summary.txt
├── requirements.txt
├── rapport_tp5.md
└── README.md