\# Rapport Final - Travaux Pratiques Applications Distribuées



\## Page de garde



\*\*Nom :\*\* Fassi Fihri Mouad

\*\*ID :\*\* 2300446

\*\*Module :\*\* Applications Distribuées

\*\*Parcours :\*\* Big Data

\*\*Année universitaire :\*\* 2025/2026



\---



\## 1. Introduction générale



Ce rapport final présente l'ensemble des travaux pratiques réalisés durant le semestre dans le module Applications Distribuées.

L'objectif principal de ces TPs était de comprendre les principes fondamentaux des architectures distribuées appliquées au domaine du Big Data.



Au fil des séances, les travaux ont permis de passer progressivement d'un simple pipeline de traitement de données à des architectures plus avancées intégrant des services réseau, des communications TCP, du RPC, des files de messages, du stream processing, du partitionnement, des offsets, des consumer groups et une mini plateforme Big Data complète.



Ce rapport résume les objectifs, les technologies utilisées, les résultats obtenus et les compétences développées à travers chaque TP.



\---



\## 2. Organisation du dépôt GitHub



Le dépôt GitHub est organisé de manière structurée afin de faciliter la lecture, l'exécution et l'évaluation des travaux.



La structure générale est la suivante :



```text

MES-TPs/

├── README.md

├── Rapport\_Final/

│   └── rapport\_final.md

└── TPs/

&#x20;   ├── TP1-Station météo \& irrigation/

&#x20;   ├── TP1.2.3-Mini service ingestion IoT et pipeline ETL/

&#x20;   ├── TP2-Base logicielle ingestion IoT/

&#x20;   ├── TP3-Sockets TCP/

&#x20;   ├── TP4-RPC Data Service/

&#x20;   ├── TP4.2-RPC Data Service IoT/

&#x20;   ├── TP5-Pipeline ingestion IoT/

&#x20;   ├── TP6-Stream Processor IoT/

&#x20;   ├── TP7-Partitionnement offsets consumer groups/

&#x20;   ├── TP8-Architecture distribuée Big Data/

&#x20;   └── TP9-Plateforme Big Data/

```



Chaque TP contient généralement :



\* un fichier `README.md` ;

\* le code source ;

\* les données d'entrée si nécessaires ;

\* les fichiers de sortie ;

\* les logs d'exécution ;

\* un fichier `requirements.txt` ;

\* un rapport ou compte rendu spécifique.



\---



\## 3. Synthèse des travaux pratiques



\## 3.1 TP1 - Station météo et irrigation



Le premier TP consistait à réaliser un mini pipeline ETL pour traiter des données météo et d'irrigation.



Le pipeline suit les étapes suivantes :



```text

extract → transform → quality\_report → build\_features → load

```



Les principales opérations réalisées sont :



\* lecture d'un fichier CSV brut ;

\* nettoyage des données ;

\* traitement des valeurs manquantes ;

\* détection des valeurs aberrantes ;

\* création de variables dérivées ;

\* génération d'un rapport qualité ;

\* export des résultats en CSV ;

\* journalisation des étapes dans un fichier log.



Ce TP a permis de comprendre les bases du Data Engineering et l'importance de la qualité des données.



\---



\## 3.2 TP1.2.3 - Mini service d'ingestion IoT et pipeline ETL qualité



Ce TP combine l'ingestion de données IoT avec un pipeline ETL de qualité.



Le système permet de recevoir des données IoT, de les valider, de stocker les données acceptées puis de les nettoyer et enrichir à travers un pipeline ETL.



Les notions travaillées sont :



\* validation de données IoT ;

\* stockage intermédiaire ;

\* nettoyage de données ;

\* génération de fichiers enrichis ;

\* production de logs et de métriques.



Ce TP a permis de relier les premières notions d'ingestion avec les principes de transformation et de qualité des données.



\---



\## 3.3 TP2 - Base logicielle d'un service d'ingestion Big Data IoT



Le TP2 portait sur la construction de la base logicielle d'un service d'ingestion IoT.



Il a permis de mettre en place :



\* des modèles de données ;

\* des contrats de données ;

\* des validateurs ;

\* la sérialisation JSON ;

\* le masquage des informations sensibles dans les logs ;

\* une logique de validation défensive.



Ce TP a introduit l'importance de construire une base robuste avant d'ajouter la communication réseau ou la distribution.



\---



\## 3.4 TP3 - Mini service d'ingestion IoT sur sockets TCP



Le TP3 a transformé la logique locale du TP2 en un service distribué utilisant des sockets TCP.



Le travail réalisé comprend :



\* un serveur TCP ;

\* un client TCP ;

\* un protocole applicatif basé sur JSON ;

\* un système de framing ;

\* des identifiants de corrélation `request\_id` ;

\* la gestion des erreurs réseau ;

\* les logs côté client et serveur.



Ce TP a permis de comprendre les bases de la communication réseau entre deux applications.



\---



\## 3.5 TP4 - Mini RPC Data Service



Le TP4 a introduit le concept de RPC, c'est-à-dire l'appel de méthodes distantes.



Le service RPC permet d'appeler plusieurs méthodes :



\* `health.ping` ;

\* `ingest.batch` ;

\* `stats.daily\_summary`.



Les éléments principaux du TP sont :



\* un protocole JSON-RPC simplifié ;

\* un routeur de méthodes ;

\* un serveur HTTP multi-threadé ;

\* un client RPC avec timeout et retries ;

\* des logs structurés ;

\* des métriques d'exécution.



Ce TP a permis de comprendre comment passer d'une simple communication TCP à une abstraction plus organisée autour de méthodes distantes.



