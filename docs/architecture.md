# 🏗️ Architecture MonBotGaming

## 📊 Vue d'ensemble du système

```
🎮 MonBotGaming Architecture
┌─────────────────────────────────────────────────────────┐
│                    🚀 main.py                          │
│                 (Point d'entrée)                        │
└─────────────────────┬───────────────────────────────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
┌───────────▼──────────┐ ┌──────▼──────┐
│   ⚙️ config.py       │ │ 🤖 cogs/    │
│ (Configuration)      │ │ (Modules)   │
└──────────────────────┘ └─────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
            ┌───────▼──┐ ┌──────▼──┐ ┌─────▼─────┐
            │🔧 builds │ │🎯 events│ │👥 community│
            │   .py    │ │   .py   │ │    .py    │
            └──────────┘ └─────────┘ └───────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
            ┌───────▼──┐ ┌──────▼──┐ ┌─────▼─────┐
            │🛠️ utils/ │ │📊 data/ │ │📚 docs/   │
            │(Helpers) │ │(Storage)│ │(Guides)   │
            └──────────┘ └─────────┘ └───────────┘
```

## 🔄 Flux de données

1. **Discord Event** → `main.py` 
2. **Command Detection** → Specific `cog`
3. **RGPD Consent Check** → `rgpd_consent_ui.py`
4. **Data Processing** → `utils/` helpers
5. **Storage** → `data/` JSON files (encrypted)
6. **Response** → Discord embed/message

## 🎮 Gaming Logic

```
User Input: "!ai ask meilleur build necro"
    │
    ▼
┌─────────────────────────────────────┐
│ ai_gaming.py (Cog)                  │
│ ├─ Parse game context              │
│ ├─ Call gemini_ai.py               │
│ └─ Format response                 │
└─────────────────────────────────────┘
    │
    ▼ 
┌─────────────────────────────────────┐
│ utils/gemini_ai.py                  │
│ ├─ Hardcore prompts                │
│ ├─ Game-specific context           │
│ └─ Generate response               │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Discord Rich Embed                  │
│ ├─ Game-themed colors              │
│ ├─ Structured response             │
│ └─ Interactive elements            │
└─────────────────────────────────────┘
```

## 🎯 Jeux supportés

```
🔥 Diablo 4        🔫 Escape from Tarkov
⚔️ WoW Classic     ⚡ League of Legends  
🏹 Baldur's Gate 3  🚀 Helldivers 2
🏴‍☠️ Sea of Thieves  🃏 MTG Arena
... et plus encore !
```

## 📈 Évolutivité

L'architecture modulaire permet d'ajouter facilement :
- ✅ Nouveaux jeux via `config.py`
- ✅ Nouvelles commandes via `cogs/`
- ✅ Nouvelles fonctions via `utils/`
- ✅ Nouvelles données via `data/`
