# 🔒 Privacy Commands pour MonBotGaming - Conformité RGPD
# Commandes de gestion des données personnelles et consentements

import discord
from discord.ext import commands
import sys
import os

# Ajouter utils au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

import io
from datetime import datetime, timedelta
from utils.data_management.rgpd_conversation_memory import rgpd_conversation_memory
from utils.discord_helpers.embed_helpers import create_gaming_embed
from config import RGPD_CONFIG

class PrivacyCommands(commands.Cog):
    """
    Module de gestion de la confidentialité et RGPD
    Permet aux utilisateurs de gérer leurs données personnelles
    """    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='privacy', invoke_without_command=True)
    async def privacy_commands(self, ctx):
        """Commandes de confidentialité RGPD - Interface moderne avec boutons"""
        
        from utils.discord_helpers.rgpd_consent_ui import show_privacy_management
        
        # Utiliser la nouvelle interface avec boutons
        await show_privacy_management(ctx)
    
    @privacy_commands.command(name='status')
    async def privacy_status(self, ctx):
        """Affiche le statut de vos données stockées"""
        
        has_consent, consent_data = rgpd_conversation_memory.check_user_consent(ctx.author.id)
        
        if not has_consent:
            status_embed = create_gaming_embed(
                title="🔒 Statut de vos données",
                description="❌ **Aucune donnée stockée**\n\nVous n'avez pas donné votre consentement pour le stockage de données.",
                color='warning'
            )
            status_embed.add_field(
                name="💡 Pour activer la mémoire",
                value="Utilisez `!privacy accept` pour permettre au bot de se souvenir de nos conversations.",
                inline=False
            )
        else:
            # Calculer les stats
            hashed_id = rgpd_conversation_memory._hash_user_id(str(ctx.author.id))
            message_count = len(rgpd_conversation_memory.conversations.get(hashed_id, []))
            consent_date = datetime.fromisoformat(consent_data.get('consent_date', ''))
            expiry_date = consent_date + timedelta(days=RGPD_CONFIG['consent_duration_days'])
            
            status_embed = create_gaming_embed(
                title="🔒 Statut de vos données",
                description="✅ **Consentement accordé**\n\nVos données sont stockées de manière sécurisée.",
                color='success'
            )
            
            status_embed.add_field(
                name="📊 Données stockées",
                value=f"• Messages en mémoire: {message_count}\n"
                      f"• Conservation des messages: {RGPD_CONFIG['memory_duration_hours']}h\n"
                      f"• Accordé le: {consent_date.strftime('%d/%m/%Y')}\n"
                      f"• Expire le: {expiry_date.strftime('%d/%m/%Y')}",
                inline=False
            )
            
            status_embed.add_field(
                name="🔄 Actions disponibles",
                value="`!privacy forget` - Supprimer toutes vos données\n"
                      "`!privacy export` - Exporter vos données (Article 20 RGPD)",
                inline=False
            )
        
        await ctx.send(embed=status_embed, ephemeral=True)
    
    @privacy_commands.command(name='accept')
    async def privacy_accept(self, ctx):
        """Active la mémoire conversationnelle"""
        
        # Accorder le consentement pour la durée par défaut
        success = rgpd_conversation_memory.grant_user_consent(ctx.author.id)
        
        if success:
            accept_embed = create_gaming_embed(
                title="✅ Consentement accordé",
                description=f"Merci ! Je peux maintenant garder en mémoire nos conversations pendant **{RGPD_CONFIG['memory_duration_hours']}h**.",
                color='success'
            )
            
            accept_embed.add_field(
                name="🔐 Sécurité et Durée",
                value=f"• Votre consentement est valable pour **{RGPD_CONFIG['consent_duration_days']} jours**.\n"
                      f"• Vos données sont chiffrées (AES-256).\n"
                      f"• Suppression automatique des messages après {RGPD_CONFIG['memory_duration_hours']}h.\n"
                      "• Conformité RGPD garantie.",
                inline=False
            )
            
            accept_embed.add_field(
                name="🔄 Révocation",
                value="Vous pouvez révoquer ce consentement à tout moment avec `!privacy forget`",
                inline=False
            )
        else:
            accept_embed = create_gaming_embed(
                title="❌ Erreur",
                description="Une erreur s'est produite lors de l'enregistrement de votre consentement.",
                color='error'
            )
        
        await ctx.send(embed=accept_embed, ephemeral=True)
    
    @privacy_commands.command(name='decline')
    async def privacy_decline(self, ctx):
        """Refuse le stockage de données"""
        
        decline_embed = create_gaming_embed(
            title="✅ Choix respecté",
            description="Aucune donnée ne sera stockée. Je continuerai à vous aider sans mémoire conversationnelle.",
            color='info'
        )
        
        decline_embed.add_field(
            name="💡 Fonctionnalités limitées",
            value="Sans mémoire, je ne pourrai pas:\n"
                  "• Me souvenir de vos jeux préférés\n"
                  "• Maintenir le contexte entre messages\n"
                  "• Personnaliser mes réponses",
            inline=False
        )
        
        decline_embed.add_field(
            name="🔄 Changement d'avis",
            value="Vous pouvez activer la mémoire plus tard avec `!privacy accept`",
            inline=False
        )
        
        await ctx.send(embed=decline_embed, ephemeral=True)
    
    @privacy_commands.command(name='consent')
    async def privacy_consent(self, ctx):
        """Force la redemande de consentement (si vous avez changé d'avis)"""
        
        from utils.discord_helpers.rgpd_consent_ui import consent_declined_cache, show_consent_request
        
        # Supprimer du cache de refus si présent
        if ctx.author.id in consent_declined_cache:
            del consent_declined_cache[ctx.author.id]
        
        # Créer un message artificiel pour la demande de consentement
        class FakeMessage:
            def __init__(self, content, author, mentions):
                self.content = content
                self.author = author
                self.mentions = mentions
        
        fake_message = FakeMessage("@bot je veux changer d'avis sur le consentement", ctx.author, [ctx.bot.user])
        
        # Afficher la demande de consentement
        success = await show_consent_request(ctx, ctx.bot, fake_message)
        
        if not success:
            # Si la fonction ne fonctionne pas, afficher un message alternatif
            consent_embed = create_gaming_embed(
                title="🔄 Changement de consentement",
                description="Voulez-vous maintenant autoriser le stockage de vos conversations ?",
                color='info'
            )
            await ctx.send(embed=consent_embed, ephemeral=True)
    
    # Commande forget supprimée - utilisez l'interface !privacy avec boutons
    # Commande export supprimée - utilisez l'interface !privacy avec boutons
    
    @privacy_commands.command(name='info')
    async def privacy_info(self, ctx):
        """Informations détaillées sur la gestion des données"""
        
        info_embed = create_gaming_embed(
            title="📋 Information RGPD - MonBotGaming",
            description="Détails sur la collecte et le traitement de vos données personnelles",
            color='info'
        )
        
        info_embed.add_field(
            name="📝 Données collectées",
            value="• Contenu des messages (chiffré)\n"
                  "• Contexte de conversation\n"
                  "• Préférences gaming déduites\n"
                  "• Horodatage des interactions",
            inline=True
        )
        
        info_embed.add_field(
            name="🎯 Finalités",
            value="• Améliorer la qualité des réponses\n"
                  "• Maintenir le contexte conversationnel\n"
                  "• Personnaliser l'assistance gaming\n"
                  "• Éviter les répétitions",
            inline=True
        )
        
        info_embed.add_field(
            name="🔐 Sécurité",
            value="• Chiffrement AES-256\n"
                  "• Hachage anonymisant des IDs\n"
                  "• Suppression automatique\n"
                  "• Accès restreint aux données",
            inline=True
        )
        
        info_embed.add_field(
            name="⏱️ Conservation",
            value=f"• Mémoire conversationnelle: {RGPD_CONFIG['memory_duration_hours']}h\n"
                  f"• Consentement utilisateur: {RGPD_CONFIG['consent_duration_days']} jours\n"
                  "• Suppression automatique\n"
                  "• Pas de sauvegarde long terme",
            inline=True
        )
        
        info_embed.add_field(
            name="🌍 Transferts",
            value="• Stockage local uniquement\n"
                  "• Pas de transfert vers des tiers\n"
                  "• Pas d'analyse externe\n"
                  "• Données en France",
            inline=True
        )
        
        info_embed.add_field(
            name="⚖️ Base légale",
            value="• Consentement explicite (Art. 6 RGPD)\n"
                  "• Révocable à tout moment\n"
                  "• Durée limitée\n"
                  "• Finalité spécifique",
            inline=True
        )
        
        info_embed.add_field(
            name="📧 Contact",
            value="Pour toute question sur vos données:\n"
                  "• Utilisez les commandes `!privacy`\n"
                  "• Droit à l'information garanti\n"
                  "• Réponse immédiate automatisée",
            inline=False
        )
        
        await ctx.send(embed=info_embed, ephemeral=True)

async def setup(bot):
    """Charge le cog Privacy"""
    await bot.add_cog(PrivacyCommands(bot))
