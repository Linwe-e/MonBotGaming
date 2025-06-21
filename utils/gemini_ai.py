# 🤖 Gestionnaire Gemini AI pour MonBotGaming
# Interface intelligente pour l'assistance gaming

import google.generativeai as genai
import os
from typing import Optional, Dict, List
from dotenv import load_dotenv

load_dotenv()

class GeminiAI:
    """
    Interface Gemini AI spécialisée pour le gaming
    Adaptation du pattern IA de Rhodham96/DiscordBot
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self._is_valid_api_key(self.api_key):
            try:
                genai.configure(api_key=self.api_key)
                # Utilisation de Gemini 2.0 Flash (version stable gratuite)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.available = True
            except Exception as e:
                print(f"⚠️ Erreur configuration Gemini 2.0: {e}")
                self.available = False
        else:
            self.available = False
    
    def _is_valid_api_key(self, api_key: str) -> bool:
        """
        Valide la clé API de manière sécurisée
        """
        if not api_key:
            return False
        
        # Vérifications de format basiques pour une clé Gemini
        if len(api_key) < 20:  # Les clés Gemini sont plus longues
            return False
            
        if not api_key.startswith('AIza'):  # Format typique des clés Google AI
            return False
            
        # Pas de caractères suspects ou de placeholders évidents
        forbidden_patterns = ['exemple', 'test', 'placeholder', 'ici', 'cle', 'key']
        api_key_lower = api_key.lower()
        
        for pattern in forbidden_patterns:
            if pattern in api_key_lower:
                return False
        
        return True
    
    def is_available(self) -> bool:
        """
        Vérifie si l'IA est disponible et configurée
        """
        return self.available
    
    async def gaming_assistant(self, question: str, game_context: str = None) -> str:
        """
        Assistant gaming principal utilisant Gemini 2.0 Flash
        """
        if not self.available:
            return "❌ Gemini AI non configuré - Configure ta clé GEMINI_API_KEY dans .env"
        
        # Construire le prompt avec contexte gaming
        game_prompt = f"\n🎮 Contexte de jeu : {game_context}" if game_context else ""
        
        prompt = f"""
        🎮 ASSISTANT GAMING EXPERT

        Question : {question}{game_prompt}

        Tu es un expert gaming spécialisé dans :
        • 🏗️ Builds et optimisations
        • 🎯 Stratégies et tactiques  
        • 👥 Compositions d'équipe
        • 📊 Meta et mécaniques de jeu
        • 🎲 Conseils pour débutants/experts

        Donne une réponse pratique et utile pour un joueur :
        • 💡 Conseils concrets
        • 📊 Informations précises  
        • 🎯 Actions recommandées

        Réponds en français, 200 mots max, avec des emojis gaming.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Erreur Gemini 2.0 : {str(e)}"
    
    async def analyze_build(self, build_description: str, game: str = None) -> str:
        """
        Analyse un build de jeu avec Gemini 2.0
        """
        if not self.available:
            return "❌ Gemini AI non configuré pour l'analyse de builds"
        
        game_context = f" pour {game}" if game else ""
        
        prompt = f"""
        🔧 ANALYSTE DE BUILD GAMING

        Build{game_context} :
        {build_description}

        Analyse ce build en détail :
        • ⚡ Forces et points forts
        • ⚠️ Faiblesses ou points d'amélioration
        • 🎯 Utilisation optimale (situations/activités)
        • 💡 Suggestions d'amélioration
        • 📊 Note générale /10

        Sois constructif et précis. 250 mots max avec emojis gaming.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Erreur lors de l'analyse du build : {str(e)}"
    
    async def suggest_team_composition(self, game: str, activity: str, players: str) -> str:
        """
        Suggère des compositions d'équipe optimales avec Gemini 2.0
        """
        if not self.available:
            return "❌ Gemini AI non configuré pour les suggestions d'équipe"
        
        prompt = f"""
        🎮 STRATÈGE D'ÉQUIPE GAMING

        Jeu : {game}
        Activité : {activity}  
        Joueurs : {players}

        Propose la composition optimale :
        • 👥 Rôles recommandés et répartition
        • ⚔️ Responsabilités par joueur
        • 🎯 Stratégies et synergies
        • 💡 Conseils tactiques spécifiques

        200 mots max, avec emojis de rôles appropriés.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Erreur lors de la suggestion d'équipe : {str(e)}"
    
    async def generate_event_description(self, game: str, event_type: str, details: Dict) -> str:
        """
        Génère une description d'événement gaming attractive avec Gemini 2.0
        """
        if not self.available:
            return f"📅 Événement {event_type} pour {game}"
        
        prompt = f"""
        🎮 CRÉATEUR D'ÉVÉNEMENT GAMING

        Jeu : {game}
        Type : {event_type}
        Détails : {details}

        Crée une description attractive qui :
        • 🔥 Excite et motive les joueurs
        • 🎯 Présente clairement les objectifs
        • ⏰ Donne les infos pratiques
        • 🏆 Met en avant les récompenses/enjeux

        150 mots max, avec emojis gaming appropriés.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"📅 Événement {event_type} pour {game} - {details.get('title', 'Session gaming')}"

    def _detect_message_type(self, message: str) -> str:
        """
        Détecte le type de message avec analyse contextuelle avancée
        """
        message_lower = message.lower().strip()
        
        # Analyse de la structure et du contenu
        has_greeting = any(word in message_lower for word in 
                          ['salut', 'bonjour', 'bonsoir', 'hello', 'hey', 'hi', 'coucou'])
        
        # Mots-clés techniques gaming (plus exhaustifs)
        tech_keywords = [
            # Builds et optimisation
            'build', 'dps', 'optimization', 'meta', 'scaling', 'stats', 'rotation', 
            'damage', 'gear', 'équipement', 'config', 'setup', 'loadout',
            # Gameplay technique
            'stratégie', 'tactique', 'combo', 'timing', 'frame', 'hitbox',
            'farm', 'grind', 'efficiency', 'min-max', 'théorycraft',
            # Performance et compétition
            'rank', 'mmr', 'elo', 'winrate', 'pro', 'tournament', 'comp',
            # Mécaniques de jeu
            'buff', 'debuff', 'proc', 'cooldown', 'mana', 'resource',
            'crit', 'penetration', 'resistance', 'armor', 'magic find'
        ]
        
        # Noms de jeux spécifiques
        game_names = [
            'diablo', 'tarkov', 'wow', 'lol', 'valorant', 'eft', 'bg3',
            'helldivers', 'warhammer', 'valheim', 'destiny', 'poe'
        ]
        
        # Questions d'aide/conseil
        help_patterns = [
            'comment', 'aide', 'help', 'conseil', 'suggestion', 'recommand',
            'que faire', 'how to', 'what should', 'meilleur', 'optimal'
        ]
        
        # Analyse intelligente du contenu technique
        tech_score = sum(1 for keyword in tech_keywords if keyword in message_lower)
        game_score = sum(1 for game in game_names if game in message_lower)
        help_score = sum(1 for pattern in help_patterns if pattern in message_lower)
        
        # Structure du message
        has_question_mark = '?' in message
        message_length = len(message.split())
        
        # Logique de décision contextuelle
        total_technical_content = tech_score + game_score + help_score
        
        # Salutation pure sans contenu technique
        if has_greeting and total_technical_content == 0 and message_length <= 4:
            if any(phrase in message_lower for phrase in 
                  ['comment vas-tu', 'ça va', 'comment allez-vous', 'how are you']):
                return 'greeting_question'
            return 'greeting'
        
        # Salutations + questions techniques = priorité technique avec politesse
        if has_greeting and total_technical_content >= 2:
            return 'technical_with_greeting'
        
        # Contenu clairement technique (même sans salutation)
        if total_technical_content >= 3 or (tech_score >= 2 and game_score >= 1):
            return 'technical'
        
        # Question d'aide générale
        if (has_question_mark or help_score >= 1) and total_technical_content >= 1:
            return 'question_with_context'
        
        # Question simple
        if has_question_mark or help_score >= 1:
            return 'question'
        
        return 'general'
        
# Instance globale
gemini_ai = GeminiAI()
