#!/usr/bin/env python3
"""
🔍 Script de diagnostic MonBotGaming
Vérifie la santé complète du bot et de son environnement
Usage: python diagnostic.py [--vps] [--full]
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from datetime import datetime

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, status, details=None):
    """Affiche un status avec couleur appropriée"""
    color = Colors.GREEN if status else Colors.RED
    symbol = "✅" if status else "❌"
    print(f"{color}{symbol} {message}{Colors.END}")
    if details:
        print(f"   {Colors.YELLOW}ℹ️  {details}{Colors.END}")

def print_header(title):
    """Affiche un en-tête coloré"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🔍 {title}{Colors.END}")
    print("=" * (len(title) + 4))

def check_python_environment():
    """Vérifie l'environnement Python"""
    print_header("ENVIRONNEMENT PYTHON")
    
    # Version Python
    python_version = sys.version_info
    is_good_version = python_version.major == 3 and python_version.minor >= 9
    print_status(
        f"Python {python_version.major}.{python_version.minor}.{python_version.micro}",
        is_good_version,
        "Python 3.9+ requis" if not is_good_version else None
    )
    
    # Environnement virtuel
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print_status("Environnement virtuel actif", in_venv)
    
    return is_good_version and in_venv

def check_dependencies():
    """Vérifie les dépendances Python"""
    print_header("DÉPENDANCES PYTHON")
    
    required_packages = [
        'discord.py',
        'python-dotenv',
        'aiohttp',
        'requests',
        'google-generativeai',
        'cryptography'
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_status(f"Package {package}", True)
        except ImportError:
            print_status(f"Package {package}", False, "pip install " + package)
            all_good = False
    
    return all_good

def check_config_files():
    """Vérifie les fichiers de configuration"""
    print_header("FICHIERS DE CONFIGURATION")
    
    files_to_check = [
        ('.env', True),
        ('config.py', True),
        ('main.py', True),
        ('requirements.txt', True),
        ('data/users.template.json', False),
        ('data/builds.template.json', False),
        ('data/events.template.json', False)
    ]
    
    all_good = True
    for file_path, required in files_to_check:
        exists = os.path.exists(file_path)
        if required and not exists:
            all_good = False
        print_status(
            f"Fichier {file_path}",
            exists,
            "Fichier requis manquant" if required and not exists else None
        )
    
    # Vérification spéciale du .env
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
            has_discord_token = 'DISCORD_TOKEN=' in env_content and 'your_discord_bot_token_here' not in env_content
            print_status("Token Discord configuré", has_discord_token)
            
            has_gemini_token = 'GEMINI_API_KEY=' in env_content and 'your_gemini_api_key_here' not in env_content
            print_status("Token Gemini configuré", has_gemini_token, "Optionnel pour l'IA")
    
    return all_good

def check_data_directory():
    """Vérifie la structure des données"""
    print_header("STRUCTURE DES DONNÉES")
    
    data_dir = Path('data')
    required_files = [
        'users.template.json',
        'builds.template.json', 
        'events.template.json'
    ]
    
    all_good = True
    print_status("Dossier data", data_dir.exists())
    
    for file_name in required_files:
        file_path = data_dir / file_name
        exists = file_path.exists()
        print_status(f"Template {file_name}", exists)
        
        if exists:
            try:
                with open(file_path, 'r') as f:
                    json.load(f)
                print_status(f"JSON valide {file_name}", True)
            except json.JSONDecodeError:
                print_status(f"JSON valide {file_name}", False, "Fichier JSON corrompu")
                all_good = False
    
    return all_good

def check_network_connectivity():
    """Vérifie la connectivité réseau"""
    print_header("CONNECTIVITÉ RÉSEAU")
    
    hosts_to_test = [
        ('discord.com', '443'),
        ('api.discord.com', '443'),
        ('generativelanguage.googleapis.com', '443')
    ]
    
    all_good = True
    for host, port in hosts_to_test:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, int(port)))
            sock.close()
            
            is_reachable = result == 0
            print_status(f"Connexion {host}:{port}", is_reachable)
            if not is_reachable:
                all_good = False
        except Exception as e:
            print_status(f"Connexion {host}:{port}", False, str(e))
            all_good = False
    
    return all_good

