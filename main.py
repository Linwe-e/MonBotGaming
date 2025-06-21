import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv

# Ajouter le dossier utils au path Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Charger les variables secrètes
load_dotenv()

# Importer nos configurations et utilitaires
from config import BOT_CONFIG, GAMES
from utils.database import db
from utils.gaming_helpers import gaming_helpers

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_CONFIG['prefix'], intents=intents)

@bot.event
async def on_ready():
    print(f'🎮 {bot.user} est connecté et prêt à gaming!')
    print(f'📊 Connecté à {len(bot.guilds)} serveur(s)')

async def setup_hook():
    """Hook d'initialisation asynchrone pour charger les cogs"""
    await load_cogs()

bot.setup_hook = setup_hook

@bot.command()
async def hello(ctx):
    await ctx.send(f'Salut **{ctx.author.name}** ! 🎮 Prêt pour du gaming ?')

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latence: {latency}ms')

# Charger les cogs (modules)
async def load_cogs():
    """Charge automatiquement tous les cogs disponibles"""
    try:
        await bot.load_extension('cogs.ai_gaming')
        print("✅ Module IA Gaming chargé")
    except Exception as e:
        print(f"⚠️ Erreur chargement IA Gaming: {e}")

# Gestion des erreurs
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Commande inconnue ! Tape `!help` pour voir les commandes disponibles.")
    else:
        print(f"Erreur: {error}")

# Lancer le bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERREUR: Token Discord manquant dans le fichier .env!")
    else:
        print("🚀 Démarrage du bot...")
        bot.run(token)
