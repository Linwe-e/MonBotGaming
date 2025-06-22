# 🎮 Exemples de Boutons Interactifs Discord

import discord
from discord.ext import commands

# ===============================
# 🎯 EXEMPLE 1: Menu Build Gaming
# ===============================

class BuildView(discord.ui.View):
    """Vue avec boutons pour gérer les builds"""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minutes timeout
    
    @discord.ui.button(label='🔥 Diablo 4', style=discord.ButtonStyle.danger, emoji='🔥')
    async def diablo_builds(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Afficher builds Diablo 4"""
        embed = discord.Embed(title="🔥 Builds Diablo 4 Disponibles", color=0x8B0000)
        embed.add_field(name="🧙‍♂️ Necromancer", value="• Blood Surge\n• Bone Spear\n• Army of the Dead", inline=True)
        embed.add_field(name="🏹 Rogue", value="• Penetrating Shot\n• Twisting Blades\n• Rain of Vengeance", inline=True)
        embed.add_field(name="🔮 Sorcerer", value="• Chain Lightning\n• Frozen Orb\n• Meteor", inline=True)
        
        # Nouveau menu pour choisir la classe
        view = DiabloClassView()
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🎯 Tarkov', style=discord.ButtonStyle.secondary, emoji='🔫')
    async def tarkov_builds(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Afficher loadouts Tarkov"""
        embed = discord.Embed(title="🔫 Loadouts Escape from Tarkov", color=0x2F3136)
        embed.add_field(name="💀 Budget PMC", value="• AK-74M + BP ammo\n• 6B3TM Armor\n• Berkut Backpack", inline=True)
        embed.add_field(name="👑 Chad Loadout", value="• HK 416 Meta\n• Slick Plate Carrier\n• Blackjack Backpack", inline=True)
        
        view = TarkovLoadoutView()
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='⚔️ WoW Classic', style=discord.ButtonStyle.primary, emoji='⚔️')
    async def wow_builds(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Afficher builds WoW"""
        embed = discord.Embed(title="⚔️ Builds WoW Classic", color=0xFFD700)
        embed.add_field(name="🛡️ Warrior Tank", value="• Protection Spec\n• Shield Slam Build\n• Threat Focused", inline=True)
        embed.add_field(name="❄️ Mage DPS", value="• Frost Spec\n• Frostbolt Spam\n• AoE Farming", inline=True)
        
        await interaction.response.edit_message(embed=embed, view=WoWBuildView())

class DiabloClassView(discord.ui.View):
    """Sous-menu pour les classes Diablo"""
    
    @discord.ui.button(label='🧙‍♂️ Voir Build Necro', style=discord.ButtonStyle.danger)
    async def necro_build(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Ici on afficherait le build détaillé du Necromancer
        embed = discord.Embed(title="🧙‍♂️ Build Necromancer - Blood Surge", color=0x8B0000)
        embed.add_field(name="⚔️ Compétences", value="Blood Surge (MAX)\nCorpse Explosion\nBone Armor", inline=False)
        embed.add_field(name="🛡️ Équipement", value="Bloodless Scream\nTemerity\nRing of Starless Skies", inline=False)
        
        # Boutons d'action sur le build
        view = BuildActionView()
        await interaction.response.edit_message(embed=embed, view=view)

class BuildActionView(discord.ui.View):
    """Actions sur un build spécifique"""
    
    @discord.ui.button(label='💾 Sauvegarder', style=discord.ButtonStyle.success, emoji='💾')
    async def save_build(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Build sauvegardé dans vos favoris!", ephemeral=True)
    
    @discord.ui.button(label='📤 Partager', style=discord.ButtonStyle.primary, emoji='📤')
    async def share_build(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔗 Lien de partage: https://monbotgaming.com/builds/necro_blood", ephemeral=True)
    
    @discord.ui.button(label='🏠 Menu Principal', style=discord.ButtonStyle.secondary, emoji='🏠')
    async def back_to_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="🎮 Menu Principal - Builds Gaming", color=0x7289DA)
        embed.description = "Choisissez votre jeu pour voir les builds disponibles !"
        view = BuildView()
        await interaction.response.edit_message(embed=embed, view=view)

# ===============================
# 🎯 EXEMPLE 2: Menu Événements
# ===============================

class EventView(discord.ui.View):
    """Menu pour les événements gaming"""
    
    @discord.ui.button(label='📅 Créer Événement', style=discord.ButtonStyle.success, emoji='📅')
    async def create_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Ouvrir un modal (formulaire) pour créer l'événement
        modal = CreateEventModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label='👥 Voir Événements', style=discord.ButtonStyle.primary, emoji='👥')
    async def view_events(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="📅 Événements à Venir", color=0x00FF7F)
        embed.add_field(name="🏰 Raid MC", value="Demain 20h00\n15/40 inscrits", inline=True)
        embed.add_field(name="🎯 Tournoi LoL", value="Samedi 14h00\n8/16 équipes", inline=True)
        
        view = EventActionView()
        await interaction.response.edit_message(embed=embed, view=view)

class EventActionView(discord.ui.View):
    """Actions sur les événements"""
    
    @discord.ui.button(label='✅ S\'inscrire', style=discord.ButtonStyle.success, emoji='✅')
    async def join_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Inscription confirmée au Raid MC!", ephemeral=True)
    
    @discord.ui.button(label='❌ Se désinscrire', style=discord.ButtonStyle.danger, emoji='❌')
    async def leave_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Désinscription confirmée.", ephemeral=True)

# ===============================
# 🎯 EXEMPLE 3: Menu Stats Gaming
# ===============================

class StatsView(discord.ui.View):
    """Menu pour les statistiques gaming"""
    
    @discord.ui.button(label='📊 Mes Stats', style=discord.ButtonStyle.primary, emoji='📊')
    async def my_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Afficher les stats du joueur
        embed = discord.Embed(title=f"📊 Stats Gaming - {interaction.user.name}", color=0x00FF7F)
        embed.add_field(name="🎮 Jeux Joués", value="Diablo 4: 120h\nWoW: 450h\nLoL: 89h", inline=False)
        embed.add_field(name="🏆 Achievements", value="🔥 Build Master\n⚔️ Raid Leader\n🎯 PvP Champion", inline=False)
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label='🏆 Classements', style=discord.ButtonStyle.secondary, emoji='🏆')
    async def leaderboards(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="🏆 Classements Serveur", color=0xFFD700)
        embed.add_field(name="👑 Top Gamers", value="1. Player1 - 1250 XP\n2. Player2 - 1100 XP\n3. Player3 - 950 XP", inline=False)
        await interaction.response.edit_message(embed=embed)

# ===============================
# 🎯 Commande principale avec menu
# ===============================

@bot.command()
async def menu(ctx):
    """Afficher le menu principal interactif"""
    embed = discord.Embed(
        title="🎮 MonBotGaming - Menu Principal", 
        description="Utilisez les boutons ci-dessous pour naviguer !",
        color=0x7289DA
    )
    embed.add_field(name="🔧 Builds", value="Gérer vos builds gaming", inline=True)
    embed.add_field(name="📅 Événements", value="Organiser des sessions", inline=True)
    embed.add_field(name="📊 Stats", value="Voir vos statistiques", inline=True)
    
    # Menu principal avec sélecteur
    view = MainMenuView()
    await ctx.send(embed=embed, view=view)

class MainMenuView(discord.ui.View):
    """Menu principal du bot"""
    
    @discord.ui.select(
        placeholder="🎮 Choisissez une catégorie...",
        options=[
            discord.SelectOption(label="Builds Gaming", description="Gérer vos builds et loadouts", emoji="🔧"),
            discord.SelectOption(label="Événements", description="Organiser des sessions gaming", emoji="📅"),
            discord.SelectOption(label="Statistiques", description="Voir vos stats et classements", emoji="📊"),
            discord.SelectOption(label="Mini-jeux", description="Jeux Discord amusants", emoji="🎲"),
        ]
    )
    async def menu_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values[0] == "Builds Gaming":
            embed = discord.Embed(title="🔧 Menu Builds Gaming", color=0x7289DA)
            view = BuildView()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "Événements":
            embed = discord.Embed(title="📅 Menu Événements", color=0x00FF7F)
            view = EventView()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "Statistiques":
            embed = discord.Embed(title="📊 Menu Statistiques", color=0xFFD700)
            view = StatsView()
            await interaction.response.edit_message(embed=embed, view=view)
