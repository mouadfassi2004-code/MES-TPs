# Rapport TP5 - Mini pipeline d'ingestion IoT

## Objectif
Ce TP met en place un pipeline asynchrone d'ingestion IoT basé sur une architecture producteur, queue et workers consommateurs.

## Architecture
Le producteur génère des messages IoT. Les messages sont placés dans une file de messages. Les workers les consomment, les valident puis les stockent. Les messages invalides ou échoués après plusieurs tentatives sont envoyés dans une dead-letter queue.

## Backpressure
La backpressure apparaît lorsque les producteurs envoient plus de messages que les workers ne peuvent en traiter. Le backlog augmente alors dans la queue. Pour corriger cela, on peut augmenter le nombre de workers, réduire le débit des producteurs ou augmenter la capacité de la queue.

## Dimensionnement
Pour 1000 messages/s, si un worker traite environ 120 messages/s, il faut au minimum 9 workers. Avec une marge de sécurité, 10 à 12 workers sont préférables.

## Résultats
Le TP produit des logs, des messages acceptés, une dead-letter queue et des métriques de traitement.

## Conclusion
Ce TP m'a permis de comprendre la communication asynchrone, le découplage, les retries, la dead-letter queue, la backpressure et l'observabilité.
