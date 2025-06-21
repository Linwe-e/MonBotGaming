# 🏗️ Architecture MonBotGaming

## 📊 Schéma Visual de l'Architecture

```mermaid
flowchart TD
    %% Définition des groupes principaux
    subgraph Discord [🎮 Discord Bot]
        direction TB
        main["`🚀 **main.py**
        Point d'entrée
        Gestion connexions`"]
        config["`⚙️ **config.py**
        Configuration
        Préfixes par jeu`"]
    end
    
    subgraph Modules [🔧 Modules Gaming]
        direction TB
        builds["`🛠️ **builds.py**
        Builds/Loadouts
        Par jeu`"]
        events["`📅 **events.py**
        Événements
        Planification`"]
        strategies["`🎯 **strategies.py**
        Guides & Conseils
        IA intégrée`"]
        community["`👥 **community.py**
        Social & Stats
        Classements`"]
        fun["`🎲 **fun.py**
        Mini-jeux
        Animations`"]
    end
    
    subgraph Data [💾 Base de Données]
        direction TB
        builds_db["`📊 **builds.json**
        Stockage builds
        Par utilisateur`"]
        events_db["`📅 **events.json**
        Événements
        Participants`"]
        users_db["`👤 **users.json**
        Profils gaming
        Statistiques`"]
    end
    
    subgraph External [🌐 Services Externes]
        direction TB
        discord_api["`💬 **Discord API**
        Interface principale`"]
        gemini_api["`🤖 **Gemini AI**
        Assistant gaming`"]
    end
    
    %% Connexions principales
    main --> builds
    main --> events
    main --> strategies
    main --> community
    main --> fun
    
    config --> main
    
    %% Connexions vers la base de données
    builds --> builds_db
    events --> events_db
    community --> users_db
    
    %% Connexions externes
    main --> discord_api
    strategies --> gemini_api
    
    %% Styles
    classDef coreStyle fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef moduleStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef dataStyle fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef externalStyle fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    class main,config coreStyle
    class builds,events,strategies,community,fun moduleStyle
    class builds_db,events_db,users_db dataStyle
    class discord_api,gemini_api externalStyle
```

## 🎯 Description des Composants

### 🔧 Core Bot
- **main.py** : Point d'entrée, gère la connexion Discord
- **config.py** : Configuration centralisée (préfixes, channels, jeux)

### 🎮 Modules Gaming
- **builds.py** : Gestion des builds/loadouts par jeu
- **events.py** : Planification d'événements gaming
- **strategies.py** : Guides et conseils avec IA
- **community.py** : Système social et stats
- **fun.py** : Mini-jeux et animations

### 💾 Données
- **builds.json** : Stockage des builds par jeu et utilisateur
- **events.json** : Événements planifiés et participants
- **users.json** : Profils gaming et statistiques

### 🌐 Services Externes
- **Discord API** : Interface principale avec Discord
- **Gemini AI** : Assistant IA pour conseils gaming

## 🔄 Flux de Données

1. **Utilisateur** → **Discord** → **main.py**
2. **main.py** → **Module approprié** (builds, events, etc.)
3. **Module** → **Base de données JSON** (lecture/écriture)
4. **Module** → **Service externe** (si nécessaire)
5. **Réponse** → **Discord** → **Utilisateur**

## 📝 Jeux Supportés

### 🎯 Stratégie/RPG
- Space Marine II, Baldur's Gate 3, Diablo I-IV
- WoW Classic/Retail, Valheim, Enshrouded

### 🔫 Action/FPS
- Escape from Tarkov, Helldivers 2

### 🎲 Multijoueur
- League of Legends, Rocket League, Sea of Thieves
- MTG Arena, Raft, Waven

### 🎭 Roleplay
- JDR (Jeu de Rôle) avec générateurs d'événements
