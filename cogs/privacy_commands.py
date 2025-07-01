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
        
        await ctx.send(embed=forget_embed, ephemeral=True)
    
    @privacy_commands.command(name='export')
    async def privacy_export(self, ctx):
        """Exporte vos données (droit à la portabilité) - Article 20 RGPD"""
        try:
            # Exporter les données
            export_data = rgpd_conversation_memory.export_user_data(ctx.author.id)
            
            if not export_data['consent_status']:
                await ctx.send("Vous n'avez pas de données à exporter car vous n'avez pas donné votre consentement.", ephemeral=True)
                return

            # Créer le contenu du fichier d'export
            export_text = f"=== EXPORT DE DONNÉES MONBOTGAMING ===\n\n"
            export_text += f"ID Utilisateur Anonymisé: {export_data['user_id_hash']}\n"
            export_text += f"Date d'Export: {export_data['export_date']}\n"
            export_text += f"Consentement Accordé: {'Oui' if export_data['consent_status'] else 'Non'}\n"
            export_text += f"Nombre de Messages en Mémoire: {export_data['conversations_count']}\n\n"
            
            if export_data.get('conversations'):
                export_text += "=== DÉTAIL DES CONVERSATIONS ===\n\n"
                for conv in export_data['conversations']:
                    sender = "Bot" if conv['is_bot'] else "Vous"
                    timestamp = datetime.fromisoformat(conv['timestamp']).strftime('%d/%m/%Y %H:%M:%S')
                    export_text += f"[{timestamp}] {sender}:\n{conv['content']}\n\n"
            else:
                export_text += "Aucune conversation en mémoire.\n"

            export_text += "\n=== FIN DE L'EXPORT ===\n"
            export_text += "Note: Les données sont chiffrées et anonymisées conformément au RGPD."

            # Vérifier si le bot a la permission d'envoyer des fichiers
            can_attach_files = ctx.channel.permissions_for(ctx.guild.me).attach_files if ctx.guild else True
            
            if can_attach_files:
                # Créer un fichier en mémoire (conforme Article 20 RGPD)
                export_file = io.BytesIO(export_text.encode('utf-8'))
                
                # Créer l'embed de confirmation
                export_embed = create_gaming_embed(
                    title="📦 Export de vos données",
                    description="✅ **Conformité Article 20 RGPD**\n\nVos données sont fournies dans un format structuré et lisible.",
                    color='success'
                )
                export_embed.add_field(
                    name="📄 Fichier",
                    value="`export_donnees.txt`",
                    inline=True
                )
                export_embed.add_field(
                    name="🔒 Confidentialité",
                    value="Ce message et le fichier ne sont visibles que par vous.",
                    inline=True
                )
                
                # Envoyer le message éphémère avec le fichier
                await ctx.send(
                    embed=export_embed, 
                    file=discord.File(export_file, filename="export_donnees.txt"),
                    ephemeral=True
                )
            else:
                # Fallback si pas de permission ATTACH_FILES
                export_embed = create_gaming_embed(
                    title="📦 Export de vos données",
                    description="⚠️ **Permission manquante**\n\nLe bot n'a pas la permission d'envoyer des fichiers. Vos données s'affichent ci-dessous.",
                    color='warning'
                )
                export_embed.add_field(
                    name="🔒 Conformité RGPD",
                    value="Données fournies conformément à l'Article 20 (format lisible).",
                    inline=False
                )
                
                # Envoyer l'embed d'abord
                await ctx.send(embed=export_embed, ephemeral=True)
                
                # Puis envoyer les données en blocs si nécessaire
                if len(export_text) <= 1900:
                    await ctx.send(f"```\n{export_text}\n```", ephemeral=True)
                else:
                    # Découper en plusieurs messages
                    chunks = [export_text[i:i+1900] for i in range(0, len(export_text), 1900)]
                    for i, chunk in enumerate(chunks):
                        header = f"📄 **Partie {i+1}/{len(chunks)}**\n" if len(chunks) > 1 else ""
                        await ctx.send(f"{header}```\n{chunk}\n```", ephemeral=True)
        except Exception as e:
            print(f"Erreur lors de l'export de données : {e}")
            error_embed = create_gaming_embed(
                title="❌ Erreur d'export",
                description="Une erreur est survenue lors de la création de votre fichier d'export. L'erreur a été enregistrée.",
                color='error'
            )
            await ctx.send(embed=error_embed, ephemeral=True)
    
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
