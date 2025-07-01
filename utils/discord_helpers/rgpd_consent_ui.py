# 🎮 Interface de Consentement RGPD - Boutons Discord Interactifs
# Solution user-friendly pour le consentement RGPD avec boutons

import discord
from discord.ext import commands
import sys
import os

# Ajouter utils au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from datetime import datetime, timedelta
from config import RGPD_CONFIG
from utils.data_management.rgpd_conversation_memory import rgpd_conversation_memory
from utils.discord_helpers.embed_helpers import create_gaming_embed

class ConsentView(discord.ui.View):
    """Vue avec boutons pour le consentement RGPD"""
    
    def __init__(self, user_id: int, bot: commands.Bot, original_message: discord.Message):
        super().__init__(timeout=300)  # 5 minutes pour décider
        self.user_id = user_id
        self.bot = bot
        self.original_message = original_message
        self.responded = False
    
    @discord.ui.button(label=f"✅ Activer la mémoire ({RGPD_CONFIG['memory_duration_hours']}h)", style=discord.ButtonStyle.green, emoji='🧠')
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Accepter avec la durée par défaut"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        self.responded = True
        success = rgpd_conversation_memory.grant_user_consent(self.user_id)
        
        if success:
            success_embed = create_gaming_embed(
                title="🎮 Mémoire activée !",
                description=f"✅ **Parfait !** Je me souviendrai de nos conversations pendant **{RGPD_CONFIG['memory_duration_hours']} heures**.\n\nJe réponds à ta question initiale tout de suite ! 🚀",
                color='success'
            )
            # Relancer le traitement du message original
            await self.bot.process_commands(self.original_message)
        else:
            success_embed = create_gaming_embed(
                title="❌ Erreur",
                description="Une erreur s'est produite. Réessaie plus tard !",
                color='error'
            )
        
        # Désactiver tous les boutons
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=success_embed, view=self)
    
    @discord.ui.button(label='❌ Non merci', style=discord.ButtonStyle.gray, emoji='🚫')
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Refuser le stockage"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        self.responded = True
        
        decline_embed = create_gaming_embed(
            title="✅ Choix respecté",
            description="**Aucun problème !** Je continuerai à t'aider sans mémoire conversationnelle.\n\nTu peux changer d'avis à tout moment ! 🎮",
            color='info'
        )
        
        # Désactiver tous les boutons
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=decline_embed, view=self)
    
    @discord.ui.button(label='ℹ️ Plus d\'infos', style=discord.ButtonStyle.secondary, emoji='📋')
    async def more_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Afficher plus d'informations RGPD"""
        
        info_embed = create_gaming_embed(
            title="📋 Informations détaillées - RGPD",
            description="**MonBotGaming** respecte ta vie privée et se conforme au RGPD européen.",
            color='info'
        )
        
        info_embed.add_field(
            name="📝 Qu'est-ce qui est stocké ?",
            value="• Le contexte de nos conversations récentes\n• Tes préférences gaming (déduites)\n• **Aucune donnée personnelle identifiable**\n• Tout est chiffré et anonymisé",
            inline=False
        )
        
        info_embed.add_field(
            name="🎯 Pourquoi ?",
            value="• Pour te donner des réponses plus pertinentes\n• Éviter de répéter les infos\n• Adapter mes conseils gaming à tes goûts\n• Maintenir une conversation fluide",
            inline=False
        )
        
        info_embed.add_field(
            name="🔐 Sécurité",
            value=f"• Chiffrement AES-256 (standard bancaire)\n• Hachage anonymisant des identifiants\n• Suppression automatique après {RGPD_CONFIG['memory_duration_hours']}h\n• Stockage local sécurisé",
            inline=False
        )
        
        info_embed.add_field(
            name="⚖️ Tes droits",
            value="• Révocation à tout moment (`!privacy forget`)\n• Export de tes données (`!privacy export`)\n• Consultation du statut (`!privacy status`)\n• Information complète garantie",
            inline=False
        )
        
        await interaction.response.send_message(embed=info_embed, ephemeral=True)
    
    async def on_timeout(self):
        """Appelé quand la vue expire"""
        if not self.responded:
            # Désactiver tous les boutons
            for item in self.children:
                item.disabled = True


