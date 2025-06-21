#!/usr/bin/env python3
"""
🔍 Script de validation de la sécurité
Vérifie que les mesures de sécurité sont bien en place.
"""

import os
from pathlib import Path
import json

def check_gitignore():
    """Vérifie que le .gitignore protège les données sensibles."""
    
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        print("❌ Fichier .gitignore manquant")
        return False
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sensitive_files = [
        "data/users.json",
        "data/builds.json", 
        "data/events.json",
        ".env"
    ]
    
    protected = []
    not_protected = []
    
    for file in sensitive_files:
        if file in content:
            protected.append(file)
        else:
            not_protected.append(file)
    
    print("🔒 Protection .gitignore :")
    for file in protected:
        print(f"  ✅ {file}")
    
    for file in not_protected:
        print(f"  ❌ {file} - NON PROTÉGÉ")
    
    return len(not_protected) == 0

def check_env_file():
    """Vérifie la configuration des secrets."""
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  Fichier .env manquant - à créer pour la production")
        return False
    
    print("🔐 Fichier .env détecté")
    
    # Vérifier sans exposer le contenu
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_vars = ["DISCORD_TOKEN", "GEMINI_API_KEY"]
    
    for var in required_vars:
        if var in content:
            print(f"  ✅ {var} configuré")
        else:
            print(f"  ❌ {var} manquant")
    
    return True

def check_data_templates():
    """Vérifie que les templates sont présents."""
    
    templates = [
        "data/users.template.json",
        "data/builds.template.json",
        "data/events.template.json"
    ]
    
    print("📄 Templates de données :")
    
    all_present = True
    for template in templates:
        path = Path(template)
        if path.exists():
            print(f"  ✅ {template}")
            
            # Vérifier la structure JSON
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    json.load(f)
                print(f"     📋 Structure JSON valide")
            except json.JSONDecodeError:
                print(f"     ❌ JSON invalide")
                all_present = False
        else:
            print(f"  ❌ {template} manquant")
            all_present = False
    
    return all_present

def check_data_files():
    """Vérifie l'état des fichiers de données réels."""
    
    data_files = [
        "data/users.json",
        "data/builds.json", 
        "data/events.json"
    ]
    
    print("💾 Fichiers de données réels :")
    
    all_valid = True
    for file in data_files:
        path = Path(file)
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Vérifier la structure de base
                if "users" in data or "builds" in data or "events" in data:
                    print(f"  ✅ {file} (structure valide)")
                else:
                    print(f"  ⚠️  {file} (structure à vérifier)")
                    all_valid = False
            except json.JSONDecodeError:
                print(f"  ❌ {file} (JSON invalide)")
                all_valid = False
        else:
            print(f"  ℹ️  {file} sera créé automatiquement")
    
    return all_valid

def check_scripts():
    """Vérifie que les scripts de sécurité sont présents."""
    
    scripts = [
        "scripts/init_data.py",
        "scripts/show_structure.py",
        "scripts/security_check.py"
    ]
    
    print("🧪 Scripts de sécurité :")
    
    all_present = True
    for script in scripts:
        path = Path(script)
        if path.exists():
            print(f"  ✅ {script}")
        else:
            print(f"  ❌ {script} manquant")
            all_present = False
    
    return all_present

def security_report():
    """Génère un rapport de sécurité complet."""
    
    print("🛡️  RAPPORT DE SÉCURITÉ MONBOTGAMING")
    print("=" * 50)
    
    checks = [
        ("Protection .gitignore", check_gitignore),
        ("Configuration secrets", check_env_file),
        ("Templates de données", check_data_templates), 
        ("Fichiers de données", check_data_files),
        ("Scripts de sécurité", check_scripts)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n🔍 {name} :")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Erreur : {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ :")
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ OK" if result else "❌ PROBLÈME"
        print(f"  {status} {name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Score de sécurité : {passed}/{total}")
    
    if passed == total:
        print("🎉 Toutes les vérifications sont passées !")
        print("🚀 Projet prêt pour la production sécurisée")
    else:
        print("⚠️  Certains problèmes nécessitent votre attention")
        print("📖 Consultez docs/SECURITY.md pour plus d'infos")

if __name__ == "__main__":
    security_report()
