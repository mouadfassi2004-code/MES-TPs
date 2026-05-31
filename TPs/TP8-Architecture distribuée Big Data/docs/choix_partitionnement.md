# Choix de partitionnement - TP8

## Clé choisie

La clé de partition retenue est order_id.

## Justification

Le choix de order_id permet de garantir que tous les événements d'une même commande vont dans la même partition.

Cela permet de conserver l'ordre logique des événements d'une commande :

1. order_created
2. order_validated
3. order_prepared
4. order_shipped
5. order_delivered ou delivery_failed

## Comparaison avec city

Une clé basée sur city faciliterait les analyses par ville, mais pourrait créer un déséquilibre si une ville produit beaucoup plus d'événements que les autres.

## Conclusion

order_id est le choix le plus adapté pour préserver l'ordre des événements liés à une même commande.
