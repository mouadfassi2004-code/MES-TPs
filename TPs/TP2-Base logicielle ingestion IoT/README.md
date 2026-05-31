# TP2 - Base logicielle d'un service d'ingestion Big Data IoT

## Objectif

Ce TP consiste à construire la base logicielle d'un service d'ingestion IoT dans un contexte Big Data.  
Le but est de modéliser les messages reçus par un service d'ingestion, de les valider, de les sérialiser et de produire des logs sécurisés.

## Technologies utilisées

- Python 3.10+
- Dataclasses
- JSON
- Logging
- Programmation orientée objet

## Structure du projet

```text
seance2_ingestion/
├── data/
│   └── sample_readings.json
├── logs/
│   └── ingestion.log
├── outputs/
│   └── run_summary.txt
├── logger_config.py
├── main.py
├── models.py
├── serialization.py
├── validators.py
├── requirements.txt
└── rapport_tp2.md