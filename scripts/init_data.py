#!/usr/bin/env python3
"""
🔧 Script d'initialisation des données du bot
Crée les fichiers de données réels à partir des templates si ils n'existent pas.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def create_data_files():
    """Crée les fichiers de données réels à partir des templates."""
    
    data_dir = Path("data")
    
    # Mapping template -> fichier réel
    files_to_create = {
        "users.template.json": "users.json",
        "builds.template.json": "builds.json", 
        "events.template.json": "events.json"
    }
    
    print("🔧 Initialisation des fichiers de données...")
    
    for template_file, real_file in files_to_create.items():
        template_path = data_dir / template_file
        real_path = data_dir / real_file
        
        # Si le fichier réel n'existe pas, le créer
        if not real_path.exists():
            if template_path.exists():
                print(f"📄 Création de {real_file} à partir du template...")
                
                # Charger le template
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                # Créer la structure de base (vide mais valide)
                if "users" in template_file:
                    initial_data = {
                        "users": {},
                        "metadata": {
                            "created": datetime.utcnow().isoformat() + "Z",
                            "version": "1.0",
                            "total_users": 0
                        }
                    }
                elif "builds" in template_file:
                    initial_data = {
                        "builds": {},
                        "metadata": {
                            "created": datetime.utcnow().isoformat() + "Z", 
                            "version": "1.0",
                            "total_builds": 0
                        }
                    }
                elif "events" in template_file:
                    initial_data = {
                        "events": {},
                        "metadata": {
                            "created": datetime.utcnow().isoformat() + "Z",
                            "version": "1.0", 
                            "total_events": 0
                        }
                    }
                
                # Sauvegarder le fichier réel
                with open(real_path, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ {real_file} créé avec succès")
            else:
                print(f"❌ Template {template_file} introuvable")
        else:
            print(f"ℹ️  {real_file} existe déjà, ignoré")
    
    print("\n🛡️  RAPPEL SÉCURITÉ:")
    print("   - Les fichiers de données réels ne sont PAS versionnés")
    print("   - Ils contiennent des données sensibles des membres") 
    print("   - Pensez à faire des backups sécurisés réguliers")
    print("   - En cas de problème, supprimez les fichiers et relancez ce script")

def check_data_integrity():
    """Vérifie l'intégrité des fichiers de données."""
    
    data_dir = Path("data")
    files_to_check = ["users.json", "builds.json", "events.json"]
    
    print("\n🔍 Vérification de l'intégrité des données...")
    
    for file_name in files_to_check:
        file_path = data_dir / file_name
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {file_name} : structure JSON valide")
                
                # Vérifications spécifiques
                if "metadata" in data:
                    print(f"   📊 Créé le : {data['metadata'].get('created', 'Inconnu')}")
                
            except json.JSONDecodeError as e:
                print(f"❌ {file_name} : JSON invalide - {e}")
            except Exception as e:
                print(f"❌ {file_name} : Erreur - {e}")
        else:
            print(f"⚠️  {file_name} : Fichier manquant")

if __name__ == "__main__":
    print("🚀 Initialisation des données MonBotGaming")
    print("=" * 50)
    
    create_data_files()
    check_data_integrity()
    
    print("\n✨ Initialisation terminée !")