class PrivacyManagementView(discord.ui.View):
    """Vue pour la gestion avancée de la confidentialité"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
    
    @discord.ui.button(label='📊 Mes données', style=discord.ButtonStyle.blurple, emoji='📊')
    async def view_data(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Voir ses données stockées"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        has_consent, consent_data = rgpd_conversation_memory.check_user_consent(self.user_id)
        
        if not has_consent:
            status_embed = create_gaming_embed(
                title="🔒 Tes données",
                description="❌ **Aucune donnée stockée**\n\nTu n'as pas donné ton consentement.",
                color='warning'
            )
        else:
            hashed_id = rgpd_conversation_memory._hash_user_id(str(self.user_id))
            message_count = len(rgpd_conversation_memory.conversations.get(hashed_id, []))
            consent_date = datetime.fromisoformat(consent_data.get('consent_date', ''))
            expiry_date = consent_date + timedelta(days=RGPD_CONFIG['consent_duration_days'])
            
            status_embed = create_gaming_embed(
                title="🔒 Tes données",
                description="✅ **Consentement actif**",
                color='success'
            )
            status_embed.add_field(
                name="📊 Résumé",
                value=f"• Messages en mémoire: {message_count}\n"
                      f"• Conservation des messages: {RGPD_CONFIG['memory_duration_hours']}h\n"
                      f"• Accordé le: {consent_date.strftime('%d/%m/%Y')}\n"
                      f"• Expire le: {expiry_date.strftime('%d/%m/%Y')}",
                inline=False
            )
        
        await interaction.response.send_message(embed=status_embed, ephemeral=True)
    
    @discord.ui.button(label='📦 Exporter', style=discord.ButtonStyle.green, emoji='📦')
    async def export_data(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Exporter ses données"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        export_data = rgpd_conversation_memory.export_user_data(self.user_id)
        
        export_embed = create_gaming_embed(
            title="📦 Export de tes données",
            description=f"Voici tout ce que MonBotGaming stocke à ton sujet :",
            color='info'
        )
        
        export_embed.add_field(
            name="📊 Résumé",
            value=f"• ID anonymisé: {export_data['user_id_hash'][:16]}...\n"
                  f"• Consentement: {'✅' if export_data['consent_status'] else '❌'}\n"
                  f"• Messages: {export_data['conversations_count']}\n"
                  f"• Export: {export_data['export_date'][:10]}",
            inline=False
        )
        
        if export_data.get('conversations'):
            conversations_preview = []
            for conv in export_data['conversations'][:3]:  # Seulement les 3 derniers
                sender = "Toi" if not conv['is_bot'] else "Bot"
                conversations_preview.append(f"{sender}: {conv['content'][:50]}...")
            
            export_embed.add_field(
                name="💬 Aperçu des conversations",
                value="\n".join(conversations_preview) or "Aucune conversation",
                inline=False
            )
        
        await interaction.response.send_message(embed=export_embed, ephemeral=True)
    
    @discord.ui.button(label='🗑️ Tout supprimer', style=discord.ButtonStyle.red, emoji='🗑️')
    async def forget_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Supprimer toutes ses données"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        success = rgpd_conversation_memory.revoke_user_consent(self.user_id)
        
        if success:
            forget_embed = create_gaming_embed(
                title="🗑️ Données supprimées",
                description="✅ **Droit à l'oubli exercé**\n\nToutes tes données ont été définitivement supprimées.",
                color='success'
            )
            forget_embed.add_field(
                name="🧹 Actions effectuées",
                value="• Consentement révoqué\n• Conversations effacées\n• Données chiffrées supprimées\n• Historique vidé",
                inline=False
            )
        else:
            forget_embed = create_gaming_embed(
                title="❌ Erreur",
                description="Erreur lors de la suppression. Réessaie plus tard !",
                color='error'
            )
        
        await interaction.response.send_message(embed=forget_embed, ephemeral=True)


async def show_consent_request(ctx, bot, original_message):
    """Affiche la demande de consentement avec boutons interactifs"""
    
    consent_embed = create_gaming_embed(
        title="🎮 Salut ! Configurons ta mémoire gaming",
        description=f"Hey **{ctx.author.display_name}** ! 👋\n\nPour t'offrir la meilleure expérience gaming, je peux garder en mémoire nos conversations. **Ton choix !**",
        color='info'
    )
    
    consent_embed.add_field(
        name="🧠 Avec la mémoire, je peux :",
        value="• Me souvenir de tes jeux favoris\n• Maintenir le contexte entre messages\n• Te donner des conseils personnalisés\n• Éviter de répéter les infos",
        inline=False
    )
    
    consent_embed.add_field(
        name="🔐 Sécurité garantie :",
        value=f"• Données chiffrées et anonymisées\n• Suppression automatique après {RGPD_CONFIG['memory_duration_hours']}h\n• Conforme RGPD\n• Révocable à tout moment",
        inline=False
    )
    
    consent_embed.add_field(
        name="⏰ Choisis ta durée :",
        value=f"**{RGPD_CONFIG['memory_duration_hours']}h** = Parfait pour une session gaming\n**Refuser** = Pas de problème !",
        inline=False
    )
    
    view = ConsentView(ctx.author.id, bot, original_message)
    
    try:
        await ctx.send(embed=consent_embed, view=view, ephemeral=True)
        return True
    except Exception as e:
        print(f"Erreur affichage consentement: {e}")
        return False



async def show_privacy_management(ctx):
    """Affiche l'interface de gestion de la confidentialité"""
    
    privacy_embed = create_gaming_embed(
        title="🔒 Gestion de tes données",
        description="Contrôle total sur tes informations personnelles",
        color='info'
    )
    
    has_consent, consent_data = rgpd_conversation_memory.check_user_consent(ctx.author.id)
    
    if has_consent:
        privacy_embed.add_field(
            name="✅ Statut actuel",
            value=f"Mémoire active ({RGPD_CONFIG['memory_duration_hours']}h)",
            inline=False
        )
    else:
        privacy_embed.add_field(
            name="❌ Statut actuel",
            value="Aucune donnée stockée",
            inline=False
        )
    
    privacy_embed.add_field(
        name="🎮 Actions disponibles",
        value="Utilise les boutons ci-dessous pour gérer tes données",
        inline=False
    )
    
    view = PrivacyManagementView(ctx.author.id)
    
    try:
        await ctx.send(embed=privacy_embed, view=view, ephemeral=True)
        return True
    except Exception as e:
        print(f"Erreur gestion privacy: {e}")
        return False
