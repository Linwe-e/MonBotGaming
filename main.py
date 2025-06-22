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

@bot.event
async def on_message(message):
    """Gestionnaire pour les mentions directes du bot"""
    # Ignorer les messages du bot lui-même
    if message.author == bot.user:
        return
    
    # Vérifier si le bot est mentionné
    if bot.user in message.mentions:
        # Extraire le contenu du message sans la mention
        content = message.content
        # Supprimer la mention du bot du message
        for mention in message.mentions:
            if mention == bot.user:
                content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
        
        content = content.strip()
        
        # Si il y a du contenu après la mention, traiter comme une question IA
        if content:
            try:
                from utils.gemini_ai import gemini_ai
                from utils.embed_helpers import create_ai_response_embed, create_gaming_embed
                
                if gemini_ai.is_available():
                    # Détecter le type de message
                    message_type = gemini_ai._detect_message_type(content)
                    
                    # Générer une réponse adaptée selon le type
                    if 'greeting' in message_type.lower() or any(word in content.lower() for word in ['salut', 'bonjour', 'hello', 'hi']):
                        # Embed de salutation stylé
                        greeting_embed = create_gaming_embed(
                            title=f"🎮 Salut {message.author.name} !",
                            description="Prêt pour du gaming hardcore ? Je peux t'aider avec tes builds, stratégies, ou n'importe quelle question gaming ! 😄",
                            color='gaming'
                        )
                        greeting_embed.add_field(
                            name="💡 Astuce",
                            value="Tu peux aussi utiliser `!ai help` pour voir toutes mes commandes !",
                            inline=False
                        )
                        await message.reply(embed=greeting_embed)
                    else:
                        # Utiliser l'assistant gaming pour les questions techniques
                        response = await gemini_ai.gaming_assistant(content)
                        
                        # Créer un embed de réponse stylé
                        response_embed = create_ai_response_embed(content, response)
                        
                        # Gestion des réponses longues
                        if len(response) <= 1000:
                            await message.reply(embed=response_embed)
                        else:
                            # Embed + messages additionnels pour les réponses longues
                            await message.reply(embed=response_embed)
                            remaining = response[1000:]
                            while remaining:
                                chunk = remaining[:1900]
                                remaining = remaining[1900:]
                                await message.channel.send(f"```{chunk}```")
                else:
                    # Embed d'erreur stylé
                    error_embed = create_gaming_embed(
                        title="🤖 IA Temporairement Indisponible",
                        description="L'assistant gaming n'est pas disponible pour le moment.",
                        color='warning'
                    )
                    error_embed.add_field(
                        name="🔧 Solution",
                        value="Essaie `!ai status` pour plus d'infos sur la configuration.",
                        inline=False
                    )
                    await message.reply(embed=error_embed)
            except Exception as e:
                print(f"Erreur mention IA: {e}")
                # Embed d'erreur simple
                fallback_embed = create_gaming_embed(
                    title="🎮 Salut ! Je suis là pour t'aider !",
                    description="Une petite erreur s'est produite, mais je reste disponible !",
                    color='info'
                )
                fallback_embed.add_field(
                    name="🎯 Commandes disponibles",
                    value="Utilise `!ai help` pour voir mes commandes gaming !",
                    inline=False
                )
                await message.reply(embed=fallback_embed)
        else:
            # Mention sans contenu = salutation simple avec embed
            simple_greeting = create_gaming_embed(
                title=f"🎮 Salut {message.author.name} !",
                description="Comment puis-je t'aider avec tes jeux ? 😄",
                color='gaming'
            )
            simple_greeting.add_field(
                name="💬 Utilisation",
                value="Pose-moi une question ou utilise `!ai help` pour voir mes commandes !",
                inline=False
            )
            await message.reply(embed=simple_greeting)
    
    # Traiter les commandes normales
    await bot.process_commands(message)

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
