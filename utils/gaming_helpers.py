# 🎮 Utilitaires Gaming pour MonBotGaming
# Fonctions spécialisées pour les fonctionnalités gaming

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import random
import re
from typing import Dict, List, Optional, Tuple
from config import GAMES, COLORS

class GamingHelpers:
    """Collection d'utilitaires pour les fonctionnalités gaming"""
    
    @staticmethod
    def create_gaming_embed(title: str, description: str = "", color: str = 'gaming', 
                           game: Optional[str] = None) -> discord.Embed:
        """Crée un embed Discord stylé pour le gaming"""
        embed_color = COLORS.get(color, COLORS['gaming'])
        embed = discord.Embed(title=title, description=description, color=embed_color)
        
        if game and game in GAMES:
            game_data = GAMES[game]
            embed.set_author(name=f"{game_data['emoji']} {game_data['name']}")
        
        embed.timestamp = datetime.now()
        return embed
    
    @staticmethod
    def create_build_embed(game: str, build_name: str, build_data: Dict) -> discord.Embed:
        """Crée un embed spécialisé pour afficher un build"""
        game_data = GAMES.get(game, {})
        embed = GamingHelpers.create_gaming_embed(
            title=f"🛠️ Build: {build_name}",
            color='build',
            game=game
        )
        
        # Informations de base
        embed.add_field(
            name="📋 Description",
            value=build_data.get('description', 'Aucune description'),
            inline=False
        )
        
        # Auteur et date
        author = build_data.get('author', 'Inconnu')
        created_date = build_data.get('created_date', 'Inconnue')
        embed.add_field(
            name="👤 Créé par",
            value=f"{author}\n📅 {created_date}",
            inline=True
        )
        
        # Popularité
        likes = build_data.get('likes', 0)
        uses = build_data.get('uses', 0)
        embed.add_field(
            name="📊 Statistiques",
            value=f"👍 {likes} likes\n🎯 {uses} utilisations",
            inline=True
        )
        
        return embed
    
    @staticmethod
    def create_event_embed(event_data: Dict) -> discord.Embed:
        """Crée un embed pour afficher un événement"""
        embed = GamingHelpers.create_gaming_embed(
            title=f"📅 {event_data.get('title', 'Événement')}",
            description=event_data.get('description', ''),
            color='event',
            game=event_data.get('game')
        )
        
        # Date et heure
        event_date = event_data.get('date', 'Non définie')
        embed.add_field(
            name="📅 Date & Heure",
            value=event_date,
            inline=True
        )
        
        # Participants
        participants = event_data.get('participants', [])
        max_participants = event_data.get('max_participants', 'Illimité')
        embed.add_field(
            name="👥 Participants",
            value=f"{len(participants)}/{max_participants}",
            inline=True
        )
        
        # Organisateur
        organizer = event_data.get('organizer', 'Inconnu')
        embed.add_field(
            name="🎯 Organisateur",
            value=organizer,
            inline=True
        )
        
        return embed
    
    @staticmethod
    def parse_game_from_message(message: str) -> Tuple[Optional[str], Optional[Dict]]:
        """Extrait le jeu mentionné dans un message"""
        message_lower = message.lower()
        
        for game_id, game_data in GAMES.items():
            # Vérifier les alias
            for alias in game_data['aliases']:
                if alias.lower() in message_lower:
                    return game_id, game_data
            
            # Vérifier le nom complet
            if game_data['name'].lower() in message_lower:
                return game_id, game_data
        
        return None, None
    
    @staticmethod
    def format_build_list(builds: Dict, game: str) -> str:
        """Formate une liste de builds pour affichage"""
        if not builds:
            return "Aucun build trouvé pour ce jeu."
        
        game_data = GAMES.get(game, {})
        lines = [f"{game_data.get('emoji', '🎮')} **{game_data.get('name', game)}**\n"]
        
        for build_name, build_data in builds.items():
            author = build_data.get('author', 'Inconnu')
            likes = build_data.get('likes', 0)
            lines.append(f"• **{build_name}** by {author} (👍 {likes})")
        
        return "\n".join(lines)
    
    @staticmethod
    def validate_build_data(build_data: Dict) -> Tuple[bool, str]:
        """Valide les données d'un build"""
        required_fields = ['name', 'description', 'author']
        
        for field in required_fields:
            if field not in build_data or not build_data[field].strip():
                return False, f"Le champ '{field}' est requis."
        
        # Vérifier la longueur des champs
        if len(build_data['name']) > 50:
            return False, "Le nom du build ne peut pas dépasser 50 caractères."
        
        if len(build_data['description']) > 1000:
            return False, "La description ne peut pas dépasser 1000 caractères."
        
        return True, "Données valides"
    
    @staticmethod
    def generate_loot_item(game: str, rarity: str = None) -> Dict:
        """Génère un objet de loot aléatoire pour un jeu"""
        rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary']
        if not rarity:
            rarity = random.choices(rarities, weights=[40, 30, 20, 8, 2])[0]
        
        # Templates d'objets par jeu
        loot_templates = {
            'diablo_4': {
                'weapons': ['Épée', 'Hache', 'Arc', 'Bâton', 'Dague'],
                'armor': ['Casque', 'Plastron', 'Gants', 'Bottes'],
                'prefixes': ['Ancien', 'Maudit', 'Béni', 'Infernal', 'Divin']
            },
            'escape_from_tarkov': {
                'weapons': ['AK-74', 'M4A1', 'VSS', 'MP7', 'Mosin'],
                'armor': ['Casque', 'Gilet pare-balles', 'Rig tactique'],
                'prefixes': ['Militaire', 'Renforcé', 'Tactique', 'Blindé']
            }
        }
        
        game_loot = loot_templates.get(game, loot_templates['diablo_4'])
        
        item_type = random.choice(['weapons', 'armor'])
        item_name = random.choice(game_loot[item_type])
        prefix = random.choice(game_loot['prefixes'])
        
        return {
            'name': f"{prefix} {item_name}",
            'rarity': rarity,
            'type': item_type,
            'game': game,
            'generated_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def roll_dice(sides: int, count: int = 1) -> Dict:
        """Lance des dés et retourne les résultats"""
        if sides not in [4, 6, 8, 10, 12, 20, 100]:
            sides = 20
        
        if count < 1 or count > 10:
            count = 1
        
        rolls = [random.randint(1, sides) for _ in range(count)]
        
        return {
            'rolls': rolls,
            'total': sum(rolls),
            'sides': sides,
            'count': count,
            'average': sum(rolls) / len(rolls)
        }
    
    @staticmethod
    def format_time_until(target_time: datetime) -> str:
        """Formate le temps restant jusqu'à une date"""
        now = datetime.now()
        if target_time <= now:
            return "⏰ Maintenant !"
        
        delta = target_time - now
        
        if delta.days > 0:
            return f"⏰ Dans {delta.days}j {delta.seconds // 3600}h"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f"⏰ Dans {hours}h {minutes}m"
        else:
            minutes = delta.seconds // 60
            return f"⏰ Dans {minutes}m"

# Instance globale des helpers
gaming_helpers = GamingHelpers()
