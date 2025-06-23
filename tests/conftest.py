"""
Fixtures communes pour tous les tests MonBotGaming
"""
import pytest
import discord
from discord.ext import commands
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Ajouter le projet au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_bot():
    """Bot Discord de test"""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!test_', intents=intents)
    return bot

@pytest.fixture
def mock_ctx():
    """Context Discord mocké"""
    ctx = MagicMock()
    ctx.send = AsyncMock()
    ctx.author.name = "TestUser"
    ctx.guild.name = "TestGuild"
    return ctx

@pytest.fixture
def sample_games():
    """Données de jeux de test"""
    return {
        'diablo_4': {
            'name': 'Diablo IV',
            'emoji': '⚔️',
            'category': 'ARPG'
        },
        'tarkov': {
            'name': 'Escape from Tarkov',
            'emoji': '🔫', 
            'category': 'FPS'
        }
    }

@pytest.fixture(scope="session")
def ai_available():
    """Vérifie si l'IA est disponible pour les tests"""
    try:
        from utils.gemini_ai import gemini_ai
        return gemini_ai.is_available()
    except:
        return False
