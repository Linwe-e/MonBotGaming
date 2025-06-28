# 💾 Gestionnaire de base de données JSON
# Interface unique pour tous les fichiers de données

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class DatabaseManager:
    """Gestionnaire centralisé pour toutes les données JSON"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.ensure_data_dir()    
    def ensure_data_dir(self):
        """S'assure que le dossier data existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_data(self, filename: str) -> Dict[str, Any]:
        """Charge les données depuis un fichier JSON"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Auto-initialisation si le fichier n'existe pas
            return self._create_default_data(filename)
        except json.JSONDecodeError:
            print(f"⚠️ Erreur de lecture JSON pour {filename}")
            return self._create_default_data(filename)
    
    def _create_default_data(self, filename: str) -> Dict[str, Any]:
        """Crée une structure de données par défaut pour un fichier"""
        default_structures = {
            'users.json': {
                "users": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0",
                    "total_users": 0
                }
            },
            'builds.json': {
                "builds": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0", 
                    "total_builds": 0
                }
            },
            'events.json': {
                "events": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0",
                    "total_events": 0
                }
            }
        }
        
        default_data = default_structures.get(filename, {})
        
        # Sauvegarder immédiatement la structure par défaut
        if default_data:
            self.save_data(filename, default_data)
            print(f"📄 Fichier {filename} initialisé automatiquement")
        
        return default_data
    
    def save_data(self, filename: str, data: Dict[str, Any]) -> bool:
        """Sauvegarde les données dans un fichier JSON"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            # Ajouter timestamp de mise à jour
            data['last_updated'] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erreur de sauvegarde pour {filename}: {e}")
            return False
    
    # 🔧 Méthodes spécifiques aux builds
    def get_builds(self, game: Optional[str] = None) -> Dict[str, Any]:
        """Récupère les builds, optionnellement filtrés par jeu"""
        data = self.load_data('builds.json')
        if game:
            return data.get('builds', {}).get(game, {})
        return data.get('builds', {})
    
    def save_build(self, game: str, build_name: str, build_data: Dict[str, Any]) -> bool:
        """Sauvegarde un build pour un jeu donné"""
        data = self.load_data('builds.json')
        if 'builds' not in data:
            data['builds'] = {}
        if game not in data['builds']:
            data['builds'][game] = {}
        
        data['builds'][game][build_name] = build_data
        return self.save_data('builds.json', data)
    
    def get_user_builds(self, user_id: str, game: Optional[str] = None) -> Dict[str, Any]:
        """Récupère les builds d'un utilisateur"""
        builds = self.get_builds(game)
        user_builds = {}
        
        if game:
            for build_name, build_data in builds.items():
                if build_data.get('author_id') == user_id:
                    user_builds[build_name] = build_data
        else:
            for game_name, game_builds in builds.items():
                for build_name, build_data in game_builds.items():
                    if build_data.get('author_id') == user_id:
                        if game_name not in user_builds:
                            user_builds[game_name] = {}
                        user_builds[game_name][build_name] = build_data
        
        return user_builds
    
    # 📅 Méthodes spécifiques aux événements
    def get_events(self) -> list:
        """Récupère tous les événements"""
        data = self.load_data('events.json')
        return data.get('events', [])
    
    def save_event(self, event_data: Dict[str, Any]) -> bool:
        """Sauvegarde un nouvel événement"""
        data = self.load_data('events.json')
        if 'events' not in data:
            data['events'] = []
        
        # Générer un ID unique pour l'événement
        event_data['id'] = f"event_{len(data['events']) + 1}_{int(datetime.now().timestamp())}"
        data['events'].append(event_data)
        
        return self.save_data('events.json', data)
    
    def update_event(self, event_id: str, updated_data: Dict[str, Any]) -> bool:
        """Met à jour un événement existant"""
        data = self.load_data('events.json')
        events = data.get('events', [])
        
        for i, event in enumerate(events):
            if event.get('id') == event_id:
                events[i].update(updated_data)
                return self.save_data('events.json', data)
        
        return False
    
    # 👥 Méthodes spécifiques aux utilisateurs
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Récupère le profil d'un utilisateur"""
        data = self.load_data('users.json')
        return data.get('users', {}).get(user_id, {})
    
    def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Sauvegarde le profil d'un utilisateur"""
        data = self.load_data('users.json')
        if 'users' not in data:
            data['users'] = {}
        
        data['users'][user_id] = profile_data
        
        # Mettre à jour les stats globales
        data['stats']['total_users'] = len(data['users'])
        
        return self.save_data('users.json', data)
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques globales"""
        data = self.load_data('users.json')
        return data.get('stats', {})

# Instance globale du gestionnaire de base de données
db = DatabaseManager()
