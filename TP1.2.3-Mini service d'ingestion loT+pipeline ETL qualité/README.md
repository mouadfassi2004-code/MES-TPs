# SmartFarm IoT Ingestion + ETL Pipeline

## Description
Ce projet implémente un mini service d’ingestion IoT via TCP ainsi qu’un pipeline ETL batch permettant de nettoyer, enrichir et exporter les données acceptées.

## Structure
- `src/` : code source
- `data/` : données acceptées par le serveur
- `outputs/` : fichiers nettoyés et rapport qualité
- `logs/` : logs serveur/client/ETL + métriques

## Lancer le projet

### 1. Démarrer le serveur
```bash
python main.py