# 🎨 Utilitaire pour les embeds riches MonBotGaming

import discord
from datetime import datetime

def create_ai_response_embed(question, response, context=None):
    """Créer un embed stylé pour les réponses IA gaming"""
    
    embed = discord.Embed(
        title="🤖 MonBotGaming AI - Assistant Gaming",
        color=0x7289DA,  # Bleu Discord
        timestamp=datetime.now()
    )
    
    # Ajouter le contexte si fourni
    if context:
        embed.add_field(name="🎮 Contexte", value=context, inline=False)
    
    # Question (limitée à 200 chars pour l'affichage)
    question_text = question[:200] + "..." if len(question) > 200 else question
    embed.add_field(name="❓ Question", value=question_text, inline=False)
    
    # Réponse (laisse la gestion de la longueur à l'appelant)
    embed.add_field(name="💬 Réponse", value=response, inline=False)
    
    embed.set_footer(text="Powered by Gemini AI • Gaming Assistant", icon_url=None)
    
    return embed

def create_gaming_embed(title, description, color='default', game=None):
    """Créer un embed gaming avec thème selon le jeu"""
    
    # Couleurs par jeu
    colors = {
        'diablo': 0x8B0000,      # Rouge sang
        'wow': 0xFFD700,         # Or
        'tarkov': 0x2F3136,      # Gris foncé
        'lol': 0x0F1B3C,        # Bleu foncé LoL
        'valheim': 0x4A5D23,    # Vert forêt
        'bg3': 0x8B4513,        # Brun aventure
        'default': 0x7289DA,     # Bleu Discord
        'success': 0x00FF7F,     # Vert success
        'warning': 0xFFA500,     # Orange warning
        'error': 0xFF0000,       # Rouge erreur
        'info': 0x7289DA         # Bleu info
    }
    
    # Déterminer la couleur
    if game and game.lower() in colors:
        embed_color = colors[game.lower()]
    elif color in colors:
        embed_color = colors[color]
    else:
        embed_color = colors['default']
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=embed_color,
        timestamp=datetime.now()
    )
    
    return embed

def create_help_embed(commands_list, category="Gaming"):
    """Créer un embed d'aide stylé"""
    
    embed = discord.Embed(
        title=f"🎮 {category} - Commandes Disponibles",
        description="Voici les commandes que tu peux utiliser :",
        color=0x7289DA,
        timestamp=datetime.now()
    )
    
    for cmd_name, cmd_desc in commands_list.items():
        embed.add_field(name=f"**{cmd_name}**", value=cmd_desc, inline=False)
    
    embed.set_footer(text="MonBotGaming • Assistant Gaming")
    
    return embed

def create_status_embed(service_name, is_available, details=None):
    """Créer un embed de statut de service"""
    
    status_color = 0x00FF7F if is_available else 0xFF0000
    status_text = "🟢 En ligne" if is_available else "🔴 Hors ligne"
    
    embed = discord.Embed(
        title=f"📊 Statut - {service_name}",
        color=status_color,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="État", value=status_text, inline=True)
    
    if details:
        embed.add_field(name="Détails", value=details, inline=False)
    
    return embed
