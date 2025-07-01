"""
🧠 Smart Response System pour MonBotGaming
Gère les réponses contextuelles : embeds vs messages simples
"""
import re
from typing import Tuple, Dict, Any

class SmartResponseManager:
    """Gestionnaire intelligent de réponses selon le contexte"""
    
    # Patterns pour détecter le type de message
    GAMING_PATTERNS = [
        r'\b(build|strat|team|comp|guide|meta|loadout|stuff|rotation)\b',
        r'\b(diablo|tarkov|wow|valorant|lol|bg3|helldivers)\b',
        r'\b(dps|heal|tank|support|carry)\b',
        r'\b(level|skill|talent|paragon|stuff|gear)\b'
    ]
    
    CASUAL_PATTERNS = [
        r'\b(salut|bonjour|hello|hi|yo|hey)\b',
        r'\b(ça va|comment|pourquoi|qui est|qu\'est)\b',
        r'\b(merci|thanks|cool|super|génial)\b',
        r'\b(lol|mdr|xd|😂|🤣)\b'
    ]
    
    QUESTION_PATTERNS = [
        r'^(qui|que|quoi|comment|pourquoi|où|quand)',
        r'\?$',  # Se termine par ?
        r'\b(est-ce que|peux-tu|pourrais|aide)\b'
    ]

    PRIVACY_PATTERNS = [
        r'\b(confidentialité|confidentialite|données|donnees|data|rgpd|vie privée|vie privee|stocke|enregistre|informations personnelles|privacy|private|protection des données|protection des donnees|paramètres de confidentialité|parametres de confidentialite|consentement|mémoire|memoire|conversation sauvegardée|conversation sauvegardee|stockage|suppression des données|suppression des donnees|efface|oublie|forget|delete my data|delete my account|what do you know about me|what do you store about me|what do you keep about me|my privacy|my data|my info|my information|my conversations|personal info|personal data|personal information|erase my data|erase my info|remove my data|remove my info|gdpr|compliance|compliant)\b',
        r'\b(mes infos|mes données|mes donnees|mes conversations|mes informations|mes data|mes paramètres|mes parametres)\b',
        r'\b(ce que tu sais de moi|ce que tu gardes|ce que tu stockes|ce que tu enregistres|ce que tu retiens|ce que tu mémorises|ce que tu memorises)\b',
        r'\b(est-ce que tu gardes|est-ce que tu stockes|est-ce que tu enregistres|est-ce que tu retiens|est-ce que tu mémorises|est-ce que tu memorises)\b',
        r'\b(privacy policy|politique de confidentialité|politique de confidentialite)\b',
        r'\b(je veux supprimer|je veux effacer|je veux oublier|je veux retirer|je veux que tu oublies|je veux que tu supprimes)\b',
        r'\b(que fais-tu de mes données|que fais-tu de mes infos|que fais-tu de mes informations|que fais-tu de mes conversations)\b',
        r'\b(que fais tu de mes données|que fais tu de mes infos|que fais tu de mes informations|que fais tu de mes conversations)\b',
    ]
    
    @classmethod
    def analyze_message_context(cls, content: str) -> Dict[str, Any]:
        """
        Analyse le contexte d'un message pour déterminer le type de réponse approprié
        
        Returns:
            Dict avec type de réponse et métadonnées
        """
        content_lower = content.lower()
        
        # Compter les matches de chaque type
        gaming_score = sum(1 for pattern in cls.GAMING_PATTERNS 
                          if re.search(pattern, content_lower, re.IGNORECASE))
        
        casual_score = sum(1 for pattern in cls.CASUAL_PATTERNS 
                          if re.search(pattern, content_lower, re.IGNORECASE))
        
        privacy_score = 0
        for pattern in cls.PRIVACY_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                print(f"[DEBUG][analyze_message_context] PRIVACY pattern matched: '{pattern}' in '{content}'")
                privacy_score += 1
        
        is_question = any(re.search(pattern, content_lower, re.IGNORECASE) 
                         for pattern in cls.QUESTION_PATTERNS)
        
        # Logique de décision
        if privacy_score > 0:
            return {
                'response_type': 'privacy_info',
                'reason': 'Privacy related question',
                'gaming_score': gaming_score,
                'casual_score': casual_score,
                'privacy_score': privacy_score
            }
        
        elif len(content.split()) <= 3 and casual_score > 0:
            # Messages courts et casualaux → Réponse simple
            return {
                'response_type': 'simple',
                'reason': 'Short casual message',
                'gaming_score': gaming_score,
                'casual_score': casual_score
            }
        
        elif gaming_score >= 2:
            # Clairement gaming → Embed complet
            return {
                'response_type': 'embed_full',
                'reason': 'Gaming technical question',
                'gaming_score': gaming_score,
                'casual_score': casual_score
            }
        
        elif gaming_score == 1 and is_question:
            # Gaming léger + question → Embed léger
            return {
                'response_type': 'embed_light',
                'reason': 'Light gaming question',
                'gaming_score': gaming_score,
                'casual_score': casual_score
            }
        
        elif is_question and len(content.split()) > 8:
            # Question complexe non-gaming → Embed léger
            return {
                'response_type': 'embed_light',
                'reason': 'Complex non-gaming question',
                'gaming_score': gaming_score,
                'casual_score': casual_score
            }
        
        else:
            # Conversation normale → Réponse simple
            return {
                'response_type': 'simple',
                'reason': 'Normal conversation',
                'gaming_score': gaming_score,
                'casual_score': casual_score
            }
    
    @classmethod
    def should_use_embed(cls, content: str) -> Tuple[bool, str]:
        """
        Détermine si on doit utiliser un embed ou un message simple
        
        Returns:
            (should_use_embed, embed_type)
            embed_type: 'full', 'light', 'none', or 'privacy_info'
        """
        analysis = cls.analyze_message_context(content)
        print(f"[DEBUG][should_use_embed] content='{content}' | analysis={analysis}")
        if analysis['response_type'] == 'simple':
            return False, 'none'
        elif analysis['response_type'] == 'embed_light':
            return True, 'light'
        elif analysis['response_type'] == 'privacy_info':
            print(f"[DEBUG][should_use_embed] RGPD detected for content: '{content}'")
            return False, 'privacy_info' # Privacy info will be a simple text response, not an embed
        else:
            return True, 'full'

# Exemples de tests
if __name__ == "__main__":
    test_messages = [
        "Salut !",
        "Qui est le plus fort entre l\'hippopotame et le rhinocéros ?",
        "Comment build un necro blood sur Diablo 4 ?",
        "Peux-tu m\'aider avec ma rotation DPS ?",
        "Merci pour l\'aide !",
        "Quelle est la meta team comp pour Helldivers 2 ?",
        "Quelles sont mes données de confidentialité ?",
        "Est-ce que tu stockes mes informations personnelles ?"
    ]
    
    for msg in test_messages:
        analysis = SmartResponseManager.analyze_message_context(msg)
        use_embed, embed_type = SmartResponseManager.should_use_embed(msg)
        print(f"'{msg}' → {analysis['response_type']} (embed: {embed_type})")