# Rapport TP7 - Partitionnement, offsets et consumer groups

## Objectif

L'objectif de ce TP est de simuler les principes d'un système de streaming distribué. Le travail se concentre sur le partitionnement des messages, les offsets et les consumer groups.

## Partitionnement

Le partitionnement permet de répartir les messages entre plusieurs partitions. Une clé de partition est utilisée pour garantir qu'un même type de message arrive toujours dans la même partition.

Exemple : si la clé utilisée est `sensor_id`, alors les messages du même capteur sont toujours envoyés vers la même partition.

Cela permet de conserver l'ordre des messages pour une même clé tout en distribuant la charge entre plusieurs partitions.

## Offsets

Un offset représente la position d'un message dans une partition. Chaque consommateur doit mémoriser le dernier offset traité.

Grâce aux offsets, un consommateur peut reprendre le traitement après un arrêt sans relire tous les messages depuis le début.

## Consumer groups

Un consumer group regroupe plusieurs consommateurs. Les partitions sont distribuées entre les consommateurs du groupe.

Si le nombre de consommateurs augmente, les partitions sont réassignées. Cela permet de paralléliser le traitement.

Cependant, une partition ne peut être consommée que par un seul consommateur dans un même groupe à un moment donné.

## Reprise après arrêt

La reprise repose sur la sauvegarde des offsets. Lorsqu'un consommateur redémarre, il lit le fichier d'offsets et reprend à partir de la dernière position validée.

## Observabilité

Les logs permettent de suivre :

- l'assignation des partitions ;
- les offsets lus ;
- les messages consommés ;
- les snapshots de métriques ;
- la fin du traitement.

## Limites

Cette simulation utilise des fichiers locaux. Dans un vrai système comme Kafka, les partitions, les offsets et les consumer groups sont gérés par le broker.

## Conclusion

Ce TP m'a permis de comprendre les mécanismes fondamentaux du streaming distribué : partitionnement, offsets, consumer groups, rééquilibrage et reprise après arrêt.