def check_vps_specific():
    """Vérifications spécifiques VPS Linux"""
    print_header("VÉRIFICATIONS VPS")
    
    # Vérifier si on est sur Linux
    is_linux = platform.system() == 'Linux'
    print_status("Système Linux", is_linux)
    
    if not is_linux:
        print_status("VPS Check", False, "Non applicable (pas sur Linux)")
        return False
    
    # Vérifier systemd service
    try:
        result = subprocess.run(['systemctl', 'is-active', 'monbotgaming'], 
                              capture_output=True, text=True)
        service_active = result.returncode == 0
        print_status("Service systemd actif", service_active)
    except FileNotFoundError:
        print_status("Systemd disponible", False)
        service_active = False
    
    # Vérifier les permissions
    if os.path.exists('.env'):
        stat_info = os.stat('.env')
        permissions = oct(stat_info.st_mode)[-3:]
        secure_perms = permissions == '600'
        print_status(f"Permissions .env ({permissions})", secure_perms, 
                    "Devrait être 600" if not secure_perms else None)
    
    # Vérifier l'utilisateur
    current_user = os.getenv('USER', 'unknown')
    is_bot_user = current_user == 'botgaming'
    print_status(f"Utilisateur correct ({current_user})", is_bot_user,
                "Devrait être 'botgaming'" if not is_bot_user else None)
    
    return service_active

def check_discord_connection():
    """Test de base de connexion Discord"""
    print_header("TEST DISCORD")
    
    try:
        import discord
        from dotenv import load_dotenv
        
        load_dotenv()
        token = os.getenv('DISCORD_TOKEN')
        
        if not token or token == 'your_discord_bot_token_here':
            print_status("Token Discord", False, "Token non configuré")
            return False
        
        print_status("Token Discord présent", True)
        print_status("Bibliothèque discord.py", True)
        
        # Test basique du token (sans se connecter)
        if len(token) > 50 and '.' in token:
            print_status("Format token valide", True)
        else:
            print_status("Format token valide", False, "Token mal formaté")
            return False
            
        return True
        
    except ImportError:
        print_status("Bibliothèque discord.py", False, "pip install discord.py")
        return False
    except Exception as e:
        print_status("Test Discord", False, str(e))
        return False

def main():
    """Fonction principale"""
    print(f"{Colors.BOLD}{Colors.BLUE}🎮 DIAGNOSTIC MonBotGaming 🎮{Colors.END}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Plateforme: {platform.system()} {platform.release()}")
    
    # Arguments
    vps_mode = '--vps' in sys.argv
    full_mode = '--full' in sys.argv
    
    checks = [
        ("Environnement Python", check_python_environment),
        ("Dépendances", check_dependencies),
        ("Configuration", check_config_files),
        ("Données", check_data_directory),
        ("Connectivité", check_network_connectivity),
        ("Discord", check_discord_connection)
    ]
    
    if vps_mode or platform.system() == 'Linux':
        checks.append(("VPS Linux", check_vps_specific))
    
    # Exécution des vérifications
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_status(f"Erreur lors de {name}", False, str(e))
            results.append((name, False))
    
    # Résumé final
    print_header("RÉSUMÉ")
    total_checks = len(results)
    passed_checks = sum(1 for _, result in results if result)
    
    success_rate = (passed_checks / total_checks) * 100
    
    for name, result in results:
        print_status(name, result)
    
    print(f"\n{Colors.BOLD}Score: {passed_checks}/{total_checks} ({success_rate:.1f}%){Colors.END}")
    
    if success_rate >= 80:
        print(f"{Colors.GREEN}🎉 Bot prêt pour le gaming ! 🎉{Colors.END}")
    elif success_rate >= 60:
        print(f"{Colors.YELLOW}⚠️  Quelques problèmes à corriger{Colors.END}")
    else:
        print(f"{Colors.RED}❌ Problèmes majeurs détectés{Colors.END}")
    
    return 0 if success_rate >= 80 else 1

if __name__ == "__main__":
    sys.exit(main())
