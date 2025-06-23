# 🔒 Politique de Confidentialité RGPD - MonBotGaming

## 📋 Vue d'ensemble

MonBotGaming est conçu avec le respect de la vie privée dès la conception (**Privacy by Design**) et se conforme pleinement au Règlement Général sur la Protection des Données (RGPD).

## 🎯 Données collectées

### Données personnelles
- **ID Discord anonymisé** (haché avec HMAC-SHA256)
- **Contenu des conversations** (chiffré AES-256)
- **Horodatage des interactions**
- **Contexte gaming déduit**

### Données techniques
- **Logs d'erreurs** (sans contenu personnel)
- **Statistiques d'usage** (anonymisées)

## ⚖️ Base légale du traitement

Le traitement des données personnelles repose sur :
- **Consentement explicite** de l'utilisateur (Art. 6.1.a RGPD)
- **Finalité légitime** d'amélioration du service (Art. 6.1.f RGPD)

## 🎯 Finalités du traitement

Les données sont utilisées exclusivement pour :
1. **Améliorer la qualité des réponses** du bot
2. **Maintenir le contexte conversationnel** 
3. **Personnaliser l'assistance gaming**
4. **Éviter les répétitions** dans les réponses

## 🔐 Mesures de sécurité

### Chiffrement
- **AES-256** via bibliothèque Fernet
- **Clés de chiffrement** générées aléatoirement
- **Hachage HMAC-SHA256** pour l'anonymisation

### Minimisation des données
- **Limitation à 200 caractères** par message stocké
- **Maximum 5 messages** par utilisateur
- **Durée configurable** (1-24 heures maximum)
- **Suppression automatique** à expiration

### Contrôle d'accès
- **Accès restreint** aux données chiffrées
- **Aucun accès humain** aux conversations
- **Logs d'audit** des accès système

## ⏱️ Durée de conservation

| Type de données | Durée | Justification |
|------------------|--------|---------------|
| Conversations chiffrées | 1-24h (configurable) | Contexte conversationnel |
| Consentements | 30 jours | Preuve du consentement |
| Logs techniques | 7 jours | Débogage système |

## 👤 Vos droits RGPD

### Accès et portabilité
- **`!privacy status`** - Voir vos données stockées
- **`!privacy export`** - Télécharger vos données

### Rectification et effacement
- **`!privacy forget`** - Droit à l'oubli (suppression complète)
- **Suppression automatique** à expiration du consentement

### Consentement
- **`!privacy accept [heures]`** - Accorder le consentement
- **`!privacy decline`** - Refuser le stockage
- **Révocable à tout moment** sans justification

### Information
- **`!privacy info`** - Informations RGPD détaillées
- **Transparence complète** sur le traitement

## 🌍 Transferts de données

- **Stockage local uniquement** (serveur France)
- **Aucun transfert** vers des pays tiers
- **Aucun partage** avec des tiers
- **Pas d'analyse externe** des données

## 🚫 Ce que nous ne faisons PAS

- ❌ Vendre vos données
- ❌ Partager avec des tiers
- ❌ Analyser sans consentement
- ❌ Stocker au-delà de la durée consentie
- ❌ Identifier personnellement les utilisateurs
- ❌ Créer des profils publicitaires

## 🛡️ Conformité technique

### Architecture Privacy by Design
```
User ID → HMAC-SHA256 → Hash anonyme
Message → AES-256 → Données chiffrées
Timestamp → Auto-cleanup → Suppression automatique
```

### Contrôles automatiques
- **Vérification du consentement** avant chaque stockage
- **Nettoyage quotidien** des données expirées
- **Validation des durées** de conservation
- **Audit trail** des opérations

## 📞 Contact et réclamations

### Support automatisé
- Toutes les demandes RGPD sont **traitées automatiquement**
- **Réponse immédiate** via les commandes `!privacy`
- **Aucune intervention humaine** nécessaire

### Droits de recours
En cas de problème :
1. Utiliser les commandes `!privacy` pour résoudre
2. Contacter l'administrateur du serveur Discord
3. Droit de recours auprès de la CNIL (France)

## 🔄 Mises à jour

Cette politique peut être mise à jour pour :
- **Améliorer la protection** des données
- **Se conformer** à l'évolution réglementaire
- **Intégrer de nouvelles fonctionnalités** respectueuses

Les utilisateurs seront informés des changements significatifs.

## ✅ Attestation de conformité

MonBotGaming respecte :
- ✅ **RGPD** (Règlement 2016/679)
- ✅ **Loi Informatique et Libertés** (modifiée)
- ✅ **Principes Privacy by Design**
- ✅ **Recommandations CNIL**

---

**Dernière mise à jour :** 22 juin 2025  
**Version :** 1.0  
**Responsable :** MonBotGaming Privacy System
