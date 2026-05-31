# Analyse fonctionnelle - TP8

## Contexte

Le projet simule une plateforme distribuée de traitement de commandes et de livraisons.

Une commande passe par plusieurs états : création, validation, préparation, expédition, livraison ou échec.

## Acteurs

- Client : crée une commande.
- Service : reçoit et valide la commande.
- Producteur : transforme la commande en événement.
- Broker : stocke les événements dans des partitions.
- Consumers : traitent les événements.
- Dashboard : produit un rapport de synthèse.

## Besoins fonctionnels

Le système doit :

- recevoir une commande ;
- valider les champs obligatoires ;
- produire un événement ;
- partitionner les événements ;
- consommer les événements ;
- sauvegarder les offsets ;
- permettre une reprise après panne ;
- produire un rapport final.

## Conclusion

Cette architecture montre comment plusieurs composants distribués peuvent coopérer autour d'un flux d'événements.
