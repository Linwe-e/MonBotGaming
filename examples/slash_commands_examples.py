# 🎮 Exemples de Slash Commands Discord

import discord
from discord.ext import commands
from discord import app_commands

# ===============================
# 🎯 EXEMPLE 1: Slash Commands Builds
# ===============================

@app_commands.command(name="build", description="🔧 Gérer vos builds gaming")
@app_commands.describe(
    action="Action à effectuer",
    game="Jeu concerné",
    build_name="Nom du build (pour show/save)",
    details="Détails du build (pour save)"
)
@app_commands.choices(action=[
    app_commands.Choice(name="📋 Lister les builds", value="list"),
    app_commands.Choice(name="👁️ Afficher un build", value="show"),
    app_commands.Choice(name="💾 Sauvegarder un build", value="save"),
    app_commands.Choice(name="🗑️ Supprimer un build", value="delete")
])
@app_commands.choices(game=[
    app_commands.Choice(name="🔥 Diablo 4", value="diablo4"),
    app_commands.Choice(name="🔫 Escape from Tarkov", value="tarkov"),
    app_commands.Choice(name="⚔️ WoW Classic", value="wow_classic"),
    app_commands.Choice(name="⚡ League of Legends", value="lol"),
    app_commands.Choice(name="🏹 Baldur's Gate 3", value="bg3")
])
async def slash_build(
    interaction: discord.Interaction,
    action: app_commands.Choice[str],
    game: app_commands.Choice[str],
    build_name: str = None,
    details: str = None
):
    """Slash command pour gérer les builds"""
    
    if action.value == "list":
        # Lister les builds pour le jeu
        embed = discord.Embed(
            title=f"📋 Builds {game.name}",
            color=0x7289DA
        )
        
        # Simulation de builds existants
        builds = {
            "diablo4": ["🧙‍♂️ Necro Blood Surge", "🏹 Rogue Penetrating Shot", "🔮 Sorc Chain Lightning"],
            "tarkov": ["💀 Budget PMC", "👑 Chad Loadout", "🎯 Sniper Setup"],
            "wow_classic": ["🛡️ Prot Warrior", "❄️ Frost Mage", "🌿 Resto Druid"]
        }
        
        if game.value in builds:
            embed.description = "\n".join([f"• {build}" for build in builds[game.value]])
        else:
            embed.description = "Aucun build trouvé pour ce jeu."
        
        await interaction.response.send_message(embed=embed)
    
    elif action.value == "show":
        if not build_name:
            await interaction.response.send_message("❌ Nom du build requis pour l'affichage!", ephemeral=True)
            return
        
        # Afficher un build spécifique
        embed = discord.Embed(
            title=f"🔧 Build: {build_name}",
            description=f"Build pour {game.name}",
            color=0x00FF7F
        )
        
        # Exemple de build détaillé
        if game.value == "diablo4" and "necro" in build_name.lower():
            embed.add_field(name="⚔️ Compétences", value="• Blood Surge (MAX)\n• Corpse Explosion\n• Bone Armor", inline=True)
            embed.add_field(name="🛡️ Équipement", value="• Bloodless Scream\n• Temerity\n• Ring of Starless Skies", inline=True)
            embed.add_field(name="🎯 Stats Priorité", value="1. Vulnerable Damage\n2. Crit Strike Damage\n3. Core Skill Damage", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    elif action.value == "save":
        if not build_name or not details:
            await interaction.response.send_message("❌ Nom et détails du build requis pour la sauvegarde!", ephemeral=True)
            return
        
        # Sauvegarder le build
        embed = discord.Embed(
            title="💾 Build Sauvegardé",
            description=f"**{build_name}** pour {game.name}",
            color=0x00FF7F
        )
        embed.add_field(name="📝 Détails", value=details[:200] + "..." if len(details) > 200 else details, inline=False)
        embed.add_field(name="👤 Auteur", value=interaction.user.mention, inline=True)
        
        await interaction.response.send_message(embed=embed)

# ===============================
# 🎯 EXEMPLE 2: Slash Commands Événements
# ===============================

@app_commands.command(name="event", description="📅 Gérer les événements gaming")
@app_commands.describe(
    action="Action à effectuer",
    name="Nom de l'événement",
    game="Jeu de l'événement",
    date="Date (format: YYYY-MM-DD HH:MM)",
    max_players="Nombre maximum de joueurs"
)
@app_commands.choices(action=[
    app_commands.Choice(name="📅 Créer un événement", value="create"),
    app_commands.Choice(name="👁️ Voir les événements", value="list"),
    app_commands.Choice(name="✅ S'inscrire", value="join"),
    app_commands.Choice(name="❌ Se désinscrire", value="leave")
])
async def slash_event(
    interaction: discord.Interaction,
    action: app_commands.Choice[str],
    name: str = None,
    game: str = None,
    date: str = None,
    max_players: int = 10
):
    """Slash command pour gérer les événements"""
    
    if action.value == "create":
        if not name or not game or not date:
            await interaction.response.send_message("❌ Nom, jeu et date requis pour créer un événement!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"📅 Événement Créé: {name}",
            color=0x00FF7F,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="🎮 Jeu", value=game, inline=True)
        embed.add_field(name="📅 Date", value=date, inline=True)
        embed.add_field(name="👥 Joueurs Max", value=str(max_players), inline=True)
        embed.add_field(name="👤 Organisateur", value=interaction.user.mention, inline=True)
        
        # Ajouter boutons d'inscription
        from examples.modal_examples import EventRegistrationView
        view = EventRegistrationView()
        
        await interaction.response.send_message(embed=embed, view=view)
    
    elif action.value == "list":
        embed = discord.Embed(title="📅 Événements à Venir", color=0x7289DA)
        embed.add_field(name="🏰 Raid MC", value="WoW Classic - Demain 20h\n15/40 participants", inline=False)
        embed.add_field(name="🎯 Tournoi LoL", value="League of Legends - Samedi 14h\n8/16 équipes", inline=False)
        
        await interaction.response.send_message(embed=embed)

# ===============================
# 🎯 EXEMPLE 3: Slash Commands IA Gaming
# ===============================

@app_commands.command(name="ai", description="🤖 Assistant IA Gaming")
@app_commands.describe(
    question="Votre question gaming",
    context="Contexte spécifique (jeu, situation...)"
)
async def slash_ai(
    interaction: discord.Interaction,
    question: str,
    context: str = None
):
    """Slash command pour l'IA gaming"""
    
    # Defer pour éviter le timeout (réponse peut être longue)
    await interaction.response.defer()
    
    try:
        # Importer et utiliser l'IA
        from utils.gemini_ai import gemini_ai
        
        if gemini_ai.is_available():
            # Ajouter le contexte si fourni
            full_question = f"{question}"
            if context:
                full_question = f"Contexte: {context}\nQuestion: {question}"
            
            # Générer la réponse
            response = await gemini_ai.gaming_assistant(full_question)
            
            # Créer un embed pour la réponse
            embed = discord.Embed(
                title="🤖 MonBotGaming AI",
                color=0x7289DA,
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="❓ Question", value=question[:200] + "..." if len(question) > 200 else question, inline=False)
            
            # Diviser la réponse si trop longue
            if len(response) <= 1000:
                embed.add_field(name="💬 Réponse", value=response, inline=False)
                await interaction.followup.send(embed=embed)
            else:
                # Réponse longue - diviser en plusieurs messages
                embed.add_field(name="💬 Réponse", value=response[:1000] + "...", inline=False)
                await interaction.followup.send(embed=embed)
                
                # Envoyer le reste en messages simples
                remaining = response[1000:]
                while remaining:
                    chunk = remaining[:1900]
                    remaining = remaining[1900:]
                    await interaction.followup.send(chunk)
        else:
            embed = discord.Embed(
                title="❌ IA Indisponible",
                description="L'assistant IA est temporairement indisponible.",
                color=0xFF0000
            )
            await interaction.followup.send(embed=embed)
    
    except Exception as e:
        print(f"Erreur IA slash command: {e}")
        embed = discord.Embed(
            title="❌ Erreur",
            description="Une erreur s'est produite lors du traitement de votre question.",
            color=0xFF0000
        )
        await interaction.followup.send(embed=embed)

# ===============================
# 🎯 EXEMPLE 4: Slash Commands Stats
# ===============================

@app_commands.command(name="stats", description="📊 Voir les statistiques gaming")
@app_commands.describe(
    user="Utilisateur (optionnel, vous par défaut)",
    game="Jeu spécifique (optionnel, tous par défaut)"
)
async def slash_stats(
    interaction: discord.Interaction,
    user: discord.Member = None,
    game: str = None
):
    """Slash command pour voir les stats"""
    
    target_user = user or interaction.user
    
    embed = discord.Embed(
        title=f"📊 Stats Gaming - {target_user.display_name}",
        color=0x00FF7F,
        timestamp=discord.utils.utcnow()
    )
    
    embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)
    
    if game:
        # Stats pour un jeu spécifique
        embed.add_field(name=f"🎮 {game}", value="Temps: 120h\nVictoires: 45\nK/D: 2.3", inline=False)
    else:
        # Stats générales
        embed.add_field(name="🎮 Jeux Actifs", value="Diablo 4, WoW Classic, LoL", inline=False)
        embed.add_field(name="⏱️ Temps Total", value="450 heures", inline=True)
        embed.add_field(name="🏆 Achievements", value="23 débloqués", inline=True)
        embed.add_field(name="🥇 Rang Serveur", value="#15 sur 250", inline=True)
    
    await interaction.response.send_message(embed=embed)

# ===============================
# 🎯 EXEMPLE 5: Slash Commands Recherche d'Équipe
# ===============================

@app_commands.command(name="findteam", description="👥 Rechercher une équipe ou des coéquipiers")
@app_commands.describe(
    game="Jeu pour lequel vous cherchez",
    role="Votre rôle préféré",
    rank="Votre rang/niveau"
)
async def slash_findteam(
    interaction: discord.Interaction,
    game: str,
    role: str = None,
    rank: str = None
):
    """Slash command pour rechercher une équipe"""
    
    embed = discord.Embed(
        title="👥 Recherche d'Équipe",
        description=f"**{interaction.user.display_name}** recherche des coéquipiers !",
        color=0x00FF7F,
        timestamp=discord.utils.utcnow()
    )
    
    embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
    embed.add_field(name="🎮 Jeu", value=game, inline=True)
    embed.add_field(name="🎯 Rôle", value=role or "Flexible", inline=True)
    embed.add_field(name="🏆 Rang", value=rank or "Non spécifié", inline=True)
    
    # Boutons pour répondre
    from examples.modal_examples import TeamResponseView
    view = TeamResponseView(interaction.user.id)
    
    await interaction.response.send_message(embed=embed, view=view)

# ===============================
# 🎯 Configuration des Slash Commands
# ===============================

