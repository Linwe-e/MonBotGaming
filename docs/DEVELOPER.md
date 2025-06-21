# 🛠️ Guide Développeur - MonBotGaming

## 🏗️ **Architecture du Bot**

### Structure Modulaire
- **main.py** : Point d'entrée, gestion des événements Discord
- **config.py** : Configuration centralisée (jeux, couleurs, channels)
- **cogs/** : Modules fonctionnels (commandes groupées par thème)
- **utils/** : Fonctions utilitaires réutilisables
- **data/** : Stockage JSON des données persistantes

### Pattern de Développement
Inspiré de [Rhodham96/DiscordBot](https://github.com/Rhodham96/DiscordBot/) avec :
- Architecture modulaire avec extensions
- Gestion d'erreurs centralisée  
- Configuration par variables d'environnement
- Utilitaires gaming spécialisés

## 🤖 **IA Gemini Hardcore**

### Configuration
```python
# utils/gemini_ai.py - Prompts optimisés hardcore
HARDCORE_PROMPTS = {
    'vocabulary': 'technical',
    'assume_knowledge': True,
    'provide_numbers': True,
    'advanced_strategies': True
}
```

### Prompts Spécialisés
- **Théorycrafting** : Calculs DPS/EHP, breakpoints
- **Meta Analysis** : Tier lists, optimisations actuelles
- **Technical Language** : Frame data, i-frames, scaling
- **Pro Strategies** : Edge cases, cheese strats

## 📁 **Ajout de Nouveaux Modules**

### 1. Créer un Cog
```python
# cogs/nouveau_module.py
from discord.ext import commands

class NouveauModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ma_commande(self, ctx):
        await ctx.send("Ma réponse")

async def setup(bot):
    await bot.add_cog(NouveauModule(bot))
```

### 2. Charger dans main.py
```python
async def load_cogs():
    await bot.load_extension('cogs.nouveau_module')
```

## 🎮 **Ajout de Nouveaux Jeux**

### 1. Configuration dans config.py
```python
GAMES = {
    'nouveau_jeu': {
        'name': 'Mon Nouveau Jeu',
        'emoji': '🎮',
        'aliases': ['njeu', 'mnj'],
        'categories': ['build', 'team']
    }
}
```

### 2. Support IA dans gemini_ai.py
```python
'game_specific_prompts': {
    'nouveau_jeu': """
    Focus sur :
    - Mécaniques spécifiques du jeu
    - Optimisations meta actuelles
    - Stratégies avancées
    """
}
```

## 📊 **Base de Données JSON**

### Structure des Fichiers
```json
// data/builds.json
{
    "game_id": {
        "build_name": {
            "author": "user_id",
            "description": "...",
            "stats": {...},
            "created_at": "ISO_date"
        }
    }
}
```

### Accès via database.py
```python
from utils.database import db

# Sauvegarder
await db.save_build('diablo4', build_data)

# Récupérer
builds = await db.get_builds_by_game('diablo4')
```

## 🔧 **Utilitaires Gaming**

### gaming_helpers.py
```python
# Création d'embeds stylés
embed = gaming_helpers.create_gaming_embed(
    title="Mon Titre",
    color='success',
    game='diablo4'
)

# Parsing de jeu depuis message
game_id, game_data = gaming_helpers.parse_game_from_message(message)
```

## 🧪 **Tests et Validation**

### Scripts de Test
- `scripts/test_hardcore_ai.py` : Validation prompts IA
- `scripts/test_ai_methods.py` : Tests méthodes individuelles

### Commandes de Debug
```python
# test.py - Bot de test séparé
!test_config    # Vérifier configuration
!test_db        # Tester base de données
!test_ai        # Valider IA
```

## 🚀 **Déploiement**

### Variables d'Environnement
```env
DISCORD_TOKEN=bot_token_here
GEMINI_API_KEY=gemini_key_here
```

### Dépendances
```bash
pip install discord.py python-dotenv google-generativeai
```

## 🎯 **Bonnes Pratiques**

1. **Modularité** : Un cog par fonctionnalité majeure
2. **Configuration** : Tout paramétrer via config.py
3. **Erreurs** : Gestion centralisée avec messages utilisateur
4. **IA** : Prompts spécialisés par contexte gaming
5. **Tests** : Validation avant mise en production
6. **Documentation** : Code commenté et README à jour

## 🔗 **Ressources Utiles**

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Gemini AI API](https://ai.google.dev/docs)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)
- [JSON Data Handling](https://docs.python.org/3/library/json.html)
