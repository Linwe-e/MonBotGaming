# 🔍 Diagnostic simple pour identifier le problème
import os
import sys

print("🔍 Diagnostic MonBotGaming")
print("=" * 40)

# 1. Vérifier les fichiers
print("\n📁 Vérification des fichiers:")
files_to_check = [
    'config.py',
    'utils/database.py', 
    'utils/gaming_helpers.py',
    'data/builds.json',
    'data/events.json',
    'data/users.json',
    '.env'
]

for file in files_to_check:
    exists = os.path.exists(file)
    print(f"  {'✅' if exists else '❌'} {file}")

# 2. Test d'import progressif
print("\n📦 Test des imports:")

try:
    print("  🔄 Import dotenv...", end="")
    from dotenv import load_dotenv
    print(" ✅")
except Exception as e:
    print(f" ❌ {e}")

try:
    print("  🔄 Import discord...", end="")
    import discord
    from discord.ext import commands
    print(" ✅")
except Exception as e:
    print(f" ❌ {e}")

try:
    print("  🔄 Import config...", end="")
    from config import BOT_CONFIG, GAMES
    print(" ✅")
    print(f"    - Jeux configurés: {len(GAMES)}")
except Exception as e:
    print(f" ❌ {e}")

# 3. Test du path utils
print("\n🛠️ Configuration path utils:")
utils_path = os.path.join(os.path.dirname(__file__), 'utils')
print(f"  Path utils: {utils_path}")
print(f"  Path existe: {'✅' if os.path.exists(utils_path) else '❌'}")

sys.path.append(utils_path)

try:
    print("  🔄 Import utils.database...", end="")
    from utils.database import db
    print(" ✅")
except Exception as e:
    print(f" ❌ {e}")

try:
    print("  🔄 Import utils.gaming_helpers...", end="")
    from utils.gaming_helpers import gaming_helpers
    print(" ✅")
except Exception as e:
    print(f" ❌ {e}")

print("\n🎯 Diagnostic terminé!")
