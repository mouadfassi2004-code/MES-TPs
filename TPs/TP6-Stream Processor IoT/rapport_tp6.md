# Rapport TP6 - Mini Stream Processor IoT

## Objectif

L'objectif de ce TP est de réaliser un mini processeur de flux IoT. Le programme traite des événements en continu et calcule des agrégations sur des fenêtres temporelles.

## Architecture

L'architecture repose sur plusieurs étapes :

1. Lecture des événements IoT.
2. Validation des champs obligatoires.
3. Traitement selon le temps événementiel.
4. Gestion du watermark.
5. Classement des événements normaux, tardifs ou rejetés.
6. Calcul des agrégations par fenêtre.
7. Sauvegarde de l'état dans un checkpoint.
8. Export des résultats.

## Fenêtres temporelles

Les événements sont regroupés par fenêtres de temps. Pour chaque fenêtre, le programme calcule des indicateurs comme :

- nombre d'événements ;
- moyenne ;
- minimum ;
- maximum ;
- capteurs concernés.

## Watermark

Le watermark permet de décider jusqu'à quel moment les événements sont considérés comme acceptables.

Un événement qui arrive après le watermark peut être considéré comme tardif. Il est alors enregistré dans late_events.json.

## Événements rejetés

Les événements invalides sont placés dans dropped_events.json. Cela peut concerner :

- un timestamp invalide ;
- une valeur manquante ;
- une valeur non numérique ;
- un identifiant capteur vide.

## Checkpoint

Le checkpoint permet de sauvegarder l'état du traitement. En cas d'arrêt ou de reprise, il permet de conserver les informations nécessaires au suivi du flux.

## Résultats

Les principaux fichiers de sortie sont :

- outputs/aggregates.csv ;
- outputs/late_events.json ;
- outputs/dropped_events.json ;
- outputs/run_report.json ;
- logs/stream_processor.log ;
- checkpoints/state.json.

## Conclusion

Ce TP m'a permis de comprendre les bases du stream processing dans un contexte Big Data, notamment les fenêtres temporelles, le watermark, la gestion des retards, les checkpoints et l'observabilité.
