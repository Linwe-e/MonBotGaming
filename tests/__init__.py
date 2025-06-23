# Tests pour MonBotGaming - Migration vers pytest
# Package de tests pour le bot Discord gaming

"""
🧪 Package de tests MonBotGaming (pytest)

Ce package contient tous les tests pour valider le fonctionnement du bot gaming.

Structure pytest :
- test_core.py : Tests de base du bot Discord et configuration
- test_ai.py : Tests des fonctionnalités IA et gaming assistant
- test_rgpd.py : Tests de conformité RGPD et gestion des données

Utilisation avec pytest :
    pytest tests/ -v                    # Tous les tests
    pytest tests/test_core.py -v        # Tests core uniquement  
    pytest -m "ai" -v                   # Tests IA uniquement
    pytest -m "not slow" -v             # Tests rapides
    python run_tests.py [type]          # Script helper
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
__version__ = "2.0.0"  # Migration vers pytest
__author__ = "MonBotGaming Team"

def run_all_tests():
    """Lance tous les tests avec pytest (nouvelle méthode)"""
    import subprocess
    print("🧪 Utilisation de pytest pour les tests...")
    print("💡 Utilisez: python run_tests.py ou pytest tests/ -v")
    subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'], cwd=parent_dir)
