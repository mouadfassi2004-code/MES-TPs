# Rapport TP9 - Architecture Big Data distribuée en Python

## 1. Introduction

Ce TP a pour objectif de mettre en place une mini plateforme Big Data distribuée en Python.  
Il permet de regrouper plusieurs notions étudiées durant le semestre : ingestion de données, stockage, traitement, reporting, dashboard et observabilité.

Le projet représente une architecture modulaire dans laquelle chaque composant possède un rôle précis.

## 2. Objectifs du TP

Les objectifs principaux de ce TP sont :

- organiser une architecture Big Data claire ;
- séparer les différentes couches du système ;
- simuler l'ingestion de données ;
- stocker les données localement ;
- appliquer un traitement sur les données ;
- produire des indicateurs ;
- générer un rapport final ;
- assurer l'observabilité grâce aux logs.

## 3. Architecture générale

Le projet est organisé autour de plusieurs dossiers :

- `data/` : contient les données d'entrée ;
- `src/` : contient le code source ;
- `logs/` : contient les journaux d'exécution ;
- `outputs/` : contient les résultats générés ;
- `docs/` : contient la documentation ;
- `main.py` : fichier principal permettant de lancer le projet.

Cette organisation permet de séparer les responsabilités et de rendre le projet plus lisible.

## 4. Fonctionnement du système

Le fonctionnement général suit plusieurs étapes :

1. Chargement des données d'entrée.
2. Ingestion des données.
3. Stockage local.
4. Traitement des données.
5. Calcul des indicateurs.
6. Génération des fichiers de sortie.
7. Écriture des logs.
8. Production d'un rapport final.

Chaque étape représente une brique importante dans une architecture Big Data.

## 5. Couche ingestion

La couche ingestion a pour rôle de récupérer les données d'entrée et de les préparer pour le traitement.

Dans une vraie architecture Big Data, cette couche pourrait être connectée à des sources comme des capteurs IoT, des fichiers, des API ou des systèmes de messagerie.

Dans ce TP, l'ingestion est simulée localement avec Python.

## 6. Couche stockage

Les données sont stockées dans des fichiers locaux, par exemple au format JSON, CSV ou JSONL.

Même si le stockage est local, il permet de comprendre le principe d'une zone de stockage dans une plateforme Big Data.

Dans un système réel, cette couche pourrait être remplacée par HDFS, un data lake, une base NoSQL ou un stockage objet.

## 7. Couche traitement

La couche traitement applique des calculs sur les données.

Elle peut produire :

- des comptages ;
- des moyennes ;
- des agrégations ;
- des indicateurs statistiques ;
- des résumés exploitables.

Cette étape transforme les données brutes en informations utiles.

## 8. Couche reporting et dashboard

Le projet produit des fichiers de sortie dans le dossier `outputs/`.

Ces fichiers permettent de vérifier les résultats du traitement et de résumer l'état global de la plateforme.

Le fichier `outputs/run_report.json` sert de rapport technique d'exécution.

Le fichier `outputs/test_summary.txt` donne un résumé plus lisible du test réalisé.

## 9. Observabilité

L'observabilité est assurée par les logs.

Le fichier `logs/run.log` permet de suivre les différentes étapes de l'exécution :

- démarrage du TP ;
- chargement des données ;
- ingestion ;
- traitement ;
- génération des résultats ;
- fin d'exécution.

Les logs sont importants pour comprendre le comportement du système et détecter les erreurs.

## 10. Résultats obtenus

Les fichiers importants générés ou ajoutés sont :

- `README.md`
- `requirements.txt`
- `docs/architecture_tp9.md`
- `docs/compte_rendu_tp9.md`
- `outputs/test_summary.txt`
- `outputs/run_report.json`
- `logs/run.log`
- `rapport_tp9.md`

Ces fichiers permettent de documenter le projet, de comprendre son fonctionnement et de vérifier les résultats.

## 11. Difficultés rencontrées

Les principales difficultés concernent :

- l'organisation correcte de l'architecture ;
- la séparation entre ingestion, stockage, traitement et reporting ;
- la production de fichiers de sortie clairs ;
- la documentation du fonctionnement du système ;
- la structuration des logs.

## 12. Apports du TP

Ce TP m'a permis de mieux comprendre comment une architecture Big Data peut être structurée.

Il montre l'importance de :

- la modularité ;
- la clarté du code ;
- la séparation des responsabilités ;
- la traçabilité ;
- la documentation ;
- les fichiers de sortie exploitables.

## 13. Conclusion

Ce TP représente une synthèse des notions liées aux architectures Big Data distribuées.

Même si le projet reste une simulation locale en Python, il permet de comprendre les principes essentiels d'une plateforme Big Data : ingestion, stockage, traitement, reporting et observabilité.

Il constitue une base utile pour comprendre des architectures plus avancées utilisant Kafka, Spark, Hadoop, Docker ou des services cloud.
