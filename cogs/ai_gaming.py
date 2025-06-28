# 🤖 Cog IA Gaming pour MonBotGaming - Version Embeds Riches
# Commandes utilisant Gemini AI pour l'assistance gaming

import discord
from discord.ext import commands
import sys
import os

# Ajouter utils au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from config import GAMES
from utils.discord_helpers.gaming_helpers import gaming_helpers
from utils.ai.gemini_ai import gemini_ai
from utils.discord_helpers.embed_helpers import create_ai_response_embed, create_gaming_embed, create_help_embed, create_status_embed

class AIGaming(commands.Cog):
    """
    Module IA Gaming - Assistant intelligent pour tes jeux
    Avec interface embeds riches pour une meilleure UX
    """
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='ai', invoke_without_command=True)
    async def ai_commands(self, ctx):
        """Commandes IA Gaming - !ai help pour voir les options"""
        
        # Créer un embed d'aide stylé
        commands_list = {
            "!ai ask [question]": "Pose une question gaming",
            "!ai build [jeu] [description]": "Analyse un build",
            "!ai team [jeu] [activité] [joueurs]": "Composition d'équipe",
            "!ai event [jeu] [type] [détails]": "Description d'événement",
            "!ai status": "Statut de l'IA"
        }
        
        embed = create_help_embed(commands_list, "Assistant IA Gaming")
        
        if not gemini_ai.is_available():
            embed.add_field(
                name="⚠️ Configuration requise",
                value="Configure ta clé Gemini API dans le fichier .env",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @ai_commands.command(name='ask')
    async def ai_ask(self, ctx, *, question: str):
        """Pose une question à l'assistant gaming - !ai ask [question]"""
        
        if not gemini_ai.is_available():
            embed = create_status_embed("Gemini AI", False, "Clé API non configurée")
            await ctx.send(embed=embed)
            return
        
        # Détecter le contexte de jeu dans le message
        game_id, game_data = gaming_helpers.parse_game_from_message(question)
        game_context = game_data['name'] if game_data else None
        
        # Message de traitement avec embed stylé
        thinking_embed = create_gaming_embed(
            title="🤖 MonBotGaming AI - En réflexion...",
            description="🧠 Analyse de votre question gaming en cours...",
            color='info'
        )
        thinking_msg = await ctx.send(embed=thinking_embed)
        
        try:
            # Générer la réponse
            response = await gemini_ai.gaming_assistant(question, game_context)
            
            # Créer l'embed de réponse stylé avec les nouvelles fonctions
            response_embed = create_ai_response_embed(question, response, game_context)
            
            # Gestion des réponses longues
            if len(response) <= 1000:
                # Réponse courte : tout dans l'embed
                await thinking_msg.edit(embed=response_embed)
            else:
                # Réponse longue : embed + messages additionnels
                await thinking_msg.edit(embed=response_embed)
                
                # Envoyer le reste en chunks
                remaining = response[1000:]
                while remaining:
                    chunk = remaining[:1900]  # Limite Discord 2000 chars
                    remaining = remaining[1900:]
                    await ctx.send(f"```{chunk}```")
                    
        except Exception as e:
            error_embed = create_gaming_embed(
                title="❌ Erreur IA",
                description=f"Une erreur s'est produite : {str(e)}",
                color='error'
            )
            await thinking_msg.edit(embed=error_embed)
    
    @ai_commands.command(name='build')
    async def ai_build(self, ctx, game: str = None, *, description: str = None):
        """Analyse un build pour un jeu - !ai build [jeu] [description]"""
        
        if not description:
            embed = create_gaming_embed(
                title="⚠️ Paramètres manquants",
                description="Usage: `!ai build [jeu] [description du build]`",
                color='warning'
            )
            await ctx.send(embed=embed)
            return
        
        if not gemini_ai.is_available():
            embed = create_status_embed("Gemini AI", False, "Clé API non configurée")
            await ctx.send(embed=embed)
            return
        
        # Détecter le jeu
        game_id, game_data = gaming_helpers.parse_game_from_message(f"{game} {description}")
        
        # Embed de traitement
        thinking_embed = create_gaming_embed(
            title="🔧 Analyse de Build en cours...",
            description=f"🎮 Jeu: {game or 'Auto-détecté'}\n📝 Build: {description[:100]}...",
            color='info'
        )
        thinking_msg = await ctx.send(embed=thinking_embed)
        
        try:
            # Analyser le build
            response = await gemini_ai.analyze_build(description, game or (game_data['name'] if game_data else None))
            
            # Créer embed de réponse
            response_embed = create_ai_response_embed(f"Analyse build: {description[:50]}...", response, game_data['name'] if game_data else game)
            
            # Gestion réponses longues
            if len(response) <= 1000:
                await thinking_msg.edit(embed=response_embed)
            else:
                await thinking_msg.edit(embed=response_embed)
                
                # Chunks pour le reste
                remaining = response[1000:]
                while remaining:
                    chunk = remaining[:1900]
                    remaining = remaining[1900:]
                    await ctx.send(f"```{chunk}```")
                    
        except Exception as e:
            error_embed = create_gaming_embed(
                title="❌ Erreur Analyse Build",
                description=f"Impossible d'analyser le build : {str(e)}",
                color='error'
            )
            await thinking_msg.edit(embed=error_embed)
    
    @ai_commands.command(name='team')
    async def ai_team(self, ctx, game: str = None, activity: str = None, *, players: str = None):
        """Composition d'équipe - !ai team [jeu] [activité] [joueurs]"""
        
        if not activity or not players:
            embed = create_gaming_embed(
                title="⚠️ Paramètres manquants",
                description="Usage: `!ai team [jeu] [activité] [description des joueurs]`",
                color='warning'
            )
            await ctx.send(embed=embed)
            return
        
        if not gemini_ai.is_available():
            embed = create_status_embed("Gemini AI", False)
            await ctx.send(embed=embed)
            return
        
        # Détecter le jeu
        game_id, game_data = gaming_helpers.parse_game_from_message(f"{game} {activity}")
        
        # Embed de traitement
        thinking_embed = create_gaming_embed(
            title="👥 Analyse d'Équipe en cours...",
            description=f"🎮 Jeu: {game or 'Auto-détecté'}\n🎯 Activité: {activity}\n👤 Joueurs: {players[:50]}...",
            color='info'
        )
        thinking_msg = await ctx.send(embed=thinking_embed)
        
        try:
            response = await gemini_ai.suggest_team_composition(game or (game_data['name'] if game_data else None), activity, players)
            
            response_embed = create_ai_response_embed(f"Composition équipe pour {activity}", response, game_data['name'] if game_data else game)
            
            if len(response) <= 1000:
                await thinking_msg.edit(embed=response_embed)
            else:
                await thinking_msg.edit(embed=response_embed)
                remaining = response[1000:]
                while remaining:
                    chunk = remaining[:1900]
                    remaining = remaining[1900:]
                    await ctx.send(f"```{chunk}```")
                    
        except Exception as e:
            error_embed = create_gaming_embed(
                title="❌ Erreur Composition Équipe",
                description=f"Impossible de générer la composition : {str(e)}",
                color='error'
            )
            await thinking_msg.edit(embed=error_embed)
    
    @ai_commands.command(name='event')
    async def ai_event(self, ctx, game: str = None, event_type: str = None, *, details: str = None):
        """Description d'événement gaming - !ai event [jeu] [type] [détails]"""
        
        if not event_type:
            embed = create_gaming_embed(
                title="⚠️ Paramètres manquants",
                description="Usage: `!ai event [jeu] [type] [détails]`",
                color='warning'
            )
            await ctx.send(embed=embed)
            return
        
        if not gemini_ai.is_available():
            embed = create_status_embed("Gemini AI", False)
            await ctx.send(embed=embed)
            return
        
        # Détecter le jeu
        game_id, game_data = gaming_helpers.parse_game_from_message(f"{game} {event_type}")
        
        # Embed de traitement
        thinking_embed = create_gaming_embed(
            title="🎉 Génération Événement en cours...",
            description=f"🎮 Jeu: {game or 'Auto-détecté'}\n📅 Type: {event_type}",
            color='info'
        )
        thinking_msg = await ctx.send(embed=thinking_embed)
        
        try:
            response = await gemini_ai.generate_event_description(game or (game_data['name'] if game_data else None), event_type, {'title': details} if details else {})
            
            response_embed = create_ai_response_embed(f"Événement {event_type}", response, game_data['name'] if game_data else game)
            
            if len(response) <= 1000:
                await thinking_msg.edit(embed=response_embed)
            else:
                await thinking_msg.edit(embed=response_embed)
                remaining = response[1000:]
                while remaining:
                    chunk = remaining[:1900]
                    remaining = remaining[1900:]
                    await ctx.send(f"```{chunk}```")
                    
        except Exception as e:
            error_embed = create_gaming_embed(
                title="❌ Erreur Génération Événement",
                description=f"Impossible de générer l'événement : {str(e)}",
                color='error'
            )
            await thinking_msg.edit(embed=error_embed)
    
    @ai_commands.command(name='status')
    async def ai_status(self, ctx):
        """Afficher le statut de l'IA avec embed stylé"""
        
        is_available = gemini_ai.is_available()
        
        if is_available:
            embed = create_status_embed("Gemini AI", True, "Assistant Gaming prêt à répondre")
            embed.add_field(
                name="🔧 Modèle",
                value="gemini-2.0-flash (Gratuit)",
                inline=True
            )
            embed.add_field(
                name="🎮 Spécialisation",
                value="Gaming hardcore & builds",
                inline=True
            )
            embed.add_field(
                name="📊 Fonctionnalités",
                value="• Questions gaming\n• Analyse builds\n• Compo équipes\n• Événements",
                inline=False
            )
        else:
            embed = create_status_embed("Gemini AI", False, "Clé API non configurée")
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Fonction setup pour charger le cog"""
    await bot.add_cog(AIGaming(bot))
