# 🎮 MonBotGaming

Bot Discord gaming modulaire et évolutif pour serveurs hardcore, avec IA Gemini intégrée.

## 🚀 **Fonctionnalités**

- **🤖 Assistant IA Gaming** : Conseils techniques avancés avec Gemini 2.0 Flash
- **🔧 Gestion de builds** : Stockage et analyse de configurations optimales
- **📅 Événements gaming** : Planification de sessions et raids
- **👥 Outils communautaires** : Renforcement des liens entre gamers
- **🎲 Mini-jeux** : Animation du serveur entre les sessions

## 📁 **Structure du Projet**

```
MonBotGaming/
├── 📄 main.py              # Point d'entrée principal du bot
├── 📄 config.py            # Configuration centralisée
├── 📄 requirements.txt     # Dépendances Python
├── 📄 .env                 # Variables secrètes (non versionné)
├── 📁 cogs/                # Modules fonctionnels (commandes)
│   └── ai_gaming.py        # Module IA gaming hardcore
├── 📁 data/                # Base de données JSON
│   ├── builds.json         # Stockage des builds
│   ├── events.json         # Événements planifiés
│   └── users.json          # Profils gaming
├── 📁 utils/               # Utilitaires transversaux
│   ├── database.py         # Gestion des données JSON
│   ├── gaming_helpers.py   # Fonctions gaming communes
│   ├── gemini_ai.py        # Interface IA Gemini hardcore
│   └── hardcore_config.py  # Configuration IA avancée
├── 📁 docs/                # Documentation
│   ├── architecture.md     # Schéma visuel du projet
│   └── SECURITY.md         # Guide de sécurité
├── 📁 scripts/             # Outils de développement
│   ├── init_data.py        # Initialisation des données
│   └── security_check.py   # Audit de sécurité
├── 📁 tests/               # Tests unitaires et d'intégration
│   ├── test_bot_basic.py   # Tests du bot principal
│   ├── test_ai_methods.py  # Tests des méthodes IA
│   └── test_hardcore_ai.py # Tests prompts hardcore
└── 📁 archive/             # Anciennes versions sauvegardées
```

## 🎯 **Jeux Supportés**

- **Diablo I-IV** : Builds optimisés, théorycrafting paragon
- **Escape from Tarkov** : Loadouts meta, stratégies farming
- **Helldivers 2** : Compositions d'équipe, stratégies mission
- **WoW Classic/Retail** : Optimisations DPS, rotations
- **Baldur's Gate 3** : Builds multiclasse, synergies
- **Space Marine II** : Configurations Warhammer 40K
- **LOL, MTG Arena, Sea of Thieves** et plus...

## ⚡ **Installation Rapide**

1. **Cloner le projet** et installer les dépendances :
```bash
pip install -r requirements.txt
```

2. **Configurer les secrets** dans `.env` :
```env
DISCORD_TOKEN=ton_token_discord
GEMINI_API_KEY=ta_cle_gemini_ai
```

3. **Initialiser les données** (première fois) :
```bash
python scripts/init_data.py
```

4. **Lancer le bot** :
```bash
python main.py
```

## 🛡️ **Sécurité et Confidentialité**

- **Données membres protégées** : Non versionnées, respectent la RGPD
- **Templates fournis** : Structure visible sans données sensibles  
- **Auto-initialisation** : Création automatique des fichiers nécessaires
- **Guide de sécurité** : Voir `docs/SECURITY.md`

## 🤖 **Commandes IA Hardcore**

- `!ai ask [question]` - Assistant gaming technique
- `!ai build [jeu] [description]` - Analyse de builds poussée
- `!ai team [jeu] [activité] [joueurs]` - Compositions optimales
- `!ai event [jeu] [type] [détails]` - Événements motivants
- `!ai status` - Statut de l'IA

## 🔧 **Architecture Technique**

- **Python 3.8+** avec `discord.py`
- **IA Gemini 2.0 Flash** (gratuit, 15 req/min)
- **Structure modulaire** avec cogs
- **Base de données JSON** légère
- **Configuration centralisée** 
- **Gestion d'erreurs** robuste

## 🎮 **Philosophie Hardcore**

Ce bot est conçu pour des **gamers expérimentés** qui cherchent :
- Des conseils techniques avancés
- Du théorycrafting poussé
- Des optimisations meta
- Du vocabulaire gaming spécialisé
- Pas de conseils évidents

## 📊 **Évolutions Prévues**

- [ ] Cogs builds par jeu spécifique
- [ ] Système de classements
- [ ] Intégration APIs externes (WoWLogs, etc.)
- [ ] Notifications automatiques
- [ ] Interface web de gestion

## 🧪 **Tests et Validation**

### Lancer les Tests
```bash
# Tests individuels
python tests/test_bot_basic.py      # Tests du bot principal
python tests/test_ai_methods.py     # Tests des méthodes IA
python tests/test_hardcore_ai.py    # Tests prompts hardcore

# Tests complets (si pytest installé)
pytest tests/ -v
```

### Validation Sécurité
```bash
python scripts/security_check.py    # Audit complet de sécurité
```

---

*Développé avec ❤️ pour la communauté gaming hardcore*
