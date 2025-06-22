# 🎮 Exemples de Modals (Formulaires) Discord

import discord
from discord.ext import commands
from datetime import datetime

# ===============================
# 🎯 EXEMPLE 1: Créer un Événement
# ===============================

class CreateEventModal(discord.ui.Modal):
    """Formulaire pour créer un événement gaming"""
    
    def __init__(self):
        super().__init__(title="📅 Créer un Événement Gaming")
    
    # Champ nom de l'événement
    event_name = discord.ui.TextInput(
        label="🎮 Nom de l'Événement",
        placeholder="Ex: Raid Molten Core, Tournoi LoL, Session Tarkov...",
        max_length=100,
        required=True
    )
    
    # Champ jeu
    game = discord.ui.TextInput(
        label="🎯 Jeu",
        placeholder="Ex: WoW Classic, League of Legends, Diablo 4...",
        max_length=50,
        required=True
    )
    
    # Champ date et heure
    datetime_field = discord.ui.TextInput(
        label="📅 Date et Heure",
        placeholder="Ex: 2024-01-20 20:00 ou Samedi 20h",
        max_length=50,
        required=True
    )
    
    # Champ nombre de joueurs
    max_players = discord.ui.TextInput(
        label="👥 Nombre Maximum de Joueurs",
        placeholder="Ex: 40 (raid), 10 (équipe), 5 (groupe)...",
        max_length=3,
        required=False,
        default="10"
    )
    
    # Champ description
    description = discord.ui.TextInput(
        label="📝 Description (Optionnelle)",
        placeholder="Détails, prérequis, stuff recommandé...",
        style=discord.TextStyle.paragraph,
        max_length=500,
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Traitement du formulaire soumis"""
        
        # Créer l'embed de confirmation
        embed = discord.Embed(
            title=f"✅ Événement Créé: {self.event_name.value}",
            description=self.description.value or "Aucune description fournie",
            color=0x00FF7F,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="🎮 Jeu", value=self.game.value, inline=True)
        embed.add_field(name="📅 Date/Heure", value=self.datetime_field.value, inline=True)
        embed.add_field(name="👥 Joueurs Max", value=self.max_players.value, inline=True)
        embed.add_field(name="👤 Organisateur", value=interaction.user.mention, inline=True)
        embed.add_field(name="📊 Statut", value="🟢 Ouvert aux inscriptions", inline=True)
        
        embed.set_footer(text="Utilisez les boutons pour vous inscrire!")
        
        # Ajouter boutons d'inscription
        view = EventRegistrationView()
        
        await interaction.response.send_message(embed=embed, view=view)
        
        # TODO: Sauvegarder l'événement en base de données
        # db.save_event({
        #     'name': self.event_name.value,
        #     'game': self.game.value,
        #     'datetime': self.datetime_field.value,
        #     'max_players': int(self.max_players.value),
        #     'description': self.description.value,
        #     'organizer': interaction.user.id
        # })

# ===============================
# 🎯 EXEMPLE 2: Sauvegarder un Build
# ===============================

class SaveBuildModal(discord.ui.Modal):
    """Formulaire pour sauvegarder un build gaming"""
    
    def __init__(self):
        super().__init__(title="💾 Sauvegarder un Build")
    
    build_name = discord.ui.TextInput(
        label="🏷️ Nom du Build",
        placeholder="Ex: Necro Blood DPS, AK Meta Tarkov, Prot Warrior...",
        max_length=50,
        required=True
    )
    
    game = discord.ui.TextInput(
        label="🎮 Jeu",
        placeholder="Ex: Diablo 4, Tarkov, WoW Classic...",
        max_length=30,
        required=True
    )
    
    build_details = discord.ui.TextInput(
        label="🔧 Détails du Build",
        placeholder="Compétences, équipement, stats, rotations...",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        required=True
    )
    
    tags = discord.ui.TextInput(
        label="🏷️ Tags (séparés par virgules)",
        placeholder="Ex: DPS, Tank, PvP, Budget, Meta, Solo...",
        max_length=100,
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"💾 Build Sauvegardé: {self.build_name.value}",
            color=0x7289DA,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="🎮 Jeu", value=self.game.value, inline=True)
        embed.add_field(name="👤 Auteur", value=interaction.user.mention, inline=True)
        embed.add_field(name="🏷️ Tags", value=self.tags.value or "Aucun", inline=True)
        embed.add_field(name="🔧 Détails", value=self.build_details.value[:200] + "..." if len(self.build_details.value) > 200 else self.build_details.value, inline=False)
        
        await interaction.response.send_message(embed=embed)

# ===============================
# 🎯 EXEMPLE 3: Recherche de Partie
# ===============================

class FindTeamModal(discord.ui.Modal):
    """Formulaire pour rechercher une équipe/partie"""
    
    def __init__(self):
        super().__init__(title="👥 Rechercher une Équipe")
    
    game = discord.ui.TextInput(
        label="🎮 Jeu",
        placeholder="Ex: League of Legends, Valorant, Rocket League...",
        max_length=50,
        required=True
    )
    
    role_preferred = discord.ui.TextInput(
        label="🎯 Rôle Préféré",
        placeholder="Ex: ADC, Support, Tank, DPS, Jungle...",
        max_length=30,
        required=False
    )
    
    rank_level = discord.ui.TextInput(
        label="🏆 Rang/Niveau",
        placeholder="Ex: Gold 2, Plat, Global Elite, 1500 MMR...",
        max_length=30,
        required=False
    )
    
    availability = discord.ui.TextInput(
        label="📅 Disponibilité",
        placeholder="Ex: Soirs en semaine, Week-ends, Flexible...",
        max_length=100,
        required=False
    )
    
    comments = discord.ui.TextInput(
        label="💬 Commentaires",
        placeholder="Objectifs, style de jeu, expérience...",
        style=discord.TextStyle.paragraph,
        max_length=300,
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="👥 Recherche d'Équipe",
            description=f"**{interaction.user.name}** recherche une équipe !",
            color=0x00FF7F,
            timestamp=datetime.now()
        )
        
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.add_field(name="🎮 Jeu", value=self.game.value, inline=True)
        embed.add_field(name="🎯 Rôle", value=self.role_preferred.value or "Flexible", inline=True)
        embed.add_field(name="🏆 Rang", value=self.rank_level.value or "Non spécifié", inline=True)
        embed.add_field(name="📅 Dispo", value=self.availability.value or "À négocier", inline=True)
        
        if self.comments.value:
            embed.add_field(name="💬 Commentaires", value=self.comments.value, inline=False)
        
        # Boutons pour répondre
        view = TeamResponseView(interaction.user.id)
        
        await interaction.response.send_message(embed=embed, view=view)

# ===============================
# 🎯 Vue pour répondre aux recherches d'équipe
# ===============================

class TeamResponseView(discord.ui.View):
    """Boutons pour répondre à une recherche d'équipe"""
    
    def __init__(self, searcher_id):
        super().__init__(timeout=3600)  # 1 heure
        self.searcher_id = searcher_id
    
    @discord.ui.button(label='✋ Je suis intéressé(e)', style=discord.ButtonStyle.success, emoji='✋')
    async def interested(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.searcher_id:
            await interaction.response.send_message("❌ Vous ne pouvez pas répondre à votre propre recherche!", ephemeral=True)
            return
        
        # Envoyer un MP au chercheur
        searcher = interaction.guild.get_member(self.searcher_id)
        if searcher:
            try:
                embed = discord.Embed(
                    title="👥 Réponse à votre recherche d'équipe",
                    description=f"**{interaction.user.name}** est intéressé(e) pour jouer avec vous !",
                    color=0x00FF7F
                )
                embed.add_field(name="👤 Joueur", value=interaction.user.mention, inline=True)
                embed.add_field(name="🔗 Contact", value=f"Contactez {interaction.user.mention} sur le serveur", inline=False)
                
                await searcher.send(embed=embed)
                await interaction.response.send_message("✅ Votre intérêt a été transmis en MP!", ephemeral=True)
            except:
                await interaction.response.send_message("❌ Impossible d'envoyer le MP. Contactez directement la personne!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Utilisateur introuvable!", ephemeral=True)

# ===============================
# 🎯 Vue pour inscription aux événements
# ===============================

class EventRegistrationView(discord.ui.View):
    """Boutons pour s'inscrire à un événement"""
    
    def __init__(self):
        super().__init__(timeout=None)  # Pas de timeout pour les événements
        self.participants = []
    
    @discord.ui.button(label='✅ S\'inscrire', style=discord.ButtonStyle.success, emoji='✅')
    async def join_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.participants:
            await interaction.response.send_message("⚠️ Vous êtes déjà inscrit(e)!", ephemeral=True)
            return
        
        self.participants.append(interaction.user.id)
        await interaction.response.send_message(f"✅ **{interaction.user.name}** s'est inscrit(e) à l'événement!", ephemeral=True)
        
        # Mettre à jour l'embed avec le nouveau nombre
        embed = interaction.message.embeds[0]
        for i, field in enumerate(embed.fields):
            if field.name == "📊 Statut":
                embed.set_field_at(i, name="📊 Statut", value=f"🟢 {len(self.participants)} inscrit(s)", inline=True)
                break
        
        await interaction.edit_original_response(embed=embed, view=self)
    
    @discord.ui.button(label='❌ Se désinscrire', style=discord.ButtonStyle.danger, emoji='❌')
    async def leave_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in self.participants:
            await interaction.response.send_message("⚠️ Vous n'êtes pas inscrit(e)!", ephemeral=True)
            return
        
        self.participants.remove(interaction.user.id)
        await interaction.response.send_message(f"❌ **{interaction.user.name}** s'est désinscrit(e).", ephemeral=True)
    
    @discord.ui.button(label='👥 Voir Participants', style=discord.ButtonStyle.secondary, emoji='👥')
    async def view_participants(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.participants:
            await interaction.response.send_message("🔍 Aucun participant pour le moment.", ephemeral=True)
            return
        
        participants_list = []
        for user_id in self.participants:
            user = interaction.guild.get_member(user_id)
            if user:
                participants_list.append(f"• {user.mention}")
        
        embed = discord.Embed(
            title="👥 Liste des Participants",
            description="\n".join(participants_list),
            color=0x7289DA
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
