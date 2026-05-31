\# Rapport du Projet Final - CampusBot



\## Page de garde



\*\*Nom :\*\* Fassi Fihri Mouad

\*\*ID :\*\* 2300446

\*\*Module :\*\* Applications Distribuées

\*\*Parcours :\*\* Big Data

\*\*Année universitaire :\*\* 2025/2026



\---



\## 1. Introduction



Ce rapport présente le projet final intitulé \*\*CampusBot\*\*.

CampusBot est une application web basée sur une architecture distribuée permettant à un utilisateur d’accéder à une interface de chat et de poser des questions à un chatbot.



L’objectif principal du projet est de mettre en pratique les notions vues durant le module Applications Distribuées : séparation des services, communication entre composants, gestion des données, interface utilisateur et structuration professionnelle d’un projet.



Le projet est composé de trois parties principales :



\* `frontend` : interface utilisateur ;

\* `data\_service` : service chargé de la gestion des données ;

\* `chatbot\_service` : service responsable du traitement des questions et des réponses du chatbot.



\---



\## 2. Objectif du projet



L’objectif de CampusBot est de proposer une application simple permettant à un utilisateur de se connecter puis d’accéder directement à une interface de conversation.



Le système doit permettre :



\* l’accès à une interface web ;

\* la connexion de l’utilisateur ;

\* l’affichage automatique de la page de chat après connexion ;

\* l’envoi de questions au chatbot ;

\* la réception de réponses ;

\* la communication entre plusieurs services backend ;

\* l’organisation du projet sous forme d’architecture distribuée.



\---



\## 3. Architecture générale



Le projet est organisé en plusieurs services indépendants.



```text

Projet\_Final/

├── chatbot\_service/

├── data\_service/

├── frontend/

├── outputs/

├── Rapport\_Projet/

├── README.md

└── requirements.txt

```



Chaque dossier possède un rôle précis dans l’application.



\### 3.1 Frontend



Le dossier `frontend` contient l’interface utilisateur.

Il permet à l’utilisateur d’interagir avec l’application à travers une page web.



Le frontend gère principalement :



\* la page de connexion ;

\* l’accès à l’interface de chat ;

\* l’envoi des questions ;

\* l’affichage des réponses du chatbot.



\### 3.2 Data service



Le dossier `data\_service` représente le service responsable de la gestion des données.

Il peut contenir la logique de stockage, de recherche ou de préparation des informations utilisées par le chatbot.



Son rôle est de fournir les données nécessaires au service chatbot.



\### 3.3 Chatbot service



Le dossier `chatbot\_service` contient la logique du chatbot.

Ce service reçoit les questions envoyées depuis le frontend, les traite, puis renvoie une réponse à l’utilisateur.



Ce service représente le cœur intelligent de l’application.



\---



\## 4. Fonctionnement global de l’application



Le fonctionnement général de CampusBot suit les étapes suivantes :



1\. L’utilisateur ouvre l’interface web.

2\. Il se connecte à l’application.

3\. Après connexion, il est redirigé vers la page de chat.

4\. Il saisit une question.

5\. Le frontend envoie la question au backend.

6\. Le service chatbot traite la question.

7\. Si nécessaire, le chatbot récupère des informations depuis le service de données.

8\. Une réponse est renvoyée au frontend.

9\. L’utilisateur visualise la réponse dans l’interface de chat.



Cette organisation permet de séparer clairement l’interface, la logique métier et la gestion des données.



\---



\## 5. Technologies utilisées



Le projet utilise principalement :



\* Python pour les services backend ;

\* une interface web pour le frontend ;

\* des APIs locales pour la communication entre services ;

\* des fichiers de configuration et de dépendances ;

\* GitHub pour la gestion du code source.



Selon les services, le projet peut utiliser des frameworks comme FastAPI, Flask ou des outils web côté frontend.



\---



\## 6. Communication entre les services



CampusBot repose sur une communication entre plusieurs composants.



Le frontend communique avec les services backend à l’aide de requêtes HTTP.