\---



\## 3.6 TP4.2 - Mini RPC Data Service IoT



Le TP4.2 approfondit la logique RPC dans un contexte IoT.



Il ajoute notamment :



\* l'ingestion de lots de capteurs ;

\* la validation de lectures IoT ;

\* l'idempotence avec `batch\_id` ;

\* le calcul de statistiques ;

\* le classement des capteurs ;

\* la gestion des méthodes inconnues ;

\* les sorties et rapports de test.



Ce TP a renforcé la compréhension de la robustesse, de la validation et de l'observabilité dans un service distribué.



\---



\## 3.7 TP5 - Mini pipeline d'ingestion IoT



Le TP5 introduit une architecture asynchrone basée sur une file de messages.



L'architecture suivie est :



```text

producteur → queue → workers consommateurs → stockage

```



Les principales notions abordées sont :



\* production de messages ;

\* file d'attente ;

\* workers consommateurs ;

\* retry ;

\* dead-letter queue ;

\* backpressure ;

\* backlog ;

\* latence ;

\* métriques.



Ce TP a permis de comprendre pourquoi les architectures asynchrones sont utiles dans les systèmes Big Data à forte charge.



\---



\## 3.8 TP6 - Mini Stream Processor IoT



Le TP6 porte sur le stream processing.



Il permet de traiter des événements IoT en continu avec :



\* gestion du temps événementiel ;

\* fenêtres temporelles ;

\* watermark ;

\* événements en retard ;

\* événements rejetés ;

\* agrégations ;

\* checkpoints ;

\* logs.



Ce TP a permis de comprendre comment un système de traitement de flux peut gérer des événements arrivant dans le désordre ou en retard.



\---



\## 3.9 TP7 - Partitionnement, offsets et consumer groups



Le TP7 simule les concepts fondamentaux d'un système de streaming distribué inspiré de Kafka.



Les notions principales sont :



\* partitionnement des messages ;

\* choix d'une clé de partition ;

\* offsets ;

\* sauvegarde de progression ;

\* consumer groups ;

\* répartition des partitions entre consommateurs ;

\* reprise après arrêt ;

\* métriques et logs.



Ce TP a permis de comprendre comment les systèmes distribués répartissent la charge et assurent la reprise après panne.



\---



\## 3.10 TP8 - Architecture distribuée Big Data



Le TP8 est un travail de synthèse qui combine plusieurs notions vues dans les séances précédentes.



Le projet simule une architecture événementielle avec :



\* service de réception ;

\* contrats de données ;

\* producteur d'événements ;

\* broker local ;

\* consumers ;

\* partitionnement ;

\* offsets ;

\* stockage partitionné ;

\* dashboard ;

\* reprise après panne.



Ce TP a permis de relier les notions de service synchrone, d'événements, de consumers et de stockage structuré.



\---



\## 3.11 TP9 - Plateforme Big Data distribuée en Python



Le TP9 représente une mini plateforme Big Data organisée en plusieurs couches :



\* ingestion ;

\* messaging ;

\* stockage ;

\* processing ;

\* orchestration ;

\* observabilité ;

\* reporting.



Le projet utilise une organisation inspirée des architectures Big Data modernes avec des zones de stockage de type bronze, silver et gold.



Ce TP a permis de comprendre comment structurer une plateforme Big Data complète, même dans une simulation locale en Python.



\---



\## 4. Compétences acquises



À travers ces travaux pratiques, plusieurs compétences ont été développées :



\* structuration d'un projet Python ;

\* manipulation de fichiers CSV, JSON et JSONL ;

\* nettoyage et validation de données ;

\* conception de contrats de données ;

\* création de services TCP ;

\* mise en place d'un protocole RPC ;

\* gestion des logs ;

\* production de métriques ;

\* utilisation de files de messages ;

\* compréhension du stream processing ;

\* gestion des offsets ;

\* simulation de consumer groups ;

\* organisation d'une architecture Big Data.



Ces compétences sont importantes pour comprendre les bases des systèmes distribués et des plateformes Big Data.



\---



\## 5. Difficultés rencontrées



Les principales difficultés rencontrées durant les TPs sont :



\* organisation correcte des dossiers ;

\* gestion des dépendances Python ;

\* compréhension des communications réseau ;

\* gestion des erreurs dans les services distribués ;

\* simulation des brokers et offsets ;

\* compréhension de la backpressure ;

\* gestion des fichiers de sortie ;

\* production d'une documentation claire ;

\* nettoyage des fichiers temporaires ;

\* organisation finale du dépôt GitHub.



Ces difficultés ont permis de mieux comprendre les bonnes pratiques de développement et d'organisation d'un projet technique.



\---



\## 6. Conclusion générale



Ce semestre de travaux pratiques a permis de construire progressivement une compréhension solide des applications distribuées appliquées au Big Data.



Les premiers TPs ont introduit les bases : nettoyage, validation, contrats de données et sérialisation.

Les TPs suivants ont ajouté la communication réseau, les sockets TCP et les services RPC.

Ensuite, les travaux ont évolué vers des architectures asynchrones, du stream processing, du partitionnement, des offsets et des consumer groups.

Enfin, les derniers TPs ont permis de regrouper toutes ces notions dans des mini architectures Big Data complètes.



Ce travail m'a permis de mieux comprendre comment les données peuvent être ingérées, validées, transportées, traitées, stockées et analysées dans une architecture distribuée.



Même si les projets restent des simulations locales en Python, ils représentent les principes fondamentaux utilisés dans des technologies réelles comme Kafka, Spark, Hadoop, Airflow, Docker et les plateformes cloud Big Data.



