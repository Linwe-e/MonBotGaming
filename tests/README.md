# 🧪 Tests MonBotGaming

## 📁 Organisation des Tests

### 🔬 **Tests Principaux**

- **`test_bot_basic.py`** : Tests de base du bot Discord
- **`test_ai_methods.py`** : Tests des méthodes IA Gemini  
- **`test_hardcore_ai.py`** : Tests des prompts hardcore gaming

### 🔧 **Tests Scripts (Legacy)**

- **`test_ai_methods_scripts.py`** : Ancienne version des tests IA
- **`test_hardcore_ai_scripts.py`** : Ancienne version des tests hardcore

## 🚀 **Lancer les Tests**

### Tests Individuels
```bash
# Test du bot principal
python tests/test_bot_basic.py

# Tests IA Gemini
python tests/test_ai_methods.py

# Tests prompts hardcore
python tests/test_hardcore_ai.py
```

### Tests Complets
```bash
# Tous les tests principaux
python -m pytest tests/ -v

# Ou manuellement
python tests/test_bot_basic.py
python tests/test_ai_methods.py  
python tests/test_hardcore_ai.py
```

## 📊 **Types de Tests**

- **Tests Unitaires** : Fonctions individuelles
- **Tests d'Intégration** : IA + Discord
- **Tests Fonctionnels** : Prompts gaming
- **Tests de Performance** : Limites API

## 🎯 **Bonnes Pratiques**

1. **Toujours tester avant commit**
2. **Tests isolés** (pas de dépendances)
3. **Données de test** séparées des vraies données
4. **Mock des APIs** pour éviter les limites

---

*Tests organisés pour garantir la qualité du bot gaming* 🎮
