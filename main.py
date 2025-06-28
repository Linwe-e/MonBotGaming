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
    # Cogs will be loaded by setup_hook

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
                from utils.ai.gemini_ai import gemini_ai
                from utils.discord_helpers.embed_helpers import create_ai_response_embed, create_gaming_embed
                from utils.ai.smart_response import SmartResponseManager
                from utils.data_management.rgpd_conversation_memory import rgpd_conversation_memory
                from utils.discord_helpers.rgpd_consent_ui import show_consent_request
                
                if gemini_ai.is_available():
                    # Vérifier le consentement RGPD
                    has_consent, consent_data = rgpd_conversation_memory.check_user_consent(message.author.id)
                    
                    # Si pas de consentement, afficher l'interface avec boutons
                    if not has_consent:
                        await show_consent_request(message, bot)
                        return
                    
                    # Ajouter le message de l'utilisateur à la mémoire (si consentement)
                    rgpd_conversation_memory.add_message(message.author.id, content)
                    
                    # Analyser le contexte pour déterminer le type de réponse
                    use_embed, embed_type = SmartResponseManager.should_use_embed(content)
                    
                    # Récupérer le contexte de conversation
                    context_list = rgpd_conversation_memory.get_conversation_context(message.author.id)
                    context = "\n".join(context_list) if context_list else ""
                    
                    # Générer une réponse adaptée selon le type
                    if not use_embed and any(word in content.lower() for word in ['salut', 'bonjour', 'hello', 'hi']):
                        # Salutation simple
                        response = f"Salut {message.author.mention} ! 🎮"
                        await message.reply(response)
                        
                    elif not use_embed:
                        # Question casual → Réponse simple
                        response = await gemini_ai.gaming_assistant(content, game_context=context)
                        
                        # Réponse simple sans embed pour conversations casual
                        if len(response) <= 1500:
                            await message.reply(response)
                        else:
                            await message.reply(response[:1500] + "...")
                            
                    elif embed_type == 'light':
                        # Question gaming légère → Embed simple
                        response = await gemini_ai.gaming_assistant(content, game_context=context)
                        
                        # Embed léger sans fioritures
                        simple_embed = discord.Embed(
                            description=response[:1000] if len(response) <= 1000 else response[:1000] + "...",
                            color=0x00ff88
                        )
                        await message.reply(embed=simple_embed)
                        
                    else:
                        # Question gaming technique → Embed complet
                        response = await gemini_ai.gaming_assistant(content, game_context=context)
                        
                        # Créer un embed de réponse stylé
                        response_embed = create_ai_response_embed(content, response)
                        
                        # Gestion des réponses longues
                        if len(response) <= 1000:
                            response_embed.description = response
                            await message.reply(embed=response_embed)
                        else:
                            # Envoyer la première partie dans l'embed
                            response_embed.description = response[:1000]
                            response_embed.set_footer(text="Suite de la réponse dans les messages suivants...")
                            await message.reply(embed=response_embed)

                            # Envoyer le reste en plusieurs messages si nécessaire
                            remaining_response = response[1000:]
                            for i in range(0, len(remaining_response), 1900):
                                chunk = remaining_response[i:i+1900]
                                await message.channel.send(f"```{chunk}```")
                    
                    # Sauvegarder la réponse du bot (si consentement et si response définie)
                    if 'response' in locals():
                        rgpd_conversation_memory.add_message(
                            message.author.id, 
                            response[:200] + "..." if len(response) > 200 else response, 
                            is_bot=True
                        )
                    
                else:
                    # Simple message d'erreur sans embed pour l'IA indisponible
                    await message.reply("🤖 L'assistant gaming n'est pas disponible pour le moment. Essaie `!ai status` pour plus d'infos.")
                    
            except discord.HTTPException as e:
                print(f"Erreur Discord lors de la mention IA: {e}")
                await message.reply("❌ Une erreur de communication avec Discord est survenue. Veuillez réessayer plus tard.")
            except Exception as e:
                print(f"Erreur inattendue lors de la mention IA: {e}")
                await message.reply("🎮 Oups ! Une erreur inattendue s'est produite. L'assistant gaming est temporairement indisponible. Nous travaillons à résoudre le problème !")
                
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
    """Charge automatiquement tous les cogs disponibles dans le dossier 'cogs'"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Module {filename[:-3]} chargé")
            except Exception as e:
                print(f"⚠️ Erreur chargement du module {filename[:-3]}: {e}")

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
        print("❌ ERREUR: Token Discord manquant ! Assure-toi qu'il est défini dans le fichier .env ou comme variable d'environnement système.")
    else:
        print("🚀 Démarrage du bot...")
        bot.run(token)
