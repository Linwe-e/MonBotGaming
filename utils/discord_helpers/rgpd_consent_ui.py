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

# Cache temporaire pour les refus de consentement (éviter de redemander immédiatement)
consent_declined_cache = {}


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
        success = rgpd_conversation_memory.grant_user_consent(str(self.user_id))
        
        if success:
            success_embed = create_gaming_embed(
                title="🎮 Mémoire activée !",
                description=f"✅ **Parfait !** Je me souviendrai de nos conversations pendant **{RGPD_CONFIG['memory_duration_hours']} heures**.\n\nJe réponds à ta question initiale maintenant ! 🚀",
                color='success'
            )
            
            # Répondre d'abord avec la confirmation
            await interaction.response.edit_message(embed=success_embed, view=None)
            
            # Puis traiter la question initiale
            await self._process_original_question()
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
        
        # Mémoriser le refus pour éviter de redemander (30 jours)
        consent_declined_cache[self.user_id] = datetime.now() + timedelta(days=30)
        
        decline_embed = create_gaming_embed(
            title="✅ Choix respecté",
            description="**Aucun problème !** Je continuerai à t'aider sans mémoire conversationnelle.\n\nTu peux changer d'avis à tout moment avec `!privacy` ! 🎮\n\n*Je ne te redemanderai plus pendant 30 jours.*",
            color='info'
        )
        
        # Désactiver tous les boutons
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=decline_embed, view=self)
        
        # Répondre à la question initiale sans mémoire
        await self._process_original_question_no_memory()
    
    @discord.ui.button(label='ℹ️ Plus d\'infos', style=discord.ButtonStyle.secondary, emoji='📋')
    async def more_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Afficher plus d'informations RGPD"""
        
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
        
        await interaction.response.send_message(embed=info_embed, ephemeral=True)
    
    async def _process_original_question(self):
        """Traite la question initiale après acceptation du consentement"""
        try:
            # Extraire le contenu du message sans la mention du bot
            content = self.original_message.content
            for mention in self.original_message.mentions:
                if mention == self.bot.user:
                    content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
            
            content = content.strip()
            
            if content:
                # Importer les modules nécessaires
                from utils.ai.gemini_ai import gemini_ai
                from utils.ai.smart_response import SmartResponseManager
                from utils.discord_helpers.embed_helpers import create_ai_response_embed
                from utils.data_management.rgpd_conversation_memory import rgpd_conversation_memory
                
                if gemini_ai.is_available():
                    # Ajouter la question à la mémoire
                    rgpd_conversation_memory.add_message(str(self.user_id), content)
                    
                    # Analyser le type de réponse
                    use_embed, embed_type = SmartResponseManager.should_use_embed(content)
                    
                    # Générer la réponse IA
                    response = await gemini_ai.gaming_assistant(content)
                    
                    if embed_type == 'light':
                        # Embed simple
                        simple_embed = discord.Embed(
                            description=response[:1000] if len(response) <= 1000 else response[:1000] + "...",
                            color=0x00ff88
                        )
                        await self.original_message.reply(embed=simple_embed)
                    elif use_embed:
                        # Embed complet
                        response_embed = create_ai_response_embed(content, response)
                        response_embed.description = response[:1000] if len(response) <= 1000 else response[:1000]
                        await self.original_message.reply(embed=response_embed)
                    else:
                        # Réponse simple
                        if len(response) <= 1500:
                            await self.original_message.reply(response)
                        else:
                            await self.original_message.reply(response[:1500] + "...")
                    
                    # Sauvegarder la réponse du bot
                    rgpd_conversation_memory.add_message(
                        str(self.user_id),
                        response[:200] + "..." if len(response) > 200 else response,
                        is_bot=True
                    )
                else:
                    await self.original_message.reply("🤖 L'assistant gaming n'est pas disponible pour le moment.")
            else:
                # Pas de question, juste une salutation
                await self.original_message.reply(f"🎮 Salut {self.original_message.author.mention} ! Maintenant que j'ai ma mémoire, on peut discuter gaming ! 🚀")
                
        except Exception as e:
            print(f"Erreur lors du traitement de la question initiale: {e}")
            await self.original_message.reply("🎮 Je suis prêt à t'aider maintenant ! Pose-moi tes questions gaming ! 🚀")
    
    async def _process_original_question_no_memory(self):
        """Traite la question initiale sans mémoire (après refus de consentement)"""
        try:
            # Extraire le contenu du message sans la mention du bot
            content = self.original_message.content
            for mention in self.original_message.mentions:
                if mention == self.bot.user:
                    content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
            
            content = content.strip()
            
            if content:
                # Importer les modules nécessaires
                from utils.ai.gemini_ai import gemini_ai
                from utils.ai.smart_response import SmartResponseManager
                from utils.discord_helpers.embed_helpers import create_ai_response_embed
                
                if gemini_ai.is_available():
                    # Analyser le type de réponse
                    use_embed, embed_type = SmartResponseManager.should_use_embed(content)
                    
                    # Générer la réponse IA SANS contexte
                    response = await gemini_ai.gaming_assistant(content, game_context="")
                    
                    if embed_type == 'light':
                        # Embed simple
                        simple_embed = discord.Embed(
                            description=response[:1000] if len(response) <= 1000 else response[:1000] + "...",
                            color=0x00ff88
                        )
                        await self.original_message.reply(embed=simple_embed)
                    elif use_embed:
                        # Embed complet
                        response_embed = create_ai_response_embed(content, response)
                        response_embed.description = response[:1000] if len(response) <= 1000 else response[:1000]
                        await self.original_message.reply(embed=response_embed)
                    else:
                        # Réponse simple
                        if len(response) <= 1500:
                            await self.original_message.reply(response)
                        else:
                            await self.original_message.reply(response[:1500] + "...")
                else:
                    await self.original_message.reply("🤖 L'assistant gaming n'est pas disponible pour le moment.")
            else:
                # Pas de question, juste une salutation
                await self.original_message.reply(f"🎮 Salut {self.original_message.author.mention} ! En quoi puis-je t'aider ?")
                
        except Exception as e:
            print(f"Erreur lors du traitement de la question sans mémoire: {e}")
            await self.original_message.reply("🎮 En quoi puis-je t'aider gaming ? 🚀")
    
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
        
        has_consent, consent_data = rgpd_conversation_memory.check_user_consent(str(self.user_id))
        
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
        """Exporter ses données - Conformité Article 20 RGPD"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        try:
            import io
            
            export_data = rgpd_conversation_memory.export_user_data(str(self.user_id))
            
            if not export_data['consent_status']:
                await interaction.response.send_message("Vous n'avez pas de données à exporter car vous n'avez pas donné votre consentement.", ephemeral=True)
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
            can_attach_files = False
            if interaction.guild and interaction.channel:
                can_attach_files = interaction.channel.permissions_for(interaction.guild.me).attach_files
            else:
                can_attach_files = True  # Fallback pour les DM
            
            if can_attach_files:
                # Créer un fichier en mémoire (conforme Article 20 RGPD)
                export_file = io.BytesIO(export_text.encode('utf-8'))
                
                # Créer l'embed de confirmation
                export_embed = create_gaming_embed(
                    title="📦 Export de tes données",
                    description="✅ **Conformité Article 20 RGPD**\n\nTes données sont fournies dans un format structuré et lisible.",
                    color='success'
                )
                export_embed.add_field(
                    name="📄 Fichier",
                    value="`export_donnees.txt`",
                    inline=True
                )
                export_embed.add_field(
                    name="🔒 Confidentialité",
                    value="Ce message et le fichier ne sont visibles que par toi.",
                    inline=True
                )
                
                # Envoyer le message éphémère avec le fichier
                await interaction.response.send_message(
                    embed=export_embed, 
                    file=discord.File(export_file, filename="export_donnees.txt"),
                    ephemeral=True
                )
            else:
                # Fallback si pas de permission ATTACH_FILES
                export_embed = create_gaming_embed(
                    title="📦 Export de tes données",
                    description="⚠️ **Permission manquante**\n\nLe bot n'a pas la permission d'envoyer des fichiers. Tes données s'affichent ci-dessous.",
                    color='warning'
                )
                export_embed.add_field(
                    name="� Conformité RGPD",
                    value="Données fournies conformément à l'Article 20 (format lisible).",
                    inline=False
                )
                
                # Envoyer l'embed d'abord
                await interaction.response.send_message(embed=export_embed, ephemeral=True)
                
                # Puis envoyer les données en blocs si nécessaire
                if len(export_text) <= 1900:
                    await interaction.followup.send(f"```\n{export_text}\n```", ephemeral=True)
                else:
                    # Découper en plusieurs messages
                    chunks = [export_text[i:i+1900] for i in range(0, len(export_text), 1900)]
                    for i, chunk in enumerate(chunks):
                        header = f"📄 **Partie {i+1}/{len(chunks)}**\n" if len(chunks) > 1 else ""
                        await interaction.followup.send(f"{header}```\n{chunk}\n```", ephemeral=True)
        except Exception as e:
            print(f"Erreur lors de l'export de données (interface boutons): {e}")
            error_embed = create_gaming_embed(
                title="❌ Erreur d'export",
                description="Une erreur est survenue lors de la création de ton fichier d'export. L'erreur a été enregistrée.",
                color='error'
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
    
    @discord.ui.button(label='🗑️ Tout supprimer', style=discord.ButtonStyle.red, emoji='🗑️')
    async def forget_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Supprimer toutes ses données"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        success = rgpd_conversation_memory.revoke_user_consent(str(self.user_id))
        
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
    
    @discord.ui.button(label='✅ Activer mémoire', style=discord.ButtonStyle.green, emoji='🧠')
    async def activate_memory(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Activer la mémoire conversationnelle"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce n'est pas pour toi !", ephemeral=True)
            return
        
        # Nettoyer le cache de refus
        clear_consent_cache_for_user(self.user_id)
        
        # Accorder le consentement
        success = rgpd_conversation_memory.grant_user_consent(str(self.user_id))
        
        if success:
            activate_embed = create_gaming_embed(
                title="🎮 Mémoire activée !",
                description=f"✅ **Parfait !** Je me souviendrai maintenant de nos conversations pendant **{RGPD_CONFIG['memory_duration_hours']} heures**.",
                color='success'
            )
            activate_embed.add_field(
                name="🔐 Sécurité",
                value=f"• Données chiffrées et anonymisées\n• Suppression automatique après {RGPD_CONFIG['memory_duration_hours']}h\n• Révocable à tout moment",
                inline=False
            )
        else:
            activate_embed = create_gaming_embed(
                title="❌ Erreur",
                description="Une erreur s'est produite lors de l'activation. Réessaie plus tard !",
                color='error'
            )
        
        await interaction.response.send_message(embed=activate_embed, ephemeral=True)


def clear_consent_cache_for_user(user_id: int):
    """Nettoie le cache de refus pour un utilisateur spécifique"""
    if user_id in consent_declined_cache:
        del consent_declined_cache[user_id]


async def show_consent_request(ctx, bot, original_message):
    """Affiche la demande de consentement avec boutons interactifs"""
    
    # Vérifier si l'utilisateur a récemment refusé le consentement
    user_id = ctx.author.id
    if user_id in consent_declined_cache:
        if datetime.now() < consent_declined_cache[user_id]:
            # L'utilisateur a refusé récemment, ne pas redemander
            return False
        else:
            # Le délai est expiré, supprimer du cache
            del consent_declined_cache[user_id]
    
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
