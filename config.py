# 🎮 Configuration MonBotGaming
# Configuration centralisée pour tous les jeux et paramètres

import discord
from discord.ext import commands

# ⚙️ Configuration du bot
BOT_CONFIG = {
    'prefix': '!',
    'description': 'Bot gaming communautaire pour serveur Discord',
    'case_insensitive': True,
    'intents': discord.Intents.all()
}

# 🎯 Jeux supportés avec leurs préfixes spéciaux
GAMES = {
    # RPG/Strategy
    'space_marine_2': {
        'name': 'Space Marine II',
        'prefix': '!sm2',
        'category': 'action_rpg',
        'emoji': '⚔️',
        'aliases': ['warhammer', 'sm2']
    },
    'baldurs_gate_3': {
        'name': "Baldur's Gate 3",
        'prefix': '!bg3',
        'category': 'rpg',
        'emoji': '🐉',
        'aliases': ['bg3', 'baldurs']
    },
    'diablo_4': {
        'name': 'Diablo IV',
        'prefix': '!d4',
        'category': 'arpg',
        'emoji': '👹',
        'aliases': ['diablo', 'd4', 'diablo4']
    },
    'wow_classic': {
        'name': 'WoW Classic',
        'prefix': '!wowc',
        'category': 'mmorpg',
        'emoji': '🏛️',
        'aliases': ['classic', 'wowc']
    },
    'wow_retail': {
        'name': 'WoW Retail',
        'prefix': '!wow',
        'category': 'mmorpg',
        'emoji': '🌍',
        'aliases': ['wow', 'retail']
    },
    'valheim': {
        'name': 'Valheim',
        'prefix': '!val',
        'category': 'survival',
        'emoji': '🪓',
        'aliases': ['val', 'valheim']
    },
    'enshrouded': {
        'name': 'Enshrouded',
        'prefix': '!ens',
        'category': 'survival',
        'emoji': '🌫️',
        'aliases': ['ens', 'enshrouded']
    },
    
    # Action/FPS
    'escape_from_tarkov': {
        'name': 'Escape from Tarkov',
        'prefix': '!eft',
        'category': 'fps',
        'emoji': '🔫',
        'aliases': ['tarkov', 'eft']
    },
    'helldivers_2': {
        'name': 'Helldivers 2',
        'prefix': '!hd2',
        'category': 'coop_shooter',
        'emoji': '🚀',
        'aliases': ['helldivers', 'hd2']
    },
    
    # Multijoueur/Compétitif
    'league_of_legends': {
        'name': 'League of Legends',
        'prefix': '!lol',
        'category': 'moba',
        'emoji': '⚡',
        'aliases': ['lol', 'league']
    },
    'rocket_league': {
        'name': 'Rocket League',
        'prefix': '!rl',
        'category': 'sports',
        'emoji': '⚽',
        'aliases': ['rl', 'rocket']
    },
    'sea_of_thieves': {
        'name': 'Sea of Thieves',
        'prefix': '!sot',
        'category': 'adventure',
        'emoji': '🏴‍☠️',
        'aliases': ['sot', 'pirates']
    },
    
    # Cartes/Stratégie
    'mtg_arena': {
        'name': 'MTG Arena',
        'prefix': '!mtg',
        'category': 'card_game',
        'emoji': '🃏',
        'aliases': ['mtg', 'magic']
    },
    'waven': {
        'name': 'Waven',
        'prefix': '!waven',
        'category': 'card_game',
        'emoji': '🎴',
        'aliases': ['waven']
    },
    
    # Autres
    'raft': {
        'name': 'Raft',
        'prefix': '!raft',
        'category': 'survival',
        'emoji': '🛟',
        'aliases': ['raft']
    },
    'grounded': {
        'name': 'Grounded',
        'prefix': '!ground',
        'category': 'survival',
        'emoji': '🐜',
        'aliases': ['grounded', 'ground']
    },
    'jdr': {
        'name': 'Jeu de Rôle',
        'prefix': '!jdr',
        'category': 'roleplay',
        'emoji': '🎭',
        'aliases': ['jdr', 'roleplay', 'rp']
    }
}

# 📺 Configuration des channels Discord
CHANNELS_CONFIG = {
    'builds': 'builds-et-strats',
    'events': 'evenements-gaming',
    'general': 'general-gaming',
    'announcements': 'annonces-bot',
    'logs': 'logs-bot'
}

# 🏆 Système de rôles gaming
GAMING_ROLES = {
    'gamer': 'Gamer',
    'veteran': 'Vétéran Gaming',
    'leader': 'Chef de Raid',
    'streamer': 'Streamer',
    'helper': 'Assistant Gaming'
}

# 🎨 Couleurs pour les embeds Discord
COLORS = {
    'success': 0x00ff00,
    'error': 0xff0000,
    'warning': 0xffff00,
    'info': 0x0099ff,
    'gaming': 0x9932cc,
    'build': 0xff6347,
    'event': 0x32cd32,
    'fun': 0xffa500
}

# 🔧 Utilitaires de configuration
def get_game_by_alias(alias):
    """Trouve un jeu par son alias ou nom"""
    alias = alias.lower()
    for game_id, game_data in GAMES.items():
        if alias in [a.lower() for a in game_data['aliases']] or alias == game_data['name'].lower():
            return game_id, game_data
    return None, None

def get_games_by_category(category):
    """Récupère tous les jeux d'une catégorie"""
    return {k: v for k, v in GAMES.items() if v['category'] == category}

def get_all_categories():
    """Liste toutes les catégories de jeux"""
    return list(set(game['category'] for game in GAMES.values()))

# 🎲 Configuration des mini-jeux
MINIGAMES_CONFIG = {
    'dice_sides': [4, 6, 8, 10, 12, 20, 100],
    'quiz_categories': ['lore', 'gameplay', 'items', 'characters'],
    'loot_rarities': ['common', 'uncommon', 'rare', 'epic', 'legendary']
}

# 🔒 Configuration RGPD
RGPD_CONFIG = {
    'memory_duration_hours': 48,
    'consent_duration_days': 30
}
