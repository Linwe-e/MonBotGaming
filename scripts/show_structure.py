#!/usr/bin/env python3
# 🌳 Affichage de la structure du projet MonBotGaming

import os
from pathlib import Path

def print_tree(startpath, prefix="", max_depth=3, current_depth=0):
    """Affiche l'arborescence du projet avec emojis"""
    
    if current_depth >= max_depth:
        return
    
    # Dossiers à ignorer
    ignore_dirs = {'.git', '__pycache__', '.venv', 'node_modules', '.env'}
    
    items = []
    try:
        for item in sorted(Path(startpath).iterdir()):
            if item.name.startswith('.') and item.name not in {'.env', '.gitignore'}:
                continue
            if item.name in ignore_dirs:
                continue
            items.append(item)
    except PermissionError:
        return
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        
        # Emojis par type de fichier/dossier
        emoji = get_emoji(item)
        
        print(f"{prefix}{current_prefix}{emoji} {item.name}")
        
        if item.is_dir():
            print_tree(item, next_prefix, max_depth, current_depth + 1)

def get_emoji(path):
    """Retourne l'emoji approprié selon le type de fichier/dossier"""
    
    if path.is_dir():
        dir_emojis = {
            'cogs': '🤖',
            'utils': '🛠️',
            'data': '📊',
            'docs': '📚',
            'scripts': '🧪',
            'tests': '🧪',
            'archive': '📁',
            '.github': '⚙️'
        }
        return dir_emojis.get(path.name, '📁')
    
    file_emojis = {
        '.py': '🐍',
        '.md': '📄',
        '.json': '📋',
        '.txt': '📝',
        '.env': '🔑',
        '.gitignore': '🚫',
        '.mmd': '📊'
    }
    
    suffix = path.suffix.lower()
    if suffix in file_emojis:
        return file_emojis[suffix]
    
    # Fichiers spéciaux
    special_files = {
        'main.py': '🚀',
        'config.py': '⚙️',
        'requirements.txt': '📦',
        'README.md': '📖'
    }
    
    return special_files.get(path.name, '📄')

def show_project_stats():
    """Affiche les statistiques du projet"""
    
    stats = {
        'Python files': 0,
        'Documentation': 0,
        'Configuration': 0,
        'Total files': 0
    }
    
    for root, dirs, files in os.walk('.'):
        # Ignorer certains dossiers
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'archive'}]
        
        for file in files:
            stats['Total files'] += 1
            
            if file.endswith('.py'):
                stats['Python files'] += 1
            elif file.endswith(('.md', '.txt')):
                stats['Documentation'] += 1
            elif file in {'.env', '.gitignore', 'config.py', 'requirements.txt'}:
                stats['Configuration'] += 1
    
    return stats

def main():
    """Affichage principal"""
    
    print("🎮 STRUCTURE MONBOTGAMING")
    print("=" * 50)
    
    # Arborescence
    print("\n🌳 ARBORESCENCE:")
    print("MonBotGaming/")
    print_tree(".", max_depth=3)
    
    # Statistiques
    print("\n📊 STATISTIQUES:")
    stats = show_project_stats()
    for category, count in stats.items():
        print(f"  {category}: {count}")
      # Description des dossiers
    print("\n📁 DESCRIPTION DES DOSSIERS:")
    descriptions = {
        "🚀 main.py": "Point d'entrée principal du bot",
        "🤖 cogs/": "Modules fonctionnels (commandes Discord)",
        "🛠️ utils/": "Utilitaires et helpers réutilisables", 
        "📊 data/": "Base de données JSON (builds, events, users)",
        "📚 docs/": "Documentation du projet",
        "🧪 scripts/": "Outils de développement et administration",
        "🧪 tests/": "Tests unitaires et d'intégration",
        "📁 archive/": "Anciennes versions et sauvegardes",
        "⚙️ config.py": "Configuration centralisée",
        "🔑 .env": "Variables secrètes (tokens, clés API)"
    }
    
    for item, desc in descriptions.items():
        print(f"  {item:<15} {desc}")
    
    print(f"\n✨ Projet organisé et prêt pour le développement!")

if __name__ == "__main__":
    main()
