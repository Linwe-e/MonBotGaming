# 🧪 Tests MonBotGaming avec pytest

## 📁 Structure des Tests

```
tests/
├── conftest.py              # Fixtures communes
├── test_core.py             # Tests fonctionnalités de base, helpers, config, base de données, Discord
├── test_ai.py               # Tests IA et assistant gaming (fusionné)
└── test_rgpd.py             # Tests RGPD, consentement, sécurité, commandes privacy
```

## 🚀 **Utilisation**

### **Commandes de base**
```bash
# Tous les tests
pytest tests/ -v

# Tests par fichier
pytest tests/test_core.py -v     # Tests de base
pytest tests/test_ai.py -v       # Tests IA
pytest tests/test_rgpd.py -v     # Tests RGPD

# Tests avec markers
pytest -m "ai" -v           # Seulement les tests IA
pytest -m "not slow" -v     # Exclure tests lents
pytest -m "discord" -v      # Tests Discord uniquement
```

### **Script helper**
```bash
python run_tests.py         # Tous les tests
python run_tests.py core    # Tests core
python run_tests.py ai      # Tests IA
python run_tests.py fast    # Tests rapides
python run_tests.py coverage # Avec coverage
```

## 🎯 **Markers disponibles**

- `@pytest.mark.ai` : Tests liés à l'IA Gemini
- `@pytest.mark.discord` : Tests Discord
- `@pytest.mark.rgpd` : Tests conformité RGPD
- `@pytest.mark.slow` : Tests lents (API calls)
- `@pytest.mark.integration` : Tests d'intégration

## 🔧 **Fixtures utiles**

- `mock_bot` : Bot Discord de test
- `mock_ctx` : Context Discord mocké  
- `sample_games` : Données de jeux test
- `ai_available` : Vérifie si l'IA est configurée

## 📊 **Coverage et rapports**
```bash
# Coverage basique
pytest --cov=utils tests/

# Rapport HTML
pytest --cov=utils --cov=cogs --cov-report=html tests/
# Ouvre htmlcov/index.html

# Tests avec rapport détaillé
pytest tests/ -v --tb=long
```
2. **Tests isolés** (pas de dépendances)
3. **Données de test** séparées des vraies données
4. **Mock des APIs** pour éviter les limites

---

*Tests organisés pour garantir la qualité du bot gaming* 🎮

# Structure des tests mise à jour (2024-06)

## Organisation

- Tous les tests sont désormais à la racine du dossier `tests/`.
- Un fichier par domaine :
  - `test_ai.py` : tests IA et assistant gaming (fusionné)
  - `test_core.py` : tests des fonctionnalités de base, helpers, config, base de données, Discord
  - `test_rgpd.py` : tests RGPD, consentement, sécurité, commandes privacy
- Les anciens sous-dossiers (`ai/`, `core/`, `rgpd/`) et fichiers doublons ont été supprimés.
- Les fixtures partagées sont dans `conftest.py`.

## Lancer les tests

```bash
pytest
```

## Marqueurs utiles

- `@pytest.mark.ai` pour cibler les tests IA
- `@pytest.mark.discord` pour les tests Discord/core
- `@pytest.mark.rgpd` pour les tests RGPD
- `@pytest.mark.slow` pour les tests longs

## Ajout de tests

Ajoutez vos nouveaux tests dans le fichier correspondant à la racine du dossier `tests/`.

---

*Structure nettoyée et fusionnée par audit 2024-06.*
