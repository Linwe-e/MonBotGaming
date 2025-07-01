# 📝 Journal des modifications - MonBotGaming

## [2.1.0] - 2025-07-01

### ✨ Nouvelles fonctionnalités
- **Interface RGPD moderne** : Boutons Discord interactifs pour la gestion des données
- **Export de données amélioré** : Fichier téléchargeable conforme Article 20 RGPD
- **Gestion intelligente des permissions** : Fallback automatique si permission "Attach Files" manquante
- **UX optimisée** : Messages éphémères pour la confidentialité, interface utilisateur moderne

### 🔒 Sécurité et conformité
- **Export téléchargeable** : Fichier `export_donnees.txt` avec toutes les données utilisateur
- **Détection automatique des permissions** : Vérification de `attach_files` avant envoi de fichier
- **Mode fallback** : Affichage en texte structuré si téléchargement impossible
- **Messages éphémères** : Protection renforcée de la confidentialité

### 🛠️ Améliorations techniques
- **Code robuste** : Gestion d'erreurs complète pour l'export RGPD
- **Conformité légale** : Respect total des exigences RGPD européennes
- **Interface unifiée** : Cohérence entre commandes texte et boutons interactifs
- **Documentation mise à jour** : README et politique de confidentialité actualisés

### 🔧 Corrections
- **Types Python** : Correction des conversions user_id (str/int) dans les modules RGPD
- **Permissions Discord** : Vérification améliorée des permissions de canal
- **Gestion des erreurs** : Messages d'erreur plus informatifs pour l'utilisateur

### 📚 Documentation
- **README enrichi** : Section dédiée aux commandes RGPD avec exemples
- **Politique de confidentialité** : Mise à jour avec les nouvelles fonctionnalités
- **CHANGELOG** : Ajout du journal des modifications pour traçabilité

---

## [2.0.0] - 2025-06-28

### 🎉 Version initiale
- **Bot Discord modulaire** avec architecture en cogs
- **Assistant gaming IA** intégré (Gemini)
- **Système RGPD complet** avec consentement et chiffrement
- **Gestion des builds gaming** multi-jeux
- **Tests unitaires** avec pytest
- **Configuration centralisée** et déploiement simplifié

---

*Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)*
