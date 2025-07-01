# 🎨 Utilitaire pour les embeds riches MonBotGaming

import discord
from datetime import datetime
from typing import Union, Optional

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

async def send_long_response(target: Union[discord.Message, discord.Interaction], 
                           response: str, 
                           embed: Optional[discord.Embed] = None,
                           max_embed_length: int = 1000,
                           max_simple_length: int = 1500,
                           chunk_size: int = 1900):
    """
    Gère l'envoi de réponses longues avec troncature intelligente
    
    Args:
        target: Message Discord ou Interaction à répondre
        response: Texte de la réponse
        embed: Embed optionnel à utiliser
        max_embed_length: Longueur max dans un embed
        max_simple_length: Longueur max pour réponse simple
        chunk_size: Taille des chunks pour messages multiples
    """
    try:
        is_message = isinstance(target, discord.Message)
        
        if embed:
            # Mode embed
            if len(response) <= max_embed_length:
                embed.description = response
                if is_message:
                    await target.reply(embed=embed)
                else:
                    await target.response.send_message(embed=embed)
            else:
                # Embed + messages supplémentaires
                embed.description = response[:max_embed_length]
                embed.set_footer(text="Suite de la réponse dans les messages suivants...")
                
                if is_message:
                    await target.reply(embed=embed)
                    channel = target.channel
                else:
                    await target.response.send_message(embed=embed)
                    channel = target.channel
                
                # Envoyer le reste en chunks
                remaining = response[max_embed_length:]
                while remaining:
                    chunk = remaining[:chunk_size]
                    remaining = remaining[chunk_size:]
                    if hasattr(channel, 'send'):
                        await channel.send(f"```{chunk}```")
        else:
            # Mode message simple
            if len(response) <= max_simple_length:
                if is_message:
                    await target.reply(response)
                else:
                    await target.response.send_message(response)
            else:
                # Message tronqué
                truncated = response[:max_simple_length] + "..."
                if is_message:
                    await target.reply(truncated)
                else:
                    await target.response.send_message(truncated)
                    
    except discord.HTTPException as e:
        print(f"Erreur Discord lors de l'envoi de la réponse longue: {e}")
        error_msg = "❌ Une erreur de communication Discord s'est produite."
        try:
            is_message = isinstance(target, discord.Message)
            if is_message:
                await target.reply(error_msg)
            else:
                await target.response.send_message(error_msg)
        except discord.HTTPException:
            pass
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse longue: {e}")
        error_msg = "❌ Une erreur s'est produite lors de l'envoi de la réponse."
        try:
            is_message = isinstance(target, discord.Message)
            if is_message:
                await target.reply(error_msg)
            else:
                await target.response.send_message(error_msg)
        except discord.HTTPException:
            pass

async def send_ai_response(target: Union[discord.Message, discord.Interaction],
                          question: str,
                          response: str,
                          use_embed: bool = True,
                          embed_type: str = 'full',
                          context: Optional[str] = None):
    """
    Gère l'envoi complet d'une réponse IA selon le type
    
    Args:
        target: Message Discord ou Interaction à répondre
        question: Question posée
        response: Réponse de l'IA
        use_embed: Utiliser un embed ou non
        embed_type: Type d'embed ('full', 'light', 'none')
        context: Contexte optionnel
    """
    try:
        if embed_type == 'light':
            # Embed simple sans fioritures
            simple_embed = discord.Embed(
                description=response[:1000] if len(response) <= 1000 else response[:1000] + "...",
                color=0x00ff88
            )
            await send_long_response(target, response, embed=simple_embed)
            
        elif use_embed and embed_type == 'full':
            # Embed complet
            response_embed = create_ai_response_embed(question, response, context)
            await send_long_response(target, response, embed=response_embed)
            
        else:
            # Réponse simple sans embed
            await send_long_response(target, response)
            
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse IA: {e}")
        error_msg = "🎮 Une erreur s'est produite lors de la génération de la réponse."
        try:
            if hasattr(target, 'reply'):
                await target.reply(error_msg)
            else:
                await target.response.send_message(error_msg)
        except discord.HTTPException:
            pass

def truncate_response(response: str, max_length: int = 1000, add_ellipsis: bool = True) -> str:
    """
    Tronque intelligemment une réponse
    
    Args:
        response: Texte à tronquer
        max_length: Longueur maximale
        add_ellipsis: Ajouter "..." si tronqué
    
    Returns:
        Texte tronqué
    """
    if len(response) <= max_length:
        return response
    
    if add_ellipsis:
        return response[:max_length] + "..."
    else:
        return response[:max_length]
