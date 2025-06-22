# 🚫 RÈGLES ANTI-GÉNÉRATION DE FICHIERS TEST
# Ce fichier configure des règles pour éviter la création de fichiers test temporaires

# 1. Emplacements privilégiés pour les tests
ALLOWED_TEST_LOCATIONS = [
    "tests/",           # Tests officiels
    "examples/",        # Exemples de code  
    "scripts/",         # Scripts utilitaires
]

# 2. Noms de fichiers à éviter à la racine
FORBIDDEN_PATTERNS = [
    "test_*.py",
    "debug_*.py", 
    "temp_*.py",
    "quick_test.py",
    "*_test.py"
]

# 3. Alternatives recommandées
ALTERNATIVES = {
    "test_embeds.py": "examples/embed_examples.py",
    "test_bot_loading.py": "scripts/diagnostic.py", 
    "debug_ai.py": "tests/test_ai_methods.py",
    "quick_test.py": "scripts/show_structure.py"
}

def suggest_alternative(filename):
    """Suggérer une alternative pour un fichier de test temporaire"""
    for pattern, alternative in ALTERNATIVES.items():
        if pattern.replace("*", "") in filename:
            return alternative
    
    # Suggestions génériques
    if filename.startswith("test_"):
        return f"tests/{filename}"
    elif filename.startswith("debug_"):
        return f"scripts/{filename}"
    else:
        return f"examples/{filename}"

def check_filename(filename):
    """Vérifier si un nom de fichier respecte les règles"""
    import fnmatch
    
    for pattern in FORBIDDEN_PATTERNS:
        if fnmatch.fnmatch(filename, pattern):
            suggestion = suggest_alternative(filename)
            return False, f"❌ Évitez '{filename}' à la racine. Utilisez plutôt '{suggestion}'"
    
    return True, f"✅ '{filename}' est acceptable"

# Exemple d'utilisation :
if __name__ == "__main__":
    test_files = [
        "test_new_feature.py",
        "debug_connection.py", 
        "main.py",
        "examples/embed_demo.py"
    ]
    
    print("🧪 Vérification des noms de fichiers :")
    for file in test_files:
        valid, message = check_filename(file)
        print(f"  {message}")
