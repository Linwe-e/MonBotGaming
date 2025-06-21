# 🛡️ Guide de Sécurité et Confidentialité

## 📋 Vue d'ensemble

Ce projet respecte les bonnes pratiques de sécurité pour protéger les données des membres de la communauté gaming.

## 🔒 Données Sensibles

### Fichiers Protégés (NON versionnés)

Les fichiers suivants contiennent des données personnelles et sont exclus du versioning :

```
data/users.json      # Profils des membres, stats, préférences
data/builds.json     # Builds personnels, stratégies, équipements  
data/events.json     # Participations aux événements, performances
```

### Fichiers Templates (versionnés)

Les templates montrent la structure sans exposer de données :

```
data/users.template.json     # Structure des profils utilisateur
data/builds.template.json    # Structure des builds gaming
data/events.template.json    # Structure des événements
```

## 🔧 Initialisation Sécurisée

### Premier démarrage

```bash
# Créer les fichiers de données à partir des templates
python scripts/init_data.py

# Vérifier l'intégrité des données
python scripts/init_data.py
```

### Auto-initialisation

Le système `DatabaseManager` crée automatiquement les fichiers manquants avec une structure vide mais valide.

## 🚨 Conformité RGPD

### Données Collectées

- **Pseudos Discord** : Publics par nature
- **Stats de jeu** : Avec consentement implicite (participation)
- **Préférences** : Stockage local, pas de transmission
- **Builds** : Partagés volontairement par les membres

### Droits des Utilisateurs

- **Droit à l'effacement** : Suppression du profil sur demande
- **Droit à la portabilité** : Export des données personnelles
- **Droit de rectification** : Modification des informations

### Mise en Place

```python
# Exemple de suppression de données utilisateur
def delete_user_data(user_id: str):
    # Supprimer de tous les fichiers
    users_data = db.load_data('users.json')
    builds_data = db.load_data('builds.json') 
    events_data = db.load_data('events.json')
    
    # Effacement complet
    if user_id in users_data.get('users', {}):
        del users_data['users'][user_id]
    
    # etc...
```

## 🔐 Sécurisation des Secrets

### Variables d'Environnement

```env
# .env (NON versionné)
DISCORD_TOKEN=your_secret_token
GEMINI_API_KEY=your_gemini_key
```

### Chargement Sécurisé

```python
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
```

## 💾 Stratégie de Backup

### Recommandations

1. **Backups automatiques** : Planifier des sauvegardes régulières
2. **Chiffrement** : Chiffrer les backups contenant des données membres
3. **Rotation** : Garder plusieurs versions (7 jours, 4 semaines, 12 mois)
4. **Test de restauration** : Vérifier régulièrement les backups

### Script de Backup

```bash
# Exemple de backup chiffré (à adapter)
7z a -p"$BACKUP_PASSWORD" backup_$(date +%Y%m%d).7z data/*.json
```

## 🚧 En Cas de Problème

### Fichiers Corrompus

```bash
# Réinitialiser un fichier de données
rm data/users.json
python scripts/init_data.py
```

### Fuite de Données

1. **Identifier** l'étendue de la fuite
2. **Notifier** les membres concernés
3. **Corriger** la faille de sécurité
4. **Auditer** l'ensemble du système

### Support

- **Issues GitHub** : Pour les problèmes techniques
- **Documentation** : `docs/DEVELOPER.md`
- **Scripts de diagnostic** : `scripts/`

## ✅ Checklist Sécurité

- [ ] `.env` créé et protégé
- [ ] `.gitignore` configuré pour les données sensibles
- [ ] Scripts d'initialisation testés
- [ ] Backups configurés
- [ ] Politique de confidentialité définie
- [ ] Procédures d'urgence documentées

## 📚 Ressources

- [RGPD Official](https://gdpr.eu/)
- [Discord Developer Policy](https://discord.com/developers/docs/policy)
- [Python Security Best Practices](https://bandit.readthedocs.io/)

---

**💡 Rappel** : La sécurité est un processus continu, pas un état final.
