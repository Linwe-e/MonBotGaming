#!/usr/bin/env python3
"""
🧪 Test du nouveau système de détection contextuelle
"""

import asyncio
import sys
import os

# Ajouter le dossier parent au path pour importer depuis utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.gemini_ai import gemini_ai

async def test_context_detection():
    """Test de la détection contextuelle des messages"""
    
    print("🧪 TEST DÉTECTION CONTEXTUELLE")
    print("=" * 50)
    
    # Tests de différents types de messages
    test_cases = [
        ("Salut ! Comment vas-tu ?", "greeting_question"),
        ("Hello !", "greeting"),
        ("Comment optimiser mon build necromancer ?", "technical"),
        ("Quel est le meilleur loadout pour Tarkov ?", "technical"),
        ("Comment ça marche ce bot ?", "question"),
        ("Peux-tu m'expliquer Discord ?", "question"),
        ("Build DPS", "technical"),
        ("Bonjour tout le monde", "greeting")
    ]
    
    print("🔍 Tests de détection du type de message :")
    for message, expected_type in test_cases:
        detected_type = gemini_ai._detect_message_type(message)
        status = "✅" if detected_type == expected_type else "❌"
        print(f"{status} '{message}' → {detected_type} (attendu: {expected_type})")
    
    # Test des réponses réelles
    print(f"\n🤖 Test des réponses adaptées :")
    
    if gemini_ai.is_available():
        # Test salutation
        print(f"\n📨 Test salutation :")
        response = await gemini_ai.gaming_assistant("Salut ! Comment vas-tu ?")
        print(f"Réponse: {response[:200]}...")
        
        # Test technique
        print(f"\n📨 Test technique :")
        response = await gemini_ai.gaming_assistant("Comment optimiser un build DPS ?")
        print(f"Réponse: {response[:200]}...")
    else:
        print("⚠️ IA non disponible - tests de réponses ignorés")

if __name__ == "__main__":
    asyncio.run(test_context_detection())
