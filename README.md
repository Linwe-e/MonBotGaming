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
├── � .env.example         # Template configuration
├── �📁 cogs/                # Modules fonctionnels (commandes)
│   └── ai_gaming.py        # Module IA gaming hardcore
├── 📁 data/                # Templates de base de données
│   ├── builds.template.json    # Template stockage builds
│   ├── events.template.json    # Template événements 
│   └── users.template.json     # Template profils gaming
├── 📁 utils/               # Utilitaires transversaux
│   ├── database.py         # Gestion des données JSON
│   ├── gaming_helpers.py   # Fonctions gaming communes
│   ├── gemini_ai.py        # Interface IA Gemini hardcore
│   └── hardcore_config.py  # Configuration IA avancée
├── 📁 docs/                # Documentation
│   ├── architecture.md     # Schéma visuel du projet
│   ├── DEVELOPER.md        # Guide développeur
│   └── SECURITY.md         # Guide de sécurité
├── 📁 scripts/             # Outils de développement
│   ├── init_data.py        # Initialisation des données
│   ├── security_check.py   # Audit de sécurité
│   ├── show_structure.py   # Affichage structure projet
│   ├── install.py          # Script d'installation
│   └── diagnostic.py       # Diagnostic système
└── 📁 tests/               # Tests unitaires et d'intégration
    ├── test_bot_basic.py   # Tests du bot principal
    ├── test_ai_methods.py  # Tests des méthodes IA
    ├── test_hardcore_ai.py # Tests prompts hardcore
    ├── test_context_detection.py  # Tests détection contextuelle
    └── test_intelligent_detection.py  # Tests IA avancée
```

## 🎯 **Jeux Supportés**

### 🔥 **Jeux Principaux**
- **Diablo I-IV** : Builds optimisés, théorycrafting paragon
- **Escape from Tarkov** : Loadouts meta, stratégies farming
- **Helldivers 2** : Compositions d'équipe, stratégies mission
- **WoW Classic/Retail** : Optimisations DPS, rotations
- **Baldur's Gate 3** : Builds multiclasse, synergies
- **Space Marine II** : Configurations Warhammer 40K

### 🎮 **Catalogue Complet**
**Action/Aventure :** Space Marine II, Baldur's Gate 3, Enshrouded, Grounded  
**FPS/Shooter :** Escape from Tarkov, Helldivers 2  
**MMO/RPG :** WoW Classic, WoW Retail, Diablo I-IV  
**MOBA/Compétitif :** League of Legends  
**Coopératif :** Raft, Valheim, Sea of Thieves  
**Cartes/Stratégie :** MTG Arena, Jeux de cartes  
**Sport :** Rocket League  
**Autres :** Karabast, Waven, Un channel JDR dédié

*IA adaptée à plus de 17 jeux avec vocabulaire technique spécialisé*

## ⚡ **Installation Rapide**

1. **Cloner le projet** et installer les dépendances :
```bash
pip install -r requirements.txt
```

2. **Configurer les secrets** dans `.env` (copier depuis `.env.example`) :
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
- **Auto-initialisation** : Création automatique des vrais fichiers JSON
- **Configuration sécurisée** : `.env.example` fourni, `.env` protégé
- **Guide de sécurité** : Voir `docs/SECURITY.md`
- **Audit automatisé** : Script `security_check.py` (score 5/5)

## 🤖 **Commandes IA Hardcore**

### 💬 **Interaction Naturelle (Recommandé)**
- `@MonBotGaming [question]` - Conversation naturelle avec le bot
- `@MonBotGaming Comment optimiser mon build Necro Diablo 4 ?`
- `@MonBotGaming Salut !` - Salutation simple
- `@MonBotGaming Quelle est la meta Tarkov ?`

### ⌨️ **Commandes Classiques**
- `!ai ask [question]` - Assistant gaming technique
- `!ai build [jeu] [description]` - Analyse de builds poussée
- `!ai team [jeu] [activité] [joueurs]` - Compositions optimales
- `!ai event [jeu] [type] [détails]` - Événements motivants
- `!ai status` - Statut de l'IA

### 🎯 **Avantages des Mentions**
- **Plus naturel** : Parle au bot comme à un ami
- **Détection contextuelle** : IA adapte sa réponse au ton
- **Pas de syntaxe** : Juste mentionner et poser ta question
- **Réponses longues** : Gestion automatique des messages longs

## 🔧 **Architecture Technique**

- **Python 3.8+** avec `discord.py`
- **IA Gemini 2.0 Flash** (gratuit, 15 req/min)
- **Structure modulaire** avec cogs
- **Base de données JSON** légère
- **Configuration centralisée** 
- **Gestion d'erreurs** robuste

### 📊 **Statistiques du Projet**
- **31 fichiers** optimisés et organisés
- **18 modules Python** fonctionnels
- **5 tests** unitaires et d'intégration
- **Score sécurité : 5/5** (audit automatisé)
- **Architecture modulaire** prête pour l'évolution

## 🎮 **Philosophie Hardcore**

Ce bot est conçu pour des **gamers expérimentés** qui cherchent :
- Des conseils techniques avancés
- Du théorycrafting poussé
- Des optimisations meta
- Du vocabulaire gaming spécialisé
- Pas de conseils évidents

## 📊 **Évolutions Prévues**

- [ ] Cogs builds par jeu spécifique
- [ ] Système de classements communautaires
- [ ] Intégration APIs externes (WoWLogs, OP.GG, etc.)
- [ ] Notifications automatiques d'événements
- [ ] Interface web de gestion
- [ ] Support de nouveaux jeux gaming

## 🤝 **Contribution**

### Structure de Développement
- **`docs/DEVELOPER.md`** : Guide complet du développeur
- **`docs/SECURITY.md`** : Bonnes pratiques de sécurité
- **`scripts/`** : Outils de développement et diagnostic
- **Tests automatisés** : Validation continue du code

### Bonnes Pratiques
- Code modulaire et documenté
- Tests avant chaque merge
- Respect RGPD pour les données membres
- Sécurité par défaut (`.gitignore` robuste)

## 🧪 **Tests et Validation**

### Lancer les Tests
```bash
# Tests individuels
python tests/test_bot_basic.py          # Tests du bot principal
python tests/test_ai_methods.py         # Tests des méthodes IA
python tests/test_hardcore_ai.py        # Tests prompts hardcore
python tests/test_context_detection.py  # Tests détection contextuelle
python tests/test_intelligent_detection.py  # Tests IA avancée

# Tests complets (si pytest installé)
pytest tests/ -v
```

### Validation Sécurité
```bash
python scripts/security_check.py    # Audit complet de sécurité (score 5/5)
```

### Outils de Développement
```bash
python scripts/show_structure.py    # Affichage structure du projet
python scripts/diagnostic.py        # Diagnostic système complet
python scripts/install.py          # Installation automatisée
```

---

*Développé avec ❤️ pour la communauté gaming hardcore*
