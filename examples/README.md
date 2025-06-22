# 📖 Guide du Dossier Examples

## 🎯 **Objectif**
Ce dossier contient des **exemples pratiques** pour développer des fonctionnalités Discord.py modernes dans MonBotGaming.

## 📁 **Structure et Usage**

### 🎮 **button_examples.py**
**Usage :** Menus interactifs pour builds gaming
```python
# Exemples concrets :
- Menu builds Diablo 4 (Necro, Rogue, Sorc)
- Loadouts Tarkov (Budget PMC, Chad)
- Builds WoW Classic (Tank, DPS)
```

### 🎨 **embed_examples.py** 
**Usage :** Embeds riches stylés par jeu
```python
# Fonctions réutilisables :
- create_diablo_build_embed()
- create_wow_raid_embed()
- create_player_stats_embed()
```

### 📝 **modal_examples.py**
**Usage :** Formulaires pour créer contenus
```python
# Modals disponibles :
- CreateEventModal (événements gaming)
- SaveBuildModal (sauvegarder builds)
- JoinTeamModal (rejoindre équipes)
```

### ⚡ **slash_commands_examples.py**
**Usage :** Commandes modernes Discord
```python
# Slash commands implémentées :
- /build (gérer builds)
- /event (événements)
- /team (équipes)
- /stats (statistiques)
```

### 🧪 **demo_ux_ui.py**
**Usage :** Tester les améliorations interface
```bash
python examples/demo_ux_ui.py
```

### 👁️ **visual_demo.py**
**Usage :** Visualiser évolution UX (avant/après)
```bash
python examples/visual_demo.py
```

## 🔄 **Intégration dans le Bot Principal**

```python
# Dans tes cogs, importer les fonctions :
from examples.embed_examples import create_diablo_build_embed

# Réutiliser directement :
embed = create_diablo_build_embed(build_data)
await ctx.send(embed=embed)
```

## 🎯 **Maintenance**

- **Synchroniser** avec les évolutions du code principal
- **Tester** régulièrement les exemples
- **Ajouter** de nouveaux jeux selon besoins
- **Nettoyer** si des exemples deviennent obsolètes

## 🚀 **Prochaines Étapes**

1. **Intégrer** les meilleurs exemples dans `cogs/`
2. **Développer** de nouvelles fonctionnalités basées sur ces patterns
3. **Personnaliser** pour tes jeux spécifiques
