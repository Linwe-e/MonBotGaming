# Fichier de Contexte pour le projet MonBotGaming

Ce document sert de guide pour l'assistant IA Gemini. Il contient les informations essentielles sur le projet, ses conventions et ses commandes.

## 1. Vue d'ensemble du projet

- **Nom du projet :** MonBotGaming
- **Objectif :** Un bot Discord pour les joueurs, offrant des fonctionnalités liées aux jeux, des builds, des événements, etc. Il intègre l'IA Gemini pour des réponses intelligentes.
- **Langage principal :** Python

## 2. Stack Technique

- **Bibliothèque Discord :** `discord.py==2.3.2`
- **API externe :** Google Gemini AI (via `utils/gemini_ai.py`).
- **Gestion des dépendances :** `pip` avec `requirements.txt`.
- **Gestion des secrets :** Les variables d'environnement sont chargées depuis un fichier `.env` à la racine du projet via `python-dotenv`.
- **Framework de test :** `pytest` (probablement installé globalement ou comme dépendance de développement).

## 3. Variables d'environnement

Le fichier `.env` doit contenir les variables suivantes :

- `DISCORD_TOKEN`: Le token du bot Discord.
- `GEMINI_API_KEY`: La clé API pour Google Gemini.

## 4. Commandes essentielles

- **Installer les dépendances :** `pip install -r requirements.txt`
- **Lancer le bot :** `python main.py`
- **Lancer les tests :** `pytest`
- **Vérifier le style du code (linting) :** (À définir)

## 5. Structure du projet

- **`main.py` :** Point d'entrée principal du bot. Charge les cogs et lance la connexion à Discord.
- **`config.py` :** Gère la configuration (tokens, préfixes, etc.).
- **`cogs/` :** Contient les modules de commandes (les "Cogs") du bot, organisés par fonctionnalité.
- **`utils/` :** Fonctions et classes utilitaires réutilisées dans le projet (gestion de base de données, appels IA, etc.).
- **`data/` :** Stocke les données persistantes, comme les builds de jeux, les utilisateurs, etc. Les fichiers `.json` sont des templates.
- **`scripts/` :** Contient des scripts pour l'automatisation (déploiement, diagnostics, etc.).
- **`tests/` :** Contient les tests unitaires et d'intégration utilisant `pytest`.

## 6. Conventions de code

- **Style de code :** Suivre la PEP 8.
- **Nommage :**
    - Variables et fonctions : `snake_case`
    - Classes : `PascalCase`
- **Docstrings :** Toutes les fonctions et classes publiques doivent avoir une docstring expliquant leur rôle.
- **Typage :** Utiliser les type hints de Python partout où c'est possible.

## 7. Préférences et Principes

- **Utilisateur :** Débutant. Fournir des explications claires, guider vers les bonnes pratiques et être patient.
- **Sécurité :** La protection des données est une priorité absolue. Ne jamais exposer de clés API ou d'informations personnelles dans le code ou les logs. Toujours privilégier les variables d'environnement.
- **Méthodologie :** L'utilisateur souhaite éviter le "vibe coding". Toujours proposer un plan ou une structure avant d'écrire du code complexe. Décomposer les problèmes en étapes logiques.
- **Communication :** Préfère des explications claires et concises en français.
- **Commits :** Suivre le format "Conventional Commits" (par exemple : `feat: ajoute la commande /build`).