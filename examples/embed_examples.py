# 🎮 Exemples d'Embeds Riches pour MonBotGaming

import discord
from datetime import datetime

# ===============================
# 🎯 EXEMPLE 1: Build Diablo 4
# ===============================

def create_diablo_build_embed(build_data):
    """Créer un embed stylé pour un build Diablo 4"""
    
    embed = discord.Embed(
        title="🔥 Build Necromancer - Blood Surge",
        description="Build hardcore pour Tier 100+ optimisé DPS",
        color=0x8B0000,  # Rouge sang pour Diablo
        timestamp=datetime.now()
    )
    
    # Image principale (classe Necromancer)
    embed.set_thumbnail(url="https://diablo4.wiki.fextralife.com/file/Diablo-4/necromancer-class-diablo-4-wiki-guide.jpg")
    
    # Champs organisés
    embed.add_field(
        name="⚔️ Compétences Principales", 
        value="• Blood Surge (MAX)\n• Corpse Explosion\n• Bone Armor\n• Blood Mist", 
        inline=True
    )
    
    embed.add_field(
        name="🛡️ Équipement Key", 
        value="• Bloodless Scream (Arme)\n• Temerity (Pantalon)\n• Ring of Starless Skies", 
        inline=True
    )
    
    embed.add_field(
        name="🎯 Stats Priorité", 
        value="1. Vulnerable Damage\n2. Critical Strike Damage\n3. Core Skill Damage\n4. Lucky Hit Chance", 
        inline=False
    )
    
    # Paragon board
    embed.add_field(
        name="🌟 Paragon Boards", 
        value="Starter → Blood Begets Blood → Bone Graft → Cult Leader", 
        inline=False
    )
    
    # Footer avec auteur
    embed.set_footer(
        text=f"Build créé par {build_data['author']} | Testé Tier 95+",
        icon_url="https://cdn.discordapp.com/emojis/gameplay.png"
    )
    
    return embed

# ===============================
# 🎯 EXEMPLE 2: Événement WoW
# ===============================

def create_wow_raid_embed(event_data):
    """Embed pour un événement raid WoW"""
    
    embed = discord.Embed(
        title="🏰 Raid Molten Core - WoW Classic",
        description="Raid légendaire pour équipement Tier 1",
        color=0xFFD700,  # Or pour WoW
        timestamp=datetime.fromisoformat(event_data['date'])
    )
    
    # Image du raid
    embed.set_image(url="https://wow.wiki.fextralife.com/file/WoW/molten_core_entrance.jpg")
    
    # Informations pratiques
    embed.add_field(name="📅 Date", value=f"<t:{int(datetime.fromisoformat(event_data['date']).timestamp())}:F>", inline=True)
    embed.add_field(name="👥 Participants", value=f"{len(event_data['participants'])}/40", inline=True)
    embed.add_field(name="⏱️ Durée Estimée", value="2h30 - 3h00", inline=True)
    
    # Composition souhaitée
    embed.add_field(
        name="🛡️ Composition Requise",
        value="• **Tanks:** 3-4 (Warrior conseillé)\n• **Healers:** 8-10 (Priest/Paladin)\n• **DPS:** 25-30 (Mage/Warlock/Rogue)",
        inline=False
    )
    
    # Prérequis
    embed.add_field(
        name="✅ Prérequis",
        value="• Niveau 60 minimum\n• Résistance Feu 250+\n• Flasks/Potions préparées\n• Discord obligatoire",
        inline=False
    )
    
    return embed

# ===============================
# 🎯 EXEMPLE 3: Stats Gaming
# ===============================

def create_player_stats_embed(user_data):
    """Stats gaming d'un joueur"""
    
    embed = discord.Embed(
        title=f"📊 Stats Gaming - {user_data['username']}",
        color=0x00FF7F,  # Vert gaming
        timestamp=datetime.now()
    )
    
    # Avatar du joueur
    embed.set_thumbnail(url=user_data['avatar_url'])
    
    # Stats par jeu
    for game, stats in user_data['games'].items():
        embed.add_field(
            name=f"🎮 {game}",
            value=f"Temps: {stats['hours']}h\nVictoires: {stats['wins']}\nK/D: {stats['kd_ratio']}",
            inline=True
        )
    
    # Achievements récents
    if user_data['recent_achievements']:
        achievements_text = "\n".join([f"🏆 {ach}" for ach in user_data['recent_achievements'][:3]])
        embed.add_field(name="🏆 Achievements Récents", value=achievements_text, inline=False)
    
    return embed

# ===============================
# 🎯 EXEMPLE 4: IA Gaming Response
# ===============================

def create_ai_response_embed(question, response):
    """Embed pour les réponses IA gaming"""
    
    embed = discord.Embed(
        title="🤖 MonBotGaming AI - Assistant Gaming",
        color=0x7289DA,  # Bleu Discord
        timestamp=datetime.now()
    )
    
    embed.add_field(name="❓ Question", value=question[:200] + "..." if len(question) > 200 else question, inline=False)
    embed.add_field(name="💬 Réponse", value=response[:1000] + "..." if len(response) > 1000 else response, inline=False)
    
    embed.set_footer(text="Powered by Gemini AI • Gaming Assistant", icon_url="🤖")
    
    return embed
