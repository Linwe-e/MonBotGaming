"""
🧠 Conversation Memory System pour MonBotGaming
Garde en mémoire les conversations pour des réponses plus naturelles
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio

class ConversationMemory:
    """Gestionnaire de mémoire conversationnelle"""
    
    def __init__(self, memory_file: str = "data/conversation_memory.json"):
        self.memory_file = memory_file
        self.conversations: Dict[str, List[Dict]] = {}
        self.max_history_per_user = 10  # Limiter la mémoire
        self.memory_duration_hours = 24  # Oublier après 24h
        self.load_memory()
    
    def load_memory(self):
        """Charge la mémoire depuis le fichier"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations = data.get('conversations', {})
                    self.cleanup_old_memories()
        except Exception as e:
            print(f"Erreur chargement mémoire: {e}")
            self.conversations = {}
    
    def save_memory(self):
        """Sauvegarde la mémoire dans le fichier"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'conversations': self.conversations,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde mémoire: {e}")
    
    def cleanup_old_memories(self):
        """Supprime les souvenirs trop anciens"""
        cutoff = datetime.now() - timedelta(hours=self.memory_duration_hours)
        
        for user_id in list(self.conversations.keys()):
            # Filtrer les messages récents
            self.conversations[user_id] = [
                msg for msg in self.conversations[user_id]
                if datetime.fromisoformat(msg['timestamp']) > cutoff
            ]
            
            # Supprimer les utilisateurs sans historique
            if not self.conversations[user_id]:
                del self.conversations[user_id]
    
    def add_message(self, user_id: str, content: str, is_bot: bool = False, context: Dict = None):
        """Ajoute un message à l'historique"""
        user_id = str(user_id)
        
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        message = {
            'content': content,
            'is_bot': is_bot,
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        self.conversations[user_id].append(message)
        
        # Limiter l'historique
        if len(self.conversations[user_id]) > self.max_history_per_user:
            self.conversations[user_id] = self.conversations[user_id][-self.max_history_per_user:]
        
        # Sauvegarder de façon asynchrone
        asyncio.create_task(self._async_save())
    
    async def _async_save(self):
        """Sauvegarde asynchrone pour ne pas bloquer"""
        self.save_memory()
    
    def get_conversation_context(self, user_id: str, last_n: int = 5) -> List[Dict]:
        """Récupère le contexte de conversation récent"""
        user_id = str(user_id)
        if user_id not in self.conversations:
            return []
        
        return self.conversations[user_id][-last_n:]
    
    def has_recent_interaction(self, user_id: str, minutes: int = 10) -> bool:
        """Vérifie si l'utilisateur a interagi récemment"""
        user_id = str(user_id)
        if user_id not in self.conversations:
            return False
        
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent_messages = [
            msg for msg in self.conversations[user_id]
            if datetime.fromisoformat(msg['timestamp']) > cutoff
        ]
        
        return len(recent_messages) > 0
    
    def get_user_gaming_interests(self, user_id: str) -> List[str]:
        """Analyse les intérêts gaming de l'utilisateur depuis l'historique"""
        user_id = str(user_id)
        if user_id not in self.conversations:
            return []
        
        games_mentioned = []
        gaming_keywords = ['diablo', 'tarkov', 'wow', 'valorant', 'lol', 'bg3', 'helldivers', 'space marine']
        
        for msg in self.conversations[user_id]:
            content_lower = msg['content'].lower()
            for game in gaming_keywords:
                if game in content_lower and game not in games_mentioned:
                    games_mentioned.append(game)
        
        return games_mentioned
    
    def format_context_for_ai(self, user_id: str) -> str:
        """Formate le contexte pour l'IA"""
        context = self.get_conversation_context(user_id, 3)
        if not context:
            return ""
        
        formatted = "Contexte de conversation récent:\n"
        for msg in context:
            sender = "Bot" if msg['is_bot'] else "Utilisateur"
            formatted += f"{sender}: {msg['content'][:100]}...\n"
        
        return formatted

# Instance globale
conversation_memory = ConversationMemory()
