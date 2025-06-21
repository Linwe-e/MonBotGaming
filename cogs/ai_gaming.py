# 🤖 Cog IA Gaming pour MonBotGaming
# Commandes utilisant Gemini AI pour l'assistance gaming

import discord
from discord.ext import commands
import sys
import os

# Ajouter utils au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from config import GAMES
from utils.gaming_helpers import gaming_helpers
from utils.gemini_ai import gemini_ai

class AIGaming(commands.Cog):
    """
    Module IA Gaming - Assistant intelligent pour tes jeux
    Inspiré de l'architecture modulaire de Rhodham96/DiscordBot
    """
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='ai', invoke_without_command=True)
    async def ai_commands(self, ctx):
        """Commandes IA Gaming - !ai help pour voir les options"""
        embed = gaming_helpers.create_gaming_embed(
            title="🤖 Assistant IA Gaming",
            description="Utilise Gemini AI pour t'aider dans tes jeux !",
            color='info'
        )
        
        if not gemini_ai.is_available():
            embed.add_field(
                name="⚠️ Configuration requise",
                value="Configure ta clé Gemini API dans le fichier .env",
                inline=False
            )
        
        commands_text = """
        **!ai ask [question]** - Pose une question gaming
        **!ai build [jeu] [description]** - Analyse un build
        **!ai team [jeu] [activité] [joueurs]** - Composition d'équipe
        **!ai event [jeu] [type] [détails]** - Description d'événement
        **!ai status** - Statut de l'IA
        """
        
        embed.add_field(
            name="📋 Commandes disponibles",
            value=commands_text,
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @ai_commands.command(name='ask')
    async def ai_ask(self, ctx, *, question: str):
        """Pose une question à l'assistant gaming - !ai ask [question]"""
        
        # Détecter le contexte de jeu dans le message
        game_id, game_data = gaming_helpers.parse_game_from_message(question)
        game_context = game_data['name'] if game_data else None
        
        embed = gaming_helpers.create_gaming_embed(
            title="🤖 Assistant Gaming",
            color='info',
            game=game_id if game_data else None
        )
        
        # Afficher la question (avec limite pour éviter les erreurs)
        question_display = question[:900] + "..." if len(question) > 900 else question
        embed.add_field(
            name="❓ Question",
            value=f"```{question_display}```",
            inline=False
        )
        
        # Traitement en cours
        thinking_msg = await ctx.send(embed=embed)
        
        # Générer la réponse
        response = await gemini_ai.gaming_assistant(question, game_context)
        
        # Gestion intelligente des réponses longues
        max_embed_length = 1000  # Marge de sécurité sous la limite Discord de 1024
        
        if len(response) <= max_embed_length:
            # Réponse courte : utiliser l'embed
            embed.add_field(
                name="💡 Réponse IA",
                value=response,
                inline=False
            )
            
            if game_context:
                embed.add_field(
                    name="🎮 Contexte détecté",
                    value=f"{game_data['emoji']} {game_context}",
                    inline=True
                )
            
            await thinking_msg.edit(embed=embed)
        else:
            # Réponse longue : utiliser un message texte séparé
            if game_context:
                embed.add_field(
                    name="🎮 Contexte détecté",
                    value=f"{game_data['emoji']} {game_context}",
                    inline=True
                )
            
            embed.add_field(
                name="💡 Réponse IA",
                value="*Réponse détaillée ci-dessous*",
                inline=False
            )
            
            await thinking_msg.edit(embed=embed)
            
            # Diviser la réponse en chunks si nécessaire (limite Discord : 2000 caractères par message)
            chunks = []
            current_chunk = ""
            
            for line in response.split('\n'):
                if len(current_chunk) + len(line) + 1 > 1900:  # Marge de sécurité
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = line
                else:
                    current_chunk += '\n' + line if current_chunk else line
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Envoyer les chunks
            for i, chunk in enumerate(chunks):
                prefix = f"**Partie {i+1}/{len(chunks)}:**\n" if len(chunks) > 1 else ""
                await ctx.send(f"{prefix}{chunk}")

    @ai_commands.command(name='build')
    async def ai_build(self, ctx, game: str = None, *, description: str = None):
        """Analyse un build pour un jeu - !ai build [jeu] [description]"""
        
        if not description:
            embed = gaming_helpers.create_gaming_embed(
                title="⚠️ Paramètres manquants",
                description="Usage: `!ai build [jeu] [description du build]`",
                color='warning'
            )
            await ctx.send(embed=embed)
            return
        
        game_id, game_data = gaming_helpers.parse_game_from_message(f"{game} {description}")
        
        embed = gaming_helpers.create_gaming_embed(
            title="🔧 Analyse de Build",
            color='info',
            game=game_id if game_data else None
        )
        
        embed.add_field(
            name="📝 Description",
            value=f"```{description}```",
            inline=False
        )
        
        thinking_msg = await ctx.send(embed=embed)
          # Analyser le build
        response = await gemini_ai.analyze_build(description, game or (game_data['name'] if game_data else None))
        
        # Gestion des réponses longues comme pour ai_ask
        max_embed_length = 1000
        
        if len(response) <= max_embed_length:
            embed.add_field(
                name="💡 Analyse IA",
                value=response,
                inline=False
            )
            await thinking_msg.edit(embed=embed)
        else:
            embed.add_field(
                name="💡 Analyse IA",
                value="*Analyse détaillée ci-dessous*",
                inline=False
            )
            await thinking_msg.edit(embed=embed)
            
            # Diviser en chunks
            chunks = []
            current_chunk = ""
            
            for line in response.split('\n'):
                if len(current_chunk) + len(line) + 1 > 1900:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = line
                else:
                    current_chunk += '\n' + line if current_chunk else line
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            for i, chunk in enumerate(chunks):
                prefix = f"**Partie {i+1}/{len(chunks)}:**\n" if len(chunks) > 1 else ""
                await ctx.send(f"{prefix}{chunk}")

    @ai_commands.command(name='team')
    async def ai_team(self, ctx, game: str = None, activity: str = None, *, players: str = None):
        """Composition d'équipe - !ai team [jeu] [activité] [joueurs]"""
        
        if not activity or not players:
            embed = gaming_helpers.create_gaming_embed(
                title="⚠️ Paramètres manquants",
                description="Usage: `!ai team [jeu] [activité] [description des joueurs]`",
                color='warning'
            )
            await ctx.send(embed=embed)
            return
        
        game_id, game_data = gaming_helpers.parse_game_from_message(f"{game} {activity}")
        
        embed = gaming_helpers.create_gaming_embed(
            title="👥 Composition d'Équipe",
            color='info',
            game=game_id if game_data else None
        )
        
        embed.add_field(name="🎯 Activité", value=activity, inline=True)
        embed.add_field(name="👤 Joueurs", value=players, inline=True)
        
        thinking_msg = await ctx.send(embed=embed)
        
        response = await gemini_ai.suggest_team_composition(game or (game_data['name'] if game_data else None), activity, players)
        
        # Gestion des réponses longues
        max_embed_length = 1000
        
        if len(response) <= max_embed_length:
            embed.add_field(
                name="💡 Suggestions IA",
                value=response,
                inline=False
            )
            await thinking_msg.edit(embed=embed)
        else:
            embed.add_field(
                name="💡 Suggestions IA",
                value="*Suggestions détaillées ci-dessous*",
                inline=False
            )
            await thinking_msg.edit(embed=embed)
            
            # Diviser en chunks
            chunks = []
            current_chunk = ""
            
            for line in response.split('\n'):
                if len(current_chunk) + len(line) + 1 > 1900:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = line
                else:
                    current_chunk += '\n' + line if current_chunk else line
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            for i, chunk in enumerate(chunks):
                prefix = f"**Partie {i+1}/{len(chunks)}:**\n" if len(chunks) > 1 else ""
                await ctx.send(f"{prefix}{chunk}")

    @ai_commands.command(name='event')
    async def ai_event(self, ctx, game: str = None, event_type: str = None, *, details: str = None):
        """Description d'événement gaming - !ai event [jeu] [type] [détails]"""
        
        if not event_type:
            embed = gaming_helpers.create_gaming_embed(
                title="⚠️ Paramètres manquants",
                description="Usage: `!ai event [jeu] [type] [détails]`",
                color='warning'
            )
            await ctx.send(embed=embed)
            return
        
        game_id, game_data = gaming_helpers.parse_game_from_message(f"{game} {event_type}")
        
        embed = gaming_helpers.create_gaming_embed(
            title="🎉 Événement Gaming",
            color='info',
            game=game_id if game_data else None
        )
        
        embed.add_field(name="📅 Type", value=event_type, inline=True)
        if details:
            embed.add_field(name="📝 Détails", value=details[:500], inline=False)
        
        thinking_msg = await ctx.send(embed=embed)
        
        response = await gemini_ai.generate_event_description(game or (game_data['name'] if game_data else None), event_type, {'title': details} if details else {})
        
        # Gestion des réponses longues
        max_embed_length = 1000
        
        if len(response) <= max_embed_length:
            embed.add_field(
                name="💡 Description IA",
                value=response,
                inline=False
            )
            await thinking_msg.edit(embed=embed)
        else:
            embed.add_field(
                name="💡 Description IA",
                value="*Description détaillée ci-dessous*",
                inline=False
            )
            await thinking_msg.edit(embed=embed)
            
            # Diviser en chunks
            chunks = []
            current_chunk = ""
            
            for line in response.split('\n'):
                if len(current_chunk) + len(line) + 1 > 1900:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = line
                else:
                    current_chunk += '\n' + line if current_chunk else line
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            for i, chunk in enumerate(chunks):
                prefix = f"**Partie {i+1}/{len(chunks)}:**\n" if len(chunks) > 1 else ""
                await ctx.send(f"{prefix}{chunk}")

    @ai_commands.command(name='status')
    async def ai_status(self, ctx):
        """Afficher le statut de l'IA"""
        embed = gaming_helpers.create_gaming_embed(
            title="🤖 Statut de l'IA",
            color='info'
        )
        
        if gemini_ai.is_available():
            embed.add_field(
                name="✅ Statut",
                value="Gemini AI connecté et prêt",
                inline=False
            )
            embed.add_field(
                name="🔧 Modèle",
                value="gemini-2.0-flash-exp (Gratuit)",
                inline=True
            )
            embed.add_field(
                name="🎮 Spécialisation",
                value="Assistant Gaming",
                inline=True
            )
        else:
            embed.add_field(
                name="❌ Statut",
                value="IA non configurée",
                inline=False
            )
            embed.add_field(
                name="⚙️ Configuration",
                value="Ajoute ta clé Gemini dans .env",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Fonction setup pour charger le cog"""
    await bot.add_cog(AIGaming(bot))
