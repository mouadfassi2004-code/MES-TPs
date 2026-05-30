# Rapport TP1.2.3 - Mini service d'ingestion IoT + pipeline ETL qualité

## Objectif

L'objectif de ce TP est de combiner plusieurs notions vues dans les premières séances : ingestion de données IoT, validation, communication client/serveur, stockage local des données acceptées et traitement ETL de qualité.

## Architecture générale

Le projet contient un client, un serveur TCP, un module de validation, un module de stockage, un pipeline ETL et des fichiers de logs.

Le fonctionnement général est le suivant :

1. Le client construit des messages IoT.
2. Le serveur reçoit les messages via TCP.
3. Les données sont validées.
4. Les messages acceptés sont enregistrés dans `data/accepted_data.jsonl`.
5. Le pipeline ETL lit les données acceptées.
6. Les données sont nettoyées, enrichies et exportées dans `outputs/`.

## Composants principaux

- `src/client.py` : simule l'envoi de messages IoT.
- `src/server.py` : reçoit et traite les messages.
- `src/validator.py` : vérifie les champs obligatoires, les types, les dates et les plages de valeurs.
- `src/storage.py` : enregistre les messages acceptés.
- `src/etl_pipeline.py` : nettoie et enrichit les données.
- `src/metrics.py` : calcule les métriques d'exécution.
- `main.py` : propose un menu pour lancer le serveur, le client ou le pipeline ETL.

## Données

Le fichier `data/sample_batch.json` contient un lot de messages de test.  
Le fichier `data/accepted_data.jsonl` contient les données acceptées par le serveur ou simulées pour exécuter l'ETL.

## Validation

La validation vérifie notamment :

- la présence de `request_id`, `sensor_id`, `site_id`, `timestamp`, `temperature`, `humidity` et `irrigation` ;
- la validité du timestamp ;
- la conversion de temperature et humidity en nombres ;
- les plages de valeurs réalistes ;
- la normalisation de irrigation : ON, OFF, OUI, NON, TRUE, FALSE, 1, 0.

## Pipeline ETL

Le pipeline ETL effectue :

- lecture du fichier JSONL ;
- suppression des doublons par `request_id` ;
- conversion des dates ;
- conversion des colonnes numériques ;
- imputation des valeurs manquantes ;
- détection d'outliers ;
- création de features ;
- export CSV ;
- production d'un rapport qualité.

## Résultats

Les résultats sont disponibles dans :

- `outputs/cleaned_data.csv`
- `outputs/enriched_data.csv`
- `outputs/quality_report.txt`
- `logs/etl.log`
- `logs/run_metrics.json`

## Conclusion

Ce TP m'a permis de relier l'ingestion distribuée et le traitement de qualité des données. Il montre comment des données IoT peuvent être reçues, validées, stockées puis transformées dans une logique de pipeline Big Data.