Le service chatbot peut communiquer avec le service de données afin de récupérer les informations nécessaires pour générer une réponse.



Cette séparation correspond à une architecture distribuée simple :



```text

Utilisateur → Frontend → Chatbot Service → Data Service

```



Cette organisation rend le projet plus clair, plus maintenable et plus proche d’une architecture professionnelle.



\---



\## 7. Organisation du code



Le projet est structuré de manière modulaire.



```text

Projet\_Final/

├── chatbot\_service/

│   └── logique du chatbot

├── data\_service/

│   └── logique de gestion des données

├── frontend/

│   └── interface utilisateur

├── outputs/

│   └── résultats ou captures de fonctionnement

├── Rapport\_Projet/

│   └── rapport\_projet.md

├── README.md

└── requirements.txt

```



Cette organisation permet de comprendre rapidement le rôle de chaque composant.



\---



\## 8. Installation et exécution



Pour exécuter le projet, il faut d’abord installer les dépendances.



Exemple de commandes :



```powershell

python -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



Ensuite, chaque service peut être lancé dans un terminal différent.



Exemple :



```powershell

cd data\_service

python main.py

```



```powershell

cd chatbot\_service

python main.py

```



```powershell

cd frontend

npm install

npm run dev

```



Les commandes exactes peuvent varier selon les fichiers présents dans chaque service.



\---



\## 9. Résultats obtenus



Le projet permet d’obtenir une application web fonctionnelle avec une logique de chatbot.



Les résultats attendus sont :



\* ouverture de l’interface web ;

\* connexion utilisateur ;

\* accès à la page de chat ;

\* envoi d’une question ;

\* réception d’une réponse ;

\* communication entre les services ;

\* fonctionnement global de l’architecture multi-services.



Le dossier `outputs/` peut contenir des fichiers ou captures montrant le bon fonctionnement du projet.



\---



\## 10. Difficultés rencontrées



Plusieurs difficultés ont été rencontrées pendant la réalisation du projet :



\* organisation des services dans des dossiers séparés ;

\* communication entre le frontend et les services backend ;

\* redirection vers la page de chat après connexion ;

\* gestion des erreurs de connexion ;

\* coordination entre plusieurs terminaux ;

\* configuration des dépendances ;

\* préparation du projet pour GitHub ;

\* exclusion des fichiers inutiles comme `.venv`, `\_\_pycache\_\_` et les fichiers temporaires.



Ces difficultés ont permis de mieux comprendre les contraintes d’une application distribuée.



\---



\## 11. Améliorations possibles



Le projet peut être amélioré de plusieurs manières :



\* ajouter une authentification plus sécurisée ;

\* améliorer l’interface utilisateur ;

\* ajouter une base de données réelle ;

\* améliorer la qualité des réponses du chatbot ;

\* ajouter Docker pour lancer tous les services facilement ;

\* ajouter un fichier `docker-compose.yml` ;

\* ajouter des tests automatisés ;

\* améliorer la gestion des erreurs ;

\* ajouter un historique des conversations.



Ces améliorations permettraient de rendre l’application plus complète et plus proche d’un projet professionnel.



\---



\## 12. Lien avec le module Applications Distribuées



Ce projet applique plusieurs notions vues dans le module :



\* séparation des responsabilités ;

\* architecture multi-services ;

\* communication HTTP ;

\* backend et frontend séparés ;

\* gestion des dépendances ;

\* organisation GitHub ;

\* documentation ;

\* préparation d’un projet exécutable.



CampusBot représente donc une application distribuée simple mais cohérente.



\---



\## 13. Conclusion



Le projet CampusBot m’a permis de mettre en pratique les notions principales des applications distribuées.



À travers ce projet, j’ai appris à organiser une application en plusieurs services, à faire communiquer un frontend avec un backend, à gérer un service de données et à structurer un dépôt GitHub de manière professionnelle.



Même si le projet peut encore être amélioré, il constitue une base solide pour comprendre le fonctionnement d’une architecture distribuée moderne.



