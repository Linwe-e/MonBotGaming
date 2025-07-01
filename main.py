import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv

# Ajouter le dossier utils au path Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.dirname(__file__))

# Charger les variables secrètes
load_dotenv()

# Importer nos configurations et utilitaires
from config import BOT_CONFIG
from utils.ai.gemini_ai import gemini_ai
from utils.discord_helpers.embed_helpers import send_ai_response
from utils.ai.smart_response import SmartResponseManager
from utils.data_management.rgpd_conversation_memory import rgpd_conversation_memory
from utils.discord_helpers.rgpd_consent_ui import show_consent_request

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
    print(f"[DEBUG] on_message triggered: author={message.author}, content='{message.content}'")
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
        print(f"[DEBUG] Bot mention detected. Content after mention strip: '{content}'")
        # Si il y a du contenu après la mention, traiter comme une question IA
        if content:
            try:
                if gemini_ai.is_available():
                    # Vérifier le consentement RGPD
                    has_consent, _ = rgpd_conversation_memory.check_user_consent(message.author.id)
                    
                    # Si pas de consentement, vérifier si on doit demander ou traiter sans mémoire
                    if not has_consent:
                        # On crée un contexte "artificiel" pour pouvoir envoyer un message éphémère
                        ctx = await bot.get_context(message)
                        consent_requested = await show_consent_request(ctx, bot, message)
                        
                        # Si on n'a pas pu/voulu demander le consentement (refus récent), 
                        # traiter la question SANS mémoire
                        if not consent_requested:
                            # Traiter la question sans mémoire conversationnelle
                            print(f"[DEBUG] Traitement sans mémoire pour utilisateur ayant refusé: '{content}'")
                            
                            # Analyser le contexte pour déterminer le type de réponse
                            use_embed, embed_type = SmartResponseManager.should_use_embed(content)
                            
                            # Générer une réponse IA SANS contexte
                            response = await gemini_ai.gaming_assistant(content, game_context="")
                            
                            # Utiliser la fonction centralisée pour envoyer la réponse
                            await send_ai_response(message, content, response, use_embed, embed_type)
                        
                        return
                    
                    # Ajouter le message de l'utilisateur à la mémoire (si consentement)
                    rgpd_conversation_memory.add_message(message.author.id, content)
                    
                    print(f"[DEBUG] About to call SmartResponseManager.should_use_embed with content: '{content}'")
                    # Analyser le contexte pour déterminer le type de réponse
                    use_embed, embed_type = SmartResponseManager.should_use_embed(content)
                    print(f"[DEBUG] should_use_embed: use_embed={use_embed}, embed_type={embed_type}, content='{content}'")
                    
                    # Récupérer le contexte de conversation
                    context_list = rgpd_conversation_memory.get_conversation_context(message.author.id)
                    context = "\n".join(context_list) if context_list else ""
                    
                    # Générer une réponse adaptée selon le type
                    if not use_embed and any(word in content.lower() for word in ['salut', 'bonjour', 'hello', 'hi']):
                        # Salutation simple
                        response = f"Salut {message.author.mention} ! 🎮"
                        await message.reply(response)
                        
                    elif embed_type == 'privacy_info':
                        print(f"[DEBUG] Bloc RGPD activé pour: {content}")
                        privacy_response = (
                            f"[MBG-RGPD] Salut {message.author.mention} ! Je suis là pour t'aider avec tes questions gaming. "
                            "Concernant tes données et ta confidentialité, voici comment je fonctionne:\n\n"
                            "**Consentement RGPD :** Je ne stocke tes conversations et ton consentement que si tu as explicitement donné ton accord via notre système RGPD. "
                            "Ceci est fait pour améliorer la pertinence de mes réponses en me souvenant du contexte de nos échanges.\n\n"
                            "**Données stockées :** Je garde une trace de ton consentement et un historique anonymisé de nos conversations. "
                            "Je ne stocke aucune information personnelle identifiable (comme ton nom Discord, ton adresse e-mail, etc.). "
                            "Tes identifiants de jeu ou autres informations sensibles ne sont jamais enregistrés.\n\n"
                            "**Gestion de tes données :** Tu peux vérifier ton statut de consentement ou demander la suppression de tes données de conversation à tout moment. "
                            "Utilise les commandes dédiées pour cela (par exemple, `!rgpd status` pour voir ton consentement, ou `!rgpd delete` pour supprimer tes données).\n\n"
                            "Mon objectif est de t'offrir la meilleure assistance gaming tout en respectant ta vie privée. 🎮"
                        )
                        await message.reply(privacy_response)
                        return

                    else:
                        # Questions gaming et autres → Utiliser la fonction centralisée
                        response = await gemini_ai.gaming_assistant(content, game_context=context)
                        await send_ai_response(message, content, response, use_embed, embed_type, context)
                    
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
