# Compte rendu - TP8 : Architecture distribuée Big Data

## 1. Introduction

Ce TP a pour objectif de regrouper les notions principales vues durant le semestre dans le module Applications Distribuées adaptées au parcours Big Data.  
Le travail consiste à construire une mini architecture distribuée orientée événements permettant de simuler le traitement de commandes et de livraisons.

Le projet repose sur plusieurs composants : un service de réception, des contrats de données, un broker local, des producteurs, des consumers, un système de partitionnement, la gestion des offsets, un stockage partitionné et un dashboard de synthèse.

## 2. Objectifs du TP

Les objectifs principaux sont :

- mettre en place une architecture événementielle ;
- définir des contrats de données clairs ;
- valider les commandes reçues ;
- produire des événements ;
- répartir les événements dans des partitions ;
- consommer les événements à l'aide de consumers ;
- sauvegarder et reprendre les offsets ;
- organiser les données dans un stockage partitionné ;
- produire un rapport final sous forme JSON.

## 3. Architecture générale

L'architecture du projet est composée des éléments suivants :

- `service/` : contient la logique de réception et de validation des commandes ;
- `contracts/` : définit les structures de données utilisées ;
- `producers/` : produit les événements à partir des commandes ;
- `broker/` : simule un broker événementiel local ;
- `consumers/` : lit les événements publiés dans les partitions ;
- `offsets/` : stocke les offsets de consommation ;
- `storage/` : conserve les événements sous forme partitionnée ;
- `dashboard/` : génère une synthèse des résultats ;
- `logs/` : contient les journaux d'exécution ;
- `outputs/` : contient les rapports générés.

## 4. Fonctionnement du système

Le système commence par recevoir une commande. Cette commande est vérifiée à l'aide des règles définies dans les contrats de données.  
Si la commande est valide, un événement est généré puis envoyé vers le broker.

Le broker répartit les événements dans plusieurs partitions. La clé de partitionnement utilisée est `order_id`, car elle permet de conserver l'ordre logique des événements liés à une même commande.

Les consumers lisent ensuite les événements depuis les partitions. Après traitement, ils sauvegardent leur progression dans des fichiers d'offsets. Cela permet de reprendre le traitement après un arrêt ou une panne.

Enfin, les résultats sont stockés dans des dossiers partitionnés et un dashboard produit un rapport global.

## 5. Partitionnement

Le choix de la clé `order_id` permet de garantir que tous les événements d'une même commande sont envoyés vers la même partition.

Ce choix est important car une commande peut passer par plusieurs états :

1. `order_created`
2. `order_validated`
3. `order_prepared`
4. `order_shipped`
5. `order_delivered` ou `delivery_failed`

En utilisant `order_id`, l'ordre des événements d'une même commande est mieux conservé.

## 6. Gestion des offsets

Les offsets représentent la position de lecture d'un consumer dans une partition.  
Après chaque traitement, le consumer sauvegarde l'offset correspondant.

En cas de panne, le système peut relire le dernier offset sauvegardé et reprendre le traitement à partir de cette position.

Cette logique permet de limiter la perte de données et de rendre le système plus robuste.

## 7. Reprise après panne

Une démonstration de reprise est fournie dans le fichier :

`logs/recovery_demo.log`

Ce fichier montre que le système peut redémarrer, relire les offsets sauvegardés et reprendre la consommation des événements.

## 8. Stockage partitionné

Les événements traités sont stockés dans des dossiers organisés selon certains critères, par exemple :

`storage/city=Fes/status=failed/`

Cette organisation facilite les analyses. Par exemple, pour rechercher les livraisons échouées à Fès, il suffit de consulter le dossier correspondant.

## 9. Résultats obtenus

Les principaux résultats sont :

- génération d'événements à partir des commandes ;
- partitionnement des événements ;
- consommation par plusieurs consumers ;
- sauvegarde des offsets ;
- simulation d'une reprise après panne ;
- production d'un rapport dashboard ;
- stockage partitionné des événements.

Les fichiers importants sont :

- `rapport_final.json`
- `outputs/dashboard_report.json`
- `outputs/test_summary.txt`
- `logs/recovery_demo.log`
- `offsets/offsets.json`

## 10. Difficultés rencontrées

Les principales difficultés concernent :

- le choix de la bonne clé de partitionnement ;
- la compréhension des offsets ;
- la simulation d'une reprise après panne ;
- la séparation des responsabilités entre service, broker, producer et consumer ;
- l'organisation du stockage partitionné.

## 11. Conclusion

Ce TP m'a permis de comprendre comment plusieurs concepts d'applications distribuées peuvent être combinés dans une architecture Big Data.

Il met en pratique les notions de service synchrone, événements, broker, partitionnement, offsets, consumers, reprise après panne, stockage partitionné et dashboard.

Même si le projet reste une simulation locale, il représente les principes fondamentaux d'une architecture distribuée moderne.
