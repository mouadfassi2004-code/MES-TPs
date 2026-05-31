# Analyse finale - TP8

Si le volume de commandes double, il faut adapter le broker et les consumers. Le nombre de partitions peut être augmenté pour mieux répartir la charge.

Le système se rapproche d'une garantie at-least-once. Si une panne survient après le traitement d'un événement mais avant la sauvegarde de l'offset, l'événement peut être retraité. Pour limiter ce problème, les traitements doivent être idempotents.

Le stockage partitionné facilite les requêtes analytiques. Par exemple, pour chercher les livraisons échouées à Fès, il suffit de lire les fichiers correspondant à city=Fes et status=failed.

Si un consumer supplémentaire est ajouté, il faut vérifier le nombre de partitions. Si le nombre de consumers dépasse le nombre de partitions, certains consumers resteront inactifs.

Cette architecture reste une simulation locale, mais elle montre les principes essentiels des applications distribuées Big Data.
