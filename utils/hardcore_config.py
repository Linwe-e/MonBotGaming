# 🎮 Configuration IA Hardcore pour MonBotGaming
# Personnalisations spécifiques par jeu pour ton serveur

HARDCORE_GAMING_CONFIG = {
    # Vocabulaire technique spécialisé par jeu
    'game_vocabulary': {
        'diablo': ['paragon boards', 'aspect rolls', 'nightmare dungeons', 'malignant hearts', 'torment tiers'],
        'tarkov': ['meta ammo', 'armor penetration', 'ergo/recoil builds', 'hideout optimization', 'flea market flips'],
        'wow': ['sim results', 'stat weights', 'rotation priorities', 'weak auras', 'mythic+ routes'],
        'helldivers': ['stratagems timing', 'reinforcement efficiency', 'extract optimization', 'friendly fire management'],
        'baldurs_gate': ['multiclass synergies', 'action economy', 'spell slot optimization', 'save-or-suck spells'],
        'lol': ['wave management', 'jungle pathing', 'item spike timings', 'teamfight positioning', 'macro rotations']
    },
    
    # Niveau de technicité par type de requête
    'technicality_levels': {
        'build_analysis': 'EXTREME',  # Calculs poussés, théorycrafting
        'team_composition': 'HIGH',   # Stratégies meta avancées
        'general_question': 'HIGH',   # Pas de conseils évidents
        'event_description': 'MEDIUM' # Hype mais accessible
    },
    
    # Prompts spéciaux pour certains jeux
    'game_specific_prompts': {
        'diablo': """
        Focus sur :
        - Paragon board optimizations et glyph placements
        - Aspect priority et stat roll ranges
        - Nightmare dungeon efficiency et speed farming
        - Endgame progression paths et season meta
        """,
        
        'tarkov': """
        Focus sur :
        - Meta ammo charts et armor penetration values
        - Ergo/recoil stat optimization pour different ranges
        - Hideout upgrade priorities pour profit margins
        - Map-specific loot routes et PvP positioning
        """,
        
        'wow': """
        Focus sur :
        - SimCraft results et stat weight priorities
        - Rotation optimizations et spell priority systems
        - M+ route efficiency et pull strategies
        - Raid encounter mechanics et positioning guides
        """,
        
        'helldivers': """
        Focus sur :
        - Stratagem timing optimization et combo sequences
        - Mission efficiency routes et extract positioning
        - Difficulty scaling strategies et team coordination
        - Equipment synergies et loadout optimization
        """
    },
    
    # Ton et style pour hardcore gamers
    'hardcore_style': {
        'vocabulary': 'technical',      # Utilise le jargon gaming
        'assume_knowledge': True,       # Pas d'explications basiques
        'provide_numbers': True,        # Chiffres et calculs précis
        'mention_meta': True,          # Références au meta actuel
        'advanced_strategies': True,    # Stratégies pro-level
        'edge_cases': True             # Mentions des edge cases
    }
}
