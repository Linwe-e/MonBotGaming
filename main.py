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
                from utils.smart_response import SmartResponseManager
                from utils.conversation_memory import conversation_memory
                
                if gemini_ai.is_available():
                    # Ajouter le message de l'utilisateur à la mémoire
                    conversation_memory.add_message(message.author.id, content)
                    
                    # Analyser le contexte pour déterminer le type de réponse
                    use_embed, embed_type = SmartResponseManager.should_use_embed(content)
                    
                    # Récupérer le contexte de conversation
                    context = conversation_memory.format_context_for_ai(message.author.id)
                    
                    # Générer une réponse adaptée selon le type
                    if not use_embed and any(word in content.lower() for word in ['salut', 'bonjour', 'hello', 'hi']):
                        # Salutation simple
                        await message.reply(f"Salut {message.author.mention} ! 🎮")
                        
                    elif not use_embed:
                        # Question casual → Réponse simple
                        response = await gemini_ai.gaming_assistant(content, context=context)
                        
                        # Réponse simple sans embed pour conversations casual
                        if len(response) <= 1500:
                            await message.reply(response)
                        else:
                            await message.reply(response[:1500] + "...")
                            
                    elif embed_type == 'light':
                        # Question gaming légère → Embed simple
                        response = await gemini_ai.gaming_assistant(content, context=context)
                        
                        # Embed léger sans fioritures
                        simple_embed = discord.Embed(
                            description=response[:1000] if len(response) <= 1000 else response[:1000] + "...",
                            color=0x00ff88
                        )
                        await message.reply(embed=simple_embed)
                        
                    else:
                        # Question gaming technique → Embed complet
                        response = await gemini_ai.gaming_assistant(content, context=context)
                        
                        # Créer un embed de réponse stylé
                        response_embed = create_ai_response_embed(content, response)
                        
                        # Gestion des réponses longues
                        if len(response) <= 1000:
                            await message.reply(embed=response_embed)
                        else:
                            await message.reply(embed=response_embed)
                            remaining = response[1000:]
                            while remaining:
                                chunk = remaining[:1900]
                                remaining = remaining[1900:]
                                await message.channel.send(f"```{chunk}```")                    
                    # Sauvegarder la réponse du bot
                    conversation_memory.add_message(message.author.id, response[:200] + "..." if len(response) > 200 else response, is_bot=True)
                    
                else:
                    # Simple message d'erreur sans embed pour l'IA indisponible
                    await message.reply("🤖 L'assistant gaming n'est pas disponible pour le moment. Essaie `!ai status` pour plus d'infos.")
                    
            except Exception as e:
                print(f"Erreur mention IA: {e}")
                # Message d'erreur simple et friendly
                await message.reply("🎮 Salut ! Une petite erreur s'est produite, mais je reste disponible ! Utilise `!ai help` pour voir mes commandes gaming !")
                
        else:
            # Mention sans contenu = salutation simple SANS embed
            await message.reply(f"🎮 Salut {message.author.mention} ! Besoin d'aide gaming ?")
    
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
