#!/usr/bin/env python3
# 🚀 Script d'installation rapide MonBotGaming

import os
import subprocess
import sys
from pathlib import Path

def print_step(step, description):
    print(f"\n🔹 {step}: {description}")

def check_python():
    """Vérifier la version Python"""
    print_step("1", "Vérification Python")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requis")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def install_dependencies():
    """Installer les dépendances"""
    print_step("2", "Installation des dépendances")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées")
    except subprocess.CalledProcessError:
        print("❌ Erreur installation dépendances")
        sys.exit(1)

def setup_env_file():
    """Configurer le fichier .env"""
    print_step("3", "Configuration des secrets")
    
    env_path = Path(".env")
    if env_path.exists():
        print("✅ Fichier .env existe déjà")
        return
    
    env_template = """# 🔑 Configuration MonBotGaming
# Remplace les valeurs par tes vraies clés

# Token du bot Discord (https://discord.com/developers/applications)
DISCORD_TOKEN=ton_token_discord_ici

# Clé API Gemini (https://ai.google.dev/)
GEMINI_API_KEY=ta_cle_gemini_ici
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print("📄 Fichier .env créé avec template")
    print("⚠️  IMPORTANT: Configure tes vraies clés dans .env avant de lancer le bot!")

def check_directories():
    """Vérifier/créer les dossiers nécessaires"""
    print_step("4", "Vérification des dossiers")
    
    required_dirs = ["data", "logs", "cogs", "utils"]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir()
            print(f"📁 Créé: {dir_name}/")
        else:
            print(f"✅ Existe: {dir_name}/")

def show_next_steps():
    """Afficher les prochaines étapes"""
    print("\n" + "="*60)
    print("🎉 INSTALLATION TERMINÉE!")
    print("="*60)
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. 🔑 Configure tes clés dans .env")
    print("2. 🤖 Crée ton bot Discord: https://discord.com/developers/applications")
    print("3. 🚀 Lance le bot: python main.py")
    print("4. 🎮 Teste avec: !hello, !ping, !ai status")
    
    print("\n📚 DOCUMENTATION:")
    print("- README.md : Guide utilisateur")
    print("- docs/DEVELOPER.md : Guide développeur")
    print("- docs/architecture.md : Schéma du projet")
    
    print("\n🎯 COMMANDES IA HARDCORE:")
    print("- !ai ask [question] : Assistant gaming technique")
    print("- !ai build [jeu] [description] : Analyse de builds")
    print("- !ai team [jeu] [activité] [joueurs] : Compos optimales")

def main():
    """Installation principale"""
    print("🎮 INSTALLATION MONBOTGAMING")
    print("="*60)
    
    try:
        check_python()
        install_dependencies()
        setup_env_file()
        check_directories()
        show_next_steps()
        
    except KeyboardInterrupt:
        print("\n❌ Installation annulée")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
