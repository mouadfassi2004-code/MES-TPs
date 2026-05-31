# TP1 - Station météo & irrigation

## Objectif

Ce TP consiste à créer un mini-pipeline ETL en Python pour nettoyer un fichier météo brut, produire un rapport de qualité, créer des variables dérivées et exporter des résultats exploitables.

Le pipeline suit les étapes suivantes :

```text
extract → transform → quality_report → build_features → load