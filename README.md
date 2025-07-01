# MonBotGaming
## 🚀 Fonctionnalités principales

- **Gaming assistant IA** (Gemini) : conseils builds, stratégies, détection intelligente de messages
- **Gestion de builds** : sauvegarde, partage, affichage par jeu (Diablo, Tarkov, WoW, etc.)
- **Planification d'événements** : raids, sessions, inscriptions, rappels automatiques
- **Mini-jeux Discord** : quiz, dés JDR, simulateur de loot, etc.
- **Statistiques & communauté** : profils, classements, matchmaking
- **Conformité RGPD complète** : 
  - Interface interactive avec boutons Discord
  - Export de données téléchargeable (Article 20 RGPD)
  - Gestion intelligente des permissions
  - Droit à l'oubli et suppression sécurisée
  - Consentement explicite et révocable
  - Chiffrement AES-256 des données conversationnellesng

Bot Discord gaming communautaire, modulaire et RGPD-friendly, inspiré de [Rhodham96/DiscordBot](https://github.com/Rhodham96/DiscordBot/).

## 📁 Structure du projet

```
MonBotGaming/
├── main.py              # Point d'entrée du bot
├── config.py            # Configuration centralisée (jeux, channels, etc.)
├── cogs/                # Modules fonctionnels (builds, events, strategies, etc.)
├── utils/               # Helpers, IA, base de données, RGPD
├── data/                # Données JSON (builds, users, events...)
├── tests/               # Tests unitaires et d’intégration (pytest)
├── requirements.txt     # Dépendances Python
└── README.md            # Ce fichier
```

## 🧪 Tests & Qualité

- **Pytest** avec structure unifiée : un fichier par domaine (`test_ai.py`, `test_core.py`, `test_rgpd.py`)
- **Fixtures partagées** dans `conftest.py`
- **Mock des APIs** et données de test séparées
- **Coverage** : `pytest --cov=utils --cov=cogs --cov-report=html tests/`

## ⚙️ Lancer le bot

```bash
pip install -r requirements.txt
python main.py
```

## 🔒 Commandes RGPD

Le bot propose une interface complète de gestion des données personnelles :

### Commandes principales
- `!privacy` - Interface interactive de gestion des données avec boutons
- `!privacy status` - Consulter le statut de vos données stockées
- `!privacy export` - Exporter vos données (fichier téléchargeable conforme Article 20)
- `!privacy forget` - Supprimer définitivement toutes vos données (droit à l'oubli)
- `!privacy accept` - Donner votre consentement pour le stockage des conversations
- `!privacy info` - Informations détaillées sur la gestion RGPD

### Fonctionnalités avancées
- **Export intelligent** : fichier téléchargeable si permissions OK, sinon affichage texte
- **Interface moderne** : boutons Discord interactifs pour une UX optimale
- **Sécurité renforcée** : messages éphémères, chiffrement AES-256, hachage anonymisant
- **Conformité légale** : respect complet du RGPD européen

## 🔑 Configuration

- Variables sensibles dans `.env` (token Discord, clés API)
- Jeux et channels configurables dans `config.py`

## 📚 Ressources utiles

- [discord.py docs](https://discordpy.readthedocs.io/fr/latest/)
- [pytest docs](https://docs.pytest.org/fr/latest/)
- [Rhodham96/DiscordBot](https://github.com/Rhodham96/DiscordBot/)

---

*Bot gaming communautaire, modulaire, RGPD-friendly et prêt pour l’aventure !*
