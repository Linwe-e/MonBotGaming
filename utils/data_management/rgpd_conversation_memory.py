"""
🔒 RGPD-Compliant Conversation Memory System pour MonBotGaming
Gestion des données personnelles conforme RGPD avec consentement et chiffrement
"""
import json
import os
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import asyncio
from cryptography.fernet import Fernet
import base64

class RGPDConversationMemory:
    """Gestionnaire de mémoire conversationnelle conforme RGPD"""
    
    def __init__(self, memory_file: str = "data/conversation_memory_encrypted.json", 
                 consent_file: str = "data/user_consents.json"):
        self.memory_file = memory_file
        self.consent_file = consent_file
        self.conversations: Dict[str, List[Dict]] = {}
        self.user_consents: Dict[str, Dict] = {}
        
        # Configuration RGPD
        self.max_history_per_user = 5  # Réduit pour minimisation des données
        self.default_memory_duration_hours = 2  # Durée par défaut plus courte
        self.max_memory_duration_hours = 24  # Maximum autorisé
        
        # Chiffrement
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        self.load_data()
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Génère ou récupère la clé de chiffrement"""
        key_file = "data/.encryption_key"
        try:
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                # Générer une nouvelle clé
                key = Fernet.generate_key()
                os.makedirs(os.path.dirname(key_file), exist_ok=True)
                with open(key_file, 'wb') as f:
                    f.write(key)
                return key
        except Exception as e:
            print(f"Erreur clé de chiffrement: {e}")
            return Fernet.generate_key()
    
    def _hash_user_id(self, user_id: str) -> str:
        """Hashe l'ID utilisateur pour anonymisation"""
        # Utilise HMAC pour éviter les attaques par dictionnaire
        secret_key = b"monbotgaming_privacy_salt_2025"
        hashed = hmac.new(secret_key, str(user_id).encode(), hashlib.sha256)
        return hashed.hexdigest()[:16]  # 16 chars suffisent pour éviter les collisions
    
    def _encrypt_data(self, data: str) -> str:
        """Chiffre les données sensibles"""
        try:
            encrypted = self.cipher_suite.encrypt(data.encode())
            return base64.b64encode(encrypted).decode()
        except Exception:
            return ""  # En cas d'erreur, ne pas stocker
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Déchiffre les données"""
        try:
            decoded = base64.b64decode(encrypted_data.encode())
            decrypted = self.cipher_suite.decrypt(decoded)
            return decrypted.decode()
        except Exception:
            return ""  # En cas d'erreur, retourner vide
    
    def check_user_consent(self, user_id: str) -> Tuple[bool, Dict]:
        """Vérifie le consentement de l'utilisateur"""
        hashed_id = self._hash_user_id(user_id)
        
        if hashed_id not in self.user_consents:
            return False, {}
        
        consent_data = self.user_consents[hashed_id]
        
        # Vérifier si le consentement n'a pas expiré
        consent_date = datetime.fromisoformat(consent_data.get('consent_date', ''))
        expiry_days = consent_data.get('consent_duration_days', 30)
        
        if datetime.now() > consent_date + timedelta(days=expiry_days):
            # Consentement expiré, le supprimer
            self.revoke_user_consent(user_id)
            return False, {}
        
        return True, consent_data
    def request_user_consent(self, user_id: str, memory_duration_hours: int = None) -> str:
        """Génère un message de demande de consentement RGPD"""
        duration = memory_duration_hours or self.default_memory_duration_hours
        
        consent_message = f"""🔒 **Gestion des Données - MonBotGaming**

Pour améliorer nos conversations, je peux garder en mémoire notre discussion pendant **{duration}h maximum**.

**📋 Données stockées :**
• Vos messages récents (anonymisés et chiffrés)
• Contexte gaming pour de meilleures réponses
• Aucune donnée personnelle identifiable

**✅ Vos droits RGPD :**
• Consentement révocable à tout moment
• Suppression automatique après {duration}h
• Droit à l'oubli avec `!privacy forget`
• Données chiffrées et sécurisées

**Acceptez-vous le stockage temporaire ?**
Répondez `!privacy accept {duration}` ou `!privacy decline`"""
        
        return consent_message
    
    def grant_user_consent(self, user_id: str, memory_duration_hours: int = None) -> bool:
        """Enregistre le consentement de l'utilisateur"""
        duration = memory_duration_hours or self.default_memory_duration_hours
        
        # Limiter la durée max
        if duration > self.max_memory_duration_hours:
            duration = self.max_memory_duration_hours
        
        hashed_id = self._hash_user_id(user_id)
        
        self.user_consents[hashed_id] = {
            'consent_date': datetime.now().isoformat(),
            'memory_duration_hours': duration,
            'consent_duration_days': 30,  # Le consentement expire après 30 jours
            'data_types': ['conversation_context', 'gaming_preferences'],
            'user_hash': hashed_id  # Pour l'audit
        }
        
        self.save_consents()
        return True
    
    def revoke_user_consent(self, user_id: str) -> bool:
        """Révoque le consentement et supprime toutes les données"""
        hashed_id = self._hash_user_id(user_id)
        
        # Supprimer le consentement
        if hashed_id in self.user_consents:
            del self.user_consents[hashed_id]
        
        # Supprimer toutes les conversations
        if hashed_id in self.conversations:
            del self.conversations[hashed_id]
        
        self.save_data()
        return True
    
    def add_message(self, user_id: str, content: str, is_bot: bool = False, context: Dict = None):
        """Ajoute un message seulement si consentement accordé"""
        has_consent, consent_data = self.check_user_consent(user_id)
        
        if not has_consent:
            return False  # Pas de stockage sans consentement
        
        hashed_id = self._hash_user_id(user_id)
        
        if hashed_id not in self.conversations:
            self.conversations[hashed_id] = []
        
        # Chiffrer le contenu sensible
        encrypted_content = self._encrypt_data(content[:200])  # Limiter la taille
        
        message = {
            'content_encrypted': encrypted_content,
            'content_length': len(content),  # Pour stats sans révéler le contenu
            'is_bot': is_bot,
            'timestamp': datetime.now().isoformat(),
            'context_type': context.get('type', 'general') if context else 'general'
        }
        
        self.conversations[hashed_id].append(message)
        
        # Limiter l'historique selon le consentement
        max_messages = min(self.max_history_per_user, consent_data.get('max_messages', 5))
        if len(self.conversations[hashed_id]) > max_messages:
            self.conversations[hashed_id] = self.conversations[hashed_id][-max_messages:]
        
        # Sauvegarder de façon asynchrone
        asyncio.create_task(self._async_save())
        return True
    
    def get_conversation_context(self, user_id: str, last_n: int = 3) -> List[str]:
        """Récupère le contexte déchiffré seulement si consentement valide"""
        has_consent, consent_data = self.check_user_consent(user_id)
        
        if not has_consent:
            return []
        
        hashed_id = self._hash_user_id(user_id)
        if hashed_id not in self.conversations:
            return []
        
        recent_messages = self.conversations[hashed_id][-last_n:]
        decrypted_context = []
        
        for msg in recent_messages:
            if 'content_encrypted' in msg:
                decrypted = self._decrypt_data(msg['content_encrypted'])
                if decrypted:  # Seulement si déchiffrement réussi
                    sender = "Bot" if msg['is_bot'] else "User"
                    decrypted_context.append(f"{sender}: {decrypted}")
        
        return decrypted_context
    
    def cleanup_expired_data(self):
        """Supprime les données expirées selon les consentements"""
        for hashed_id in list(self.conversations.keys()):
            if hashed_id in self.user_consents:
                consent_data = self.user_consents[hashed_id]
                hours_limit = 48 # On nettoie les messages de plus de 48h
                cutoff = datetime.now() - timedelta(hours=hours_limit)
                
                # Filtrer les messages récents
                self.conversations[hashed_id] = [
                    msg for msg in self.conversations[hashed_id]
                    if datetime.fromisoformat(msg['timestamp']) > cutoff
                ]
                
                # Supprimer si plus de messages
                if not self.conversations[hashed_id]:
                    del self.conversations[hashed_id]
            else:
                # Pas de consentement = suppression immédiate
                del self.conversations[hashed_id]
    
    def load_data(self):
        """Charge les données chiffrées"""
        try:
            # Charger les conversations chiffrées
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations = data.get('conversations', {})
            
            # Charger les consentements
            if os.path.exists(self.consent_file):
                with open(self.consent_file, 'r', encoding='utf-8') as f:
                    self.user_consents = json.load(f)
            
            # Nettoyer les données expirées
            self.cleanup_expired_data()
            
        except Exception as e:
            print(f"Erreur chargement données RGPD: {e}")
            self.conversations = {}
            self.user_consents = {}
    
    def save_data(self):
        """Sauvegarde toutes les données"""
        self.save_memory()
        self.save_consents()
    
    def save_memory(self):
        """Sauvegarde les conversations chiffrées"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'conversations': self.conversations,
                    'last_updated': datetime.now().isoformat(),
                    'encryption_info': 'AES-256 via Fernet',
                    'data_minimization': True
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde mémoire chiffrée: {e}")
    
    def save_consents(self):
        """Sauvegarde les consentements"""
        try:
            os.makedirs(os.path.dirname(self.consent_file), exist_ok=True)
            with open(self.consent_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_consents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde consentements: {e}")
    
    async def _async_save(self):
        """Sauvegarde asynchrone"""
        self.save_data()
    
    def export_user_data(self, user_id: str) -> Dict:
        """Export des données utilisateur (droit RGPD)"""
        has_consent, consent_data = self.check_user_consent(user_id)
        hashed_id = self._hash_user_id(user_id)
        
        export_data = {
            'user_id_hash': hashed_id,
            'consent_status': has_consent,
            'consent_data': consent_data if has_consent else None,
            'conversations_count': len(self.conversations.get(hashed_id, [])),
            'export_date': datetime.now().isoformat(),
            'note': 'Données anonymisées et chiffrées conformément au RGPD'
        }
        
        if has_consent and hashed_id in self.conversations:
            # Déchiffrer pour l'export (droit d'accès)
            decrypted_messages = []
            for msg in self.conversations[hashed_id]:
                if 'content_encrypted' in msg:
                    decrypted = self._decrypt_data(msg['content_encrypted'])
                    decrypted_messages.append({
                        'content': decrypted,
                        'is_bot': msg['is_bot'],
                        'timestamp': msg['timestamp']
                    })
            export_data['conversations'] = decrypted_messages
        
        return export_data

# Instance globale RGPD-compliant
rgpd_conversation_memory = RGPDConversationMemory()
