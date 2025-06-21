# Tests pour MonBotGaming
# Package de tests pour le bot Discord gaming

"""
🧪 Package de tests MonBotGaming

Ce package contient tous les tests pour valider le fonctionnement du bot gaming.

Modules disponibles :
- test_bot_basic : Tests de base du bot Discord
- test_ai_methods : Tests des méthodes IA Gemini
- test_hardcore_ai : Tests des prompts hardcore gaming

Utilisation :
    python tests/test_bot_basic.py
    pytest tests/ -v
"""

import sys
import os

# Ajouter le dossier parent au path pour faciliter les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Configuration globale des tests
TEST_CONFIG = {
    'verbose': True,
    'mock_api_calls': True,  # Mock les appels API en test
    'test_data_dir': 'tests/test_data',
    'timeout': 30  # Timeout par défaut pour les tests
}

# Version du package de tests
__version__ = "1.0.0"
__author__ = "MonBotGaming Team"

def run_all_tests():
    """Lance tous les tests du package"""
    import subprocess
    import glob
    
    test_files = glob.glob(os.path.join(current_dir, 'test_*.py'))
    print(f"🧪 Lancement de {len(test_files)} suites de tests...")
    
    for test_file in test_files:
        print(f"\n▶️  Exécution : {os.path.basename(test_file)}")
        subprocess.run([sys.executable, test_file], cwd=parent_dir)
