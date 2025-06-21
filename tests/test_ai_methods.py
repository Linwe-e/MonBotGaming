#!/usr/bin/env python3
# Test des corrections des méthodes IA

import asyncio
import sys
import os

# Ajouter le dossier parent au path pour importer depuis utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.gemini_ai import gemini_ai

async def test_ai_methods():
    """Test des méthodes corrigées de l'IA"""
    print("🤖 Test des méthodes IA Gaming")
    print("=" * 50)
    
    # Vérifier la disponibilité
    print(f"✅ IA disponible: {gemini_ai.is_available()}")
    
    if not gemini_ai.is_available():
        print("❌ Gemini AI non configuré - Test arrêté")
        return
    
    # Test des méthodes
    tests = [
        {
            'name': 'gaming_assistant',
            'method': gemini_ai.gaming_assistant,
            'args': ('Quel est le meilleur build necro diablo 4?', 'Diablo 4')
        },
        {
            'name': 'suggest_team_composition', 
            'method': gemini_ai.suggest_team_composition,
            'args': ('Helldivers 2', 'extraction', '4 joueurs')
        },
        {
            'name': 'analyze_build',
            'method': gemini_ai.analyze_build,
            'args': ('Build necro sang avec Blood Surge et Bone Armor', 'Diablo 4')
        },
        {
            'name': 'generate_event_description',
            'method': gemini_ai.generate_event_description,
            'args': ('WoW Classic', 'raid', {'title': 'Molten Core'})
        }
    ]
    
    for test in tests:
        print(f"\n🔍 Test {test['name']}...")
        try:
            result = await test['method'](*test['args'])
            print(f"✅ {test['name']}: OK")
            print(f"📝 Longueur réponse: {len(result)} caractères")
            if len(result) > 100:
                print(f"📋 Aperçu: {result[:100]}...")
            else:
                print(f"📋 Réponse: {result}")
        except Exception as e:
            print(f"❌ {test['name']}: ERREUR - {e}")
    
    print(f"\n🎯 Tests terminés!")

if __name__ == "__main__":
    asyncio.run(test_ai_methods())