async def setup_slash_commands(bot):
    """Enregistrer les slash commands"""
    
    # Ajouter les commandes au bot
    bot.tree.add_command(slash_build)
    bot.tree.add_command(slash_event)
    bot.tree.add_command(slash_ai)
    bot.tree.add_command(slash_stats)
    bot.tree.add_command(slash_findteam)
    
    # Synchroniser avec Discord
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash commands synchronisées")
    except Exception as e:
        print(f"❌ Erreur sync slash commands: {e}")

# ===============================
# 🎯 Auto-complétion avancée
# ===============================

@slash_build.autocomplete('build_name')
async def build_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    """Auto-complétion pour les noms de builds"""
    
    # Simulation de builds existants basés sur le jeu sélectionné
    builds_db = {
        "diablo4": ["Necro Blood Surge", "Rogue Penetrating Shot", "Sorc Chain Lightning", "Barbarian Upheaval"],
        "tarkov": ["Budget PMC", "Chad Loadout", "Sniper Setup", "Pistol Run"],
        "wow_classic": ["Prot Warrior", "Frost Mage", "Resto Druid", "Combat Rogue"]
    }
    
    # Récupérer le jeu sélectionné (si possible)
    # Note: Dans un vrai scenario, on accéderait à la valeur du paramètre 'game'
    all_builds = []
    for game_builds in builds_db.values():
        all_builds.extend(game_builds)
    
    # Filtrer selon la saisie actuelle
    filtered_builds = [
        app_commands.Choice(name=build, value=build.lower().replace(" ", "_"))
        for build in all_builds
        if current.lower() in build.lower()
    ]
    
    # Retourner max 25 résultats (limite Discord)
    return filtered_builds[:25]

@slash_ai.autocomplete('context')
async def context_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    """Auto-complétion pour le contexte IA"""
    
    contexts = [
        "Diablo 4 - Build optimization",
        "WoW Classic - Raid strategy", 
        "Tarkov - Weapon builds",
        "LoL - Meta builds",
        "General gaming question",
        "PvP strategy",
        "PvE optimization",
        "Equipment recommendations"
    ]
    
    filtered_contexts = [
        app_commands.Choice(name=ctx, value=ctx)
        for ctx in contexts
        if current.lower() in ctx.lower()
    ]
    
    return filtered_contexts[:25]
