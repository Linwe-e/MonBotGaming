# 🔒 Privacy Commands pour MonBotGaming - Conformité RGPD
# Commandes de gestion des données personnelles et consentements

import discord
from discord.ext import commands
import sys
import os

# Ajouter utils au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from utils.rgpd_conversation_memory import rgpd_conversation_memory
from utils.embed_helpers import create_gaming_embed

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
        
        from utils.rgpd_consent_ui import show_privacy_management
        
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
                value="Utilisez `!privacy accept [heures]` pour permettre au bot de se souvenir de nos conversations.",
                inline=False
            )
        else:
            # Calculer les stats
            hashed_id = rgpd_conversation_memory._hash_user_id(str(ctx.author.id))
            message_count = len(rgpd_conversation_memory.conversations.get(hashed_id, []))
            
            status_embed = create_gaming_embed(
                title="🔒 Statut de vos données",
                description="✅ **Consentement accordé**\n\nVos données sont stockées de manière sécurisée.",
                color='success'
            )
            
            status_embed.add_field(
                name="📊 Données stockées",
                value=f"• Messages en mémoire: {message_count}\n"
                      f"• Durée de conservation: {consent_data.get('memory_duration_hours', 2)}h\n"
                      f"• Consentement accordé: {consent_data.get('consent_date', '')[:10]}\n"
                      f"• Type de données: Contexte conversationnel chiffré",
                inline=False
            )
            
            status_embed.add_field(
                name="🔄 Actions disponibles",
                value="`!privacy forget` - Supprimer toutes vos données\n"
                      "`!privacy export` - Télécharger vos données",
                inline=False
            )
        
        await ctx.send(embed=status_embed)
    
    @privacy_commands.command(name='accept')
    async def privacy_accept(self, ctx, duration: int = 2):
        """Active la mémoire conversationnelle - !privacy accept [heures]"""
        
        # Valider la durée
        if duration < 1:
            duration = 1
        elif duration > 24:
            duration = 24
        
        # Accorder le consentement
        success = rgpd_conversation_memory.grant_user_consent(ctx.author.id, duration)
        
        if success:
            accept_embed = create_gaming_embed(
                title="✅ Consentement accordé",
                description=f"Merci ! Je peux maintenant garder en mémoire nos conversations pendant **{duration}h**.",
                color='success'
            )
            
            accept_embed.add_field(
                name="🔐 Sécurité",
                value="• Vos données sont chiffrées (AES-256)\n"
                      "• Suppression automatique après expiration\n"
                      "• Aucune donnée personnelle identifiable stockée\n"
                      "• Conformité RGPD garantie",
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
        
        await ctx.send(embed=accept_embed)
    
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
        
        await ctx.send(embed=decline_embed)
    
    @privacy_commands.command(name='forget')
    async def privacy_forget(self, ctx):
        """Supprime toutes vos données (droit à l'oubli)"""
        
        # Supprimer toutes les données
        success = rgpd_conversation_memory.revoke_user_consent(ctx.author.id)
        
        if success:
            forget_embed = create_gaming_embed(
                title="🗑️ Données supprimées",
                description="✅ **Droit à l'oubli exercé**\n\nToutes vos données ont été définitivement supprimées.",
                color='success'
            )
            
            forget_embed.add_field(
                name="🧹 Actions effectuées",
                value="• Consentement révoqué\n"
                      "• Conversations supprimées\n"
                      "• Données chiffrées effacées\n"
                      "• Historique vidé",
                inline=False
            )
        else:
            forget_embed = create_gaming_embed(
                title="❌ Erreur",
                description="Une erreur s'est produite lors de la suppression.",
                color='error'
            )
        
        await ctx.send(embed=forget_embed)
    
    @privacy_commands.command(name='export')
    async def privacy_export(self, ctx):
        """Exporte vos données (droit à la portabilité)"""
        
        # Exporter les données
        export_data = rgpd_conversation_memory.export_user_data(ctx.author.id)
        
        export_embed = create_gaming_embed(
            title="📦 Export de vos données",
            description="Voici toutes les données que MonBotGaming stocke à votre sujet :",
            color='info'
        )
        
        export_embed.add_field(
            name="📊 Informations générales",
            value=f"• ID anonymisé: {export_data['user_id_hash']}\n"
                  f"• Consentement: {'✅ Accordé' if export_data['consent_status'] else '❌ Non accordé'}\n"
                  f"• Conversations: {export_data['conversations_count']} messages\n"
                  f"• Date d'export: {export_data['export_date'][:10]}",
            inline=False
        )
        
        if export_data['consent_status'] and export_data.get('conversations'):
            # Créer un fichier avec les données
            export_text = "=== EXPORT DONNÉES MONBOTGAMING ===\n\n"
            export_text += f"Utilisateur: {export_data['user_id_hash']}\n"
            export_text += f"Date d'export: {export_data['export_date']}\n\n"
            export_text += "=== CONVERSATIONS ===\n"
            
            for conv in export_data['conversations']:
                sender = "Vous" if not conv['is_bot'] else "Bot"
                export_text += f"{conv['timestamp'][:19]} - {sender}: {conv['content']}\n"
            
            # Envoyer en fichier si possible (Discord limite)
            if len(export_text) < 1900:
                export_embed.add_field(
                    name="💬 Conversations",
                    value=f"```{export_text[-1800:]}```",
                    inline=False
                )
            else:
                export_embed.add_field(
                    name="💬 Conversations",
                    value="Trop de données pour affichage. Fichier généré dans `data/exports/`",
                    inline=False
                )
        
        export_embed.add_field(
            name="🔒 Note de confidentialité",
            value=export_data['note'],
            inline=False
        )
        
        await ctx.send(embed=export_embed)
    
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
            value="• Durée configurable (1-24h)\n"
                  "• Suppression automatique\n"
                  "• Nettoyage quotidien\n"
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
        
        await ctx.send(embed=info_embed)

async def setup(bot):
    """Charge le cog Privacy"""
    await bot.add_cog(PrivacyCommands(bot))
