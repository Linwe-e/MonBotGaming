# 🧪 Tests pour MonBotGaming
# Fichier de test séparé pour valider nos fonctionnalités

import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv

# Ajouter le dossier parent au path Python pour importer depuis utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Charger les variables secrètes
load_dotenv()

# Importer nos configurations et utilitaires
from config import BOT_CONFIG, GAMES
from utils.database import db
from utils.gaming_helpers import gaming_helpers

# Configuration du bot de test
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

test_bot = commands.Bot(command_prefix='!test_', intents=intents)

@test_bot.event
async def on_ready():
    print(f'🧪 Bot de test {test_bot.user} est connecté!')
    print(f'📊 Mode TEST activé sur {len(test_bot.guilds)} serveur(s)')

@test_bot.command(name='config')
async def test_config(ctx):
    """Test de la configuration - affiche les jeux configurés"""
    embed = gaming_helpers.create_gaming_embed(
        title="🧪 Test Configuration",
        description=f"**{len(GAMES)} jeux configurés**",
        color='info'
    )
    
    # Afficher quelques jeux en exemple
    games_sample = list(GAMES.items())[:5]  # 5 premiers jeux
    games_text = "\n".join([f"{data['emoji']} **{data['name']}** ({data['category']})" 
                           for _, data in games_sample])
    
    embed.add_field(
        name="📋 Aperçu des jeux",
        value=games_text + f"\n\n*... et {len(GAMES) - 5} autres !*",
        inline=False
    )
    
    # Test de reconnaissance de jeux
    test_message = "J'adore jouer à tarkov et diablo"
    game_id, game_data = gaming_helpers.parse_game_from_message(test_message)
    
    if game_data:
        embed.add_field(
            name="🔍 Test reconnaissance",
            value=f"Message: '{test_message}'\n"
                  f"Jeu détecté: {game_data['emoji']} **{game_data['name']}**",
            inline=False
        )
    
    await ctx.send(embed=embed)

@test_bot.command(name='db')
async def test_database(ctx):
    """Test de la base de données"""
    embed = gaming_helpers.create_gaming_embed(
        title="💾 Test Base de Données",
        color='success'
    )
    
    # Test de lecture des fichiers
    builds_data = db.load_data('builds.json')
    events_data = db.load_data('events.json')
    users_data = db.load_data('users.json')
    
    embed.add_field(
        name="✅ Statut des fichiers",
        value=f"📊 builds.json: **OK** (v{builds_data.get('version', '?')})\n"
              f"📅 events.json: **OK** (v{events_data.get('version', '?')})\n"
              f"👥 users.json: **OK** (v{users_data.get('version', '?')})",
        inline=False
    )
    
    # Test d'écriture/lecture
    test_data = {
        'test': True,
        'timestamp': 'test_run',
        'version': '1.0'
    }
    
    success = db.save_data('test_temp.json', test_data)
    if success:
        loaded_data = db.load_data('test_temp.json')
        embed.add_field(
            name="🔄 Test écriture/lecture",
            value="✅ Sauvegarde: **OK**\n✅ Chargement: **OK**",
            inline=True
        )
    else:
        embed.add_field(
            name="🔄 Test écriture/lecture",
            value="❌ Erreur lors du test",
            inline=True
        )
    
    await ctx.send(embed=embed)

@test_bot.command(name='loot')
async def test_loot(ctx, game=None):
    """Test du générateur de loot - !test_loot [jeu]"""
    if not game:
        game = 'diablo_4'  # Par défaut
    
    embed = gaming_helpers.create_gaming_embed(
        title="🎁 Test Générateur de Loot",
        color='fun',
        game=game
    )
    
    # Générer plusieurs objets pour tester
    loots = []
    for _ in range(3):
        loot = gaming_helpers.generate_loot_item(game)
        loots.append(loot)
    
    # Couleur selon la rareté
    rarity_colors = {
        'common': '⚪',
        'uncommon': '🟢', 
        'rare': '🔵',
        'epic': '🟣',
        'legendary': '🟡'
    }
    
    loot_text = ""
    for i, loot in enumerate(loots, 1):
        rarity_emoji = rarity_colors.get(loot['rarity'], '⚪')
        loot_text += f"{i}. {rarity_emoji} **{loot['name']}** ({loot['rarity']})\n"
    
    embed.add_field(
        name="🎯 Objets générés",
        value=loot_text,
        inline=False
    )
    
    # Test avec jeu spécifique
    if game in ['diablo_4', 'escape_from_tarkov']:
        embed.add_field(
            name="✅ Template spécifique",
            value=f"Utilise le template pour **{game}**",
            inline=True
        )
    else:
        embed.add_field(
            name="ℹ️ Template par défaut",
            value="Utilise le template Diablo par défaut",
            inline=True
        )
    
    await ctx.send(embed=embed)

@test_bot.command(name='dice')
async def test_dice(ctx, sides: int = 20, count: int = 1):
    """Test des dés - !test_dice [faces] [nombre]"""
    result = gaming_helpers.roll_dice(sides, count)
    
    embed = gaming_helpers.create_gaming_embed(
        title="🎲 Test Lancer de Dés",
        color='fun'
    )
    
    # Affichage des résultats
    rolls_text = " + ".join(map(str, result['rolls']))
    if len(result['rolls']) > 1:
        rolls_text += f" = **{result['total']}**"
    
    embed.add_field(
        name=f"🎯 {count}d{sides}",
        value=f"Résultat: {rolls_text}\n"
              f"📊 Moyenne: {result['average']:.1f}",
        inline=False
    )
    
    # Test des limites
    embed.add_field(
        name="ℹ️ Validation",
        value=f"Faces autorisées: {sides in [4, 6, 8, 10, 12, 20, 100]}\n"
              f"Nombre autorisé: {1 <= count <= 10}",
        inline=True
    )
    
    await ctx.send(embed=embed)

