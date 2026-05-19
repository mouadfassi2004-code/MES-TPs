# Plateforme Big Data — Séance 9

Mini plateforme de données distribuée pour une chaîne de restauration.

## Objectif

Ce projet simule une plateforme Big Data distribuée avec :

- ingestion des événements,
- validation des contrats,
- topics événementiels,
- stockage bronze / silver / gold,
- traitement stream,
- traitement batch,
- orchestration,
- observabilité.

## Structure

```text
plateforme_bigdata/
├── contracts/
├── ingestion/
├── messaging/
├── processing/
│   ├── stream/
│   └── batch/
├── orchestration/
├── observability/
├── utils/
├── storage/
│   ├── bronze/
│   ├── silver/
│   └── gold/
└── main.py