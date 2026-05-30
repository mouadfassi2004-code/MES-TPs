# Rapport TP2 - Base logicielle d'un service d'ingestion Big Data IoT

## Objectif

L'objectif de ce TP est de construire la base logicielle d'un service d'ingestion IoT dans un contexte Big Data agricole. Le travail se concentre sur la modélisation objet, les contrats de données, la validation, la sérialisation et la sécurisation des logs.

## Contexte

Des capteurs IoT envoient des mesures contenant la température, l'humidité, l'humidité du sol, l'état de la pompe et le débit d'irrigation. Ces données doivent être validées avant d'être acceptées par le service d'ingestion.

## Architecture

Le projet est organisé autour de plusieurs fichiers :

- `models.py` : contient les dataclasses principales comme `SensorReading`, `IngestRequest`, `IngestResponse` et `ValidationError`.
- `validators.py` : contient les validateurs métier.
- `serialization.py` : contient les fonctions de sérialisation JSON.
- `logger_config.py` : configure le système de logs.
- `main.py` : orchestre le chargement, la validation et les tests.

## Validation

Trois validateurs sont utilisés :

- `RequiredFieldsValidator` vérifie les champs obligatoires.
- `RangeValidator` vérifie les plages de valeurs numériques.
- `ConsistencyValidator` vérifie la cohérence entre l'état de la pompe et le débit d'irrigation.

## Résultats

Le programme détecte correctement les anomalies présentes dans le fichier `sample_readings.json`, notamment une humidité hors plage, une température invalide, un timestamp manquant et un identifiant capteur vide.

## Sécurité des logs

Les données envoyées dans les logs sont nettoyées afin d'éviter les retours à la ligne ou les caractères dangereux. La clé API est masquée pour éviter de laisser apparaître des informations sensibles dans les traces.

## Conclusion

Ce TP m'a permis de comprendre l'importance des contrats de données, de la validation défensive et du logging sécurisé dans une application distribuée Big Data.