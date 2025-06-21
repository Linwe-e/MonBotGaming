#!/usr/bin/env python3
"""
🧪 Test de la nouvelle détection intelligente de messages
"""

import sys
import os

# Ajouter le dossier parent au path pour importer depuis utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.gemini_ai import gemini_ai

def test_message_detection():
    """Test de la détection contextuelle améliorée"""
    print("🧠 Test de la Détection Intelligente de Messages")
    print("=" * 60)
    
    # Cas de test avec résultats attendus
    test_cases = [
        # Salutations pures
        ("Salut !", "greeting"),
        ("Bonjour comment allez-vous ?", "greeting_question"),
        ("Hey ça va ?", "greeting_question"),
        
        # Salutations + questions techniques (CAS IMPORTANT)
        ("Salut ! Comment optimiser mon build nécromancien Diablo 4 ?", "technical_with_greeting"),
        ("Bonjour ! Quelle est la meilleure stratégie pour Helldivers 2 ?", "technical_with_greeting"),
        ("Hey ! J'ai besoin d'aide pour mon loadout Tarkov", "technical_with_greeting"),
        
        # Questions techniques pures
        ("Build nécromancien sang optimal pour endgame ?", "technical"),
        ("DPS rotation pour paladin ret WoW Classic", "technical"),
        ("Meta builds Diablo 4 saison 4", "technical"),
        
        # Questions avec contexte
        ("Comment faire pour progresser plus vite ?", "question_with_context"),
        ("Quel jeu me conseillez-vous ?", "question"),
        
        # Messages généraux
        ("Merci pour l'aide", "general"),
        ("C'est noté", "general"),
    ]
    
    print("📋 Tests de Détection :")
    print("-" * 60)
    
    success_count = 0
    total_count = len(test_cases)
    
    for message, expected in test_cases:
        detected = gemini_ai._detect_message_type(message)
        status = "✅" if detected == expected else "❌"
        
        if detected == expected:
            success_count += 1
        
        print(f"{status} '{message}'")
        print(f"   Attendu: {expected} | Détecté: {detected}")
        
        if detected != expected:
            print(f"   ⚠️  DIFFÉRENCE DÉTECTÉE")
        print()
    
    print("=" * 60)
    print(f"📊 Résultats: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 Tous les tests passent ! Détection intelligente opérationnelle.")
    else:
        print("⚠️  Certains cas nécessitent des ajustements.")
    
    return success_count == total_count

def test_real_scenarios():
    """Test avec des scenarios réels d'usage"""
    print("\n🎮 Test de Scénarios Réels")
    print("=" * 60)
    
    real_scenarios = [
        "Salut ! Comment optimiser mon DPS sur Diablo 4 ?",
        "Bonjour, j'ai un problème avec mon build BG3",
        "Hey ! Quelle est la meta pour LOL en ce moment ?",
        "Salut comment ça va ?",
        "Build nécromancien sang endgame S4",
        "Aide pour stratégie Helldivers 2 difficulty 9"
    ]
    
    print("🔍 Analyse des Messages Réels :")
    print("-" * 60)
    
    for message in real_scenarios:
        message_type = gemini_ai._detect_message_type(message)
        print(f"📝 '{message}'")
        print(f"🎯 Type détecté: {message_type}")
        
        # Simuler le choix du prompt
        if message_type == 'technical_with_greeting':
            print("💡 Réponse: Salut bref + Analyse technique hardcore")
        elif message_type == 'technical':
            print("💡 Réponse: Analyse technique hardcore pure")
        elif message_type == 'greeting_question':
            print("💡 Réponse: Politesse + Proposition d'aide")
        elif message_type == 'greeting':
            print("💡 Réponse: Salut gaming amical")
        else:
            print(f"💡 Réponse: Mode {message_type}")
        
        print("-" * 30)

if __name__ == "__main__":
    print("🚀 Test de la Détection Intelligente MonBotGaming")
    print("=" * 60)
    
    # Tests de détection
    detection_ok = test_message_detection()
    
    # Tests de scénarios réels
    test_real_scenarios()
    
    print("\n✨ Tests terminés !")
    
    if detection_ok:
        print("🎉 La nouvelle détection est prête pour la production !")
    else:
        print("🔧 Des ajustements sont nécessaires avant le déploiement.")
