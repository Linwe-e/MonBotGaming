#!/usr/bin/env python3
# Test des améliorations hardcore de l'IA

import asyncio
import sys
import os

# Ajouter le dossier parent au path pour importer depuis utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.gemini_ai import gemini_ai

async def test_hardcore_responses():
    """Test des réponses hardcore vs génériques"""
    print("⚔️ TEST IA HARDCORE GAMING")
    print("=" * 60)
    
    if not gemini_ai.is_available():
        print("❌ Gemini AI non configuré - Test arrêté")
        return
    
    # Questions test pour hardcore gamers
    hardcore_tests = [
        {
            'category': 'Build Analysis',
            'question': 'Analyse ce build necro diablo 4 : Blood Surge + Bone Armor + Aspect of Reanimation',
            'game': 'Diablo 4'
        },
        {
            'category': 'Team Composition', 
            'question': 'Composition optimale 4 joueurs Helldivers 2 pour Helldive difficulty',
            'game': 'Helldivers 2'
        },
        {
            'category': 'Meta Strategy',
            'question': 'Meilleure stratégie farming Escape from Tarkov wipe début',
            'game': 'Escape from Tarkov'
        },
        {
            'category': 'Advanced Question',
            'question': 'Optimisation DPS warrior fury WoW Classic phase 6',
            'game': 'WoW Classic'
        }
    ]
    
    for i, test in enumerate(hardcore_tests, 1):
        print(f"\n🎯 TEST {i}/4: {test['category']}")
        print(f"❓ Question: {test['question']}")
        print(f"🎮 Jeu: {test['game']}")
        print("⏳ Génération réponse hardcore...")
        
        try:
            response = await gemini_ai.gaming_assistant(test['question'], test['game'])
            
            print(f"✅ Réponse générée ({len(response)} caractères)")
            
            # Analyser si la réponse semble "hardcore"
            hardcore_indicators = [
                'dps', 'meta', 'optimization', 'breakpoint', 'scaling',
                'frame', 'rotation', 'synergy', 'efficiency', 'min-max',
                'calculation', 'build', 'stat', 'tier', 'priority'
            ]
            
            hardcore_score = sum(1 for indicator in hardcore_indicators 
                                if indicator.lower() in response.lower())
            
            print(f"🔥 Score hardcore: {hardcore_score}/15")
            
            # Aperçu de la réponse
            preview = response[:200].replace('\n', ' ') + "..." if len(response) > 200 else response
            print(f"📝 Aperçu: {preview}")
            
            if hardcore_score >= 5:
                print("✅ Réponse semble HARDCORE !")
            elif hardcore_score >= 3:
                print("⚠️ Réponse moyennement technique")
            else:
                print("❌ Réponse trop générique")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        print("-" * 60)
    
    print(f"\n🎯 Tests terminés!")
    print(f"💡 Si les scores sont élevés, l'IA est maintenant adaptée aux hardcore gamers!")

if __name__ == "__main__":
    asyncio.run(test_hardcore_responses())