@test_bot.command(name='embed')
async def test_embed(ctx, game=None):
    """Test des embeds stylés - !test_embed [jeu]"""
    
    # Test embed basique
    embed1 = gaming_helpers.create_gaming_embed(
        title="Test Embed Basique",
        description="Ceci est un test d'embed sans jeu spécifique",
        color='info'
    )
    
    await ctx.send(embed=embed1)
    
    # Test embed avec jeu
    if game:
        if game in GAMES:
            embed2 = gaming_helpers.create_gaming_embed(
                title="Test Embed avec Jeu",
                description=f"Embed spécialisé pour {GAMES[game]['name']}",
                color='gaming',
                game=game
            )
            await ctx.send(embed=embed2)
        else:
            await ctx.send(f"❌ Jeu '{game}' non trouvé. Jeux disponibles: {', '.join(list(GAMES.keys())[:5])}...")

@test_bot.command(name='all')
async def test_all(ctx):
    """Lance tous les tests rapidement"""
    await ctx.send("🧪 **Lancement de tous les tests...**")
    
    # Test config
    await test_config(ctx)
    await ctx.send("✅ Test config terminé\n")
    
    # Test database
    await test_database(ctx)
    await ctx.send("✅ Test database terminé\n")
    
    # Test loot
    await test_loot(ctx, 'diablo_4')
    await ctx.send("✅ Test loot terminé\n")
      # Test dice
    await test_dice(ctx, 20, 2)
    await ctx.send("✅ Test dice terminé\n")
    
    # Test AI Gemini 2.0
    await test_ai(ctx)
    await ctx.send("✅ Test IA terminé\n")
    
    await ctx.send("🎉 **Tous les tests terminés !**")

@test_bot.command(name='commands')
async def test_commands(ctx):
    """Affiche l'aide des commandes de test"""
    embed = gaming_helpers.create_gaming_embed(
        title="🧪 Commandes de Test",
        description="Préfixe: `!test_`",
        color='info'
    )
    
    commands_text = """
    **config** - Test la configuration des jeux
    **db** - Test la base de données
    **loot [jeu]** - Test le générateur de loot
    **dice [faces] [nombre]** - Test les dés
    **embed [jeu]** - Test les embeds stylés
    **ai** - Test Gemini 2.0 Flash IA
    **all** - Lance tous les tests
    **commands** - Affiche cette aide
    """
    
    embed.add_field(
        name="📋 Commandes disponibles",
        value=commands_text,
        inline=False
    )
    
    await ctx.send(embed=embed)

@test_bot.command(name='ai')
async def test_ai(ctx):
    """Test des fonctionnalités IA avec Gemini 2.0"""
    from utils.gemini_ai import gemini_ai
    
    embed = gaming_helpers.create_gaming_embed(
        title="🤖 Test Gemini 2.0 Flash",
        color='info'
    )
    
    # Test de disponibilité
    if gemini_ai.is_available():
        embed.add_field(
            name="✅ Statut",
            value="Gemini 2.0 Flash configuré et fonctionnel !",
            inline=False
        )
        
        # Message de test en cours
        thinking_msg = await ctx.send(embed=embed)
        
        # Test simple avec reconnaissance de contexte
        test_response = await gemini_ai.gaming_assistant(
            "Donne-moi un conseil rapide pour débuter à Diablo 4", 
            "Diablo IV"
        )
        
        # Mettre à jour avec la réponse
        embed.add_field(
            name="🧪 Test Assistant Gaming",
            value=test_response[:300] + "..." if len(test_response) > 300 else test_response,
            inline=False
        )
        
        # Test du générateur de build
        try:
            build_analysis = await gemini_ai.analyze_build(
                "Diablo IV", 
                "Nécromancien Blood Surge avec Army of the Dead"
            )
            embed.add_field(
                name="🛠️ Test Analyse Build",
                value=build_analysis[:200] + "..." if len(build_analysis) > 200 else build_analysis,
                inline=False
            )
        except Exception as e:
            embed.add_field(
                name="⚠️ Test Analyse Build",
                value=f"Test échoué: {str(e)[:100]}",
                inline=False
            )
        
        await thinking_msg.edit(embed=embed)
        
    else:
        embed.add_field(
            name="❌ Non configuré",
            value="Configure ta clé Gemini API dans .env\n"
                  "1. Va sur [Google AI Studio](https://makersuite.google.com/app/apikey)\n"
                  "2. Crée une clé API\n"
                  "3. Ajoute-la dans .env : `GEMINI_API_KEY=ta_cle`",
            inline=False
        )
        await ctx.send(embed=embed)

# Gestion des erreurs
@test_bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Commande de test inconnue ! Tape `!test_commands` pour voir les commandes disponibles.")
    else:
        print(f"Erreur de test: {error}")
        await ctx.send(f"❌ Erreur lors du test: {error}")

# Lancer le bot de test
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERREUR: Token Discord manquant dans le fichier .env!")
    else:
        print("🧪 Démarrage du bot de test...")
        test_bot.run(token)
