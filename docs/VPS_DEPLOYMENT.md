# 🚀 Guide Déploiement VPS - MonBotGaming

## 📋 Vue d'ensemble

Ce guide vous accompagne pour déployer votre bot Discord gaming sur votre VPS de manière optimisée et sécurisée.

## 🎯 Scripts Disponibles

### 1. **setup_vps.sh** - Installation Complète
```bash
# Sur votre VPS, téléchargez et exécutez :
wget https://raw.githubusercontent.com/Linwe-e/MonBotGaming/main/scripts/setup_vps.sh
chmod +x setup_vps.sh
sudo ./setup_vps.sh
```

**Ce script installe :**
- ✅ Python 3.11 + environnement virtuel
- ✅ Sécurité renforcée (fail2ban, firewall)
- ✅ Service systemd automatique
- ✅ Monitoring et logs
- ✅ Système de backup
- ✅ Nginx pour interface web future

### 2. **deploy.sh** - Déploiement/Mise à jour
```bash
# Mise à jour rapide du bot
sudo /home/botgaming/scripts/deploy.sh
```

### 3. **health_check.sh** - Contrôle Santé
```bash
# Vérification complète
sudo /home/botgaming/scripts/health_check.sh --detailed
```

### 4. **quick_commands.sh** - Commandes Rapides
```bash
# Gestion quotidienne
/home/botgaming/scripts/quick_commands.sh start|stop|restart|status|logs
```

## 📦 Étapes d'Installation

### Phase 1: Préparation VPS
```bash
# 1. Connexion SSH à votre VPS
ssh root@YOUR_VPS_IP

# 2. Télécharger le script d'installation
wget https://raw.githubusercontent.com/Linwe-e/MonBotGaming/main/scripts/setup_vps.sh
chmod +x setup_vps.sh

# 3. Exécuter l'installation
sudo ./setup_vps.sh
```

### Phase 2: Configuration
```bash
# 1. Modifier le fichier de configuration
nano /home/botgaming/MonBotGaming/.env

# 2. Remplacer les valeurs par vos vrais tokens :
DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OTA.GaBcDe.VOTRE_VRAI_TOKEN_ICI
GEMINI_API_KEY=AIzaSyYOTRE_VRAI_API_KEY_GEMINI_ICI
```

### Phase 3: Démarrage
```bash
# 1. Démarrer le service
sudo systemctl start monbotgaming

# 2. Vérifier le status
sudo systemctl status monbotgaming

# 3. Suivre les logs
tail -f /home/botgaming/logs/bot.log
```

## 🎮 Configuration Gaming Spécifique

### Variables d'Environnement
```env
# Gaming Features
ENABLE_AI_GAMING=true
ENABLE_BUILD_SYSTEM=true
ENABLE_EVENTS_SYSTEM=true

# Jeux supportés (automatique selon config.py)
SUPPORTED_GAMES=diablo,wow,tarkov,bg3,space_marine_2

# Sécurité données gaming
ENCRYPT_USER_DATA=true
BACKUP_INTERVAL_HOURS=24
```

## 🔧 Commandes de Gestion Quotidienne

### Surveillance
```bash
# Status rapide
/home/botgaming/scripts/quick_commands.sh status

# Health check complet
/home/botgaming/scripts/health_check.sh --detailed

# Logs en temps réel
/home/botgaming/scripts/quick_commands.sh logs
```

### Maintenance
```bash
# Redémarrage
/home/botgaming/scripts/quick_commands.sh restart

# Mise à jour
/home/botgaming/scripts/quick_commands.sh update

# Backup manuel
/home/botgaming/scripts/quick_commands.sh backup
```

## 🔒 Sécurité

### Fichiers Protégés
- `.env` : Permissions 600 (lecture propriétaire uniquement)
- Logs : Rotation automatique (30 jours)
- Backups : Automatiques chaque nuit à 3h

### Pare-feu Configuré
- SSH (22) : Autorisé
- HTTP (80) : Autorisé
- HTTPS (443) : Autorisé  
- Interface Web (8000) : Autorisé

### Protection Intrusion
- Fail2Ban actif
- Tentatives SSH limitées (3 essais)
- Ban automatique (1h)

## 📊 Monitoring

### Logs Disponibles
```bash
# Logs du bot
tail -f /home/botgaming/logs/bot.log

# Logs systèmes
journalctl -u monbotgaming -f

# Logs d'erreurs
tail -f /home/botgaming/logs/bot_error.log
```

### Métriques Surveillées
- ✅ CPU/Mémoire du processus
- ✅ Connectivité Discord
- ✅ Espace disque
- ✅ Erreurs applicatives
- ✅ Status du service

## 🎯 Optimisations Gaming

### Performance
- Service systemd optimisé
- Redémarrage automatique en cas de crash
- Gestion mémoire intelligente
- Logs rotatifs pour éviter la saturation

### Fonctionnalités Spéciales
- Backup automatique des builds gaming
- Système d'événements persistent
- Chiffrement des données utilisateurs
- Interface web préparée (port 8000)

## 🆘 Dépannage

### Problèmes Courants

**Le bot ne démarre pas :**
```bash
# Vérifier la configuration
cat /home/botgaming/MonBotGaming/.env

# Vérifier les logs
journalctl -u monbotgaming --no-pager -n 20

# Tester manuellement
sudo -u botgaming /home/botgaming/MonBotGaming/.venv/bin/python /home/botgaming/MonBotGaming/main.py
```

**Token Discord invalide :**
```bash
# Vérifier le token dans .env
grep DISCORD_TOKEN /home/botgaming/MonBotGaming/.env

# Tester la connectivité
curl -H "Authorization: Bot VOTRE_TOKEN" https://discord.com/api/users/@me
```

**Problème de permissions :**
```bash
# Réparer les permissions
sudo chown -R botgaming:botgaming /home/botgaming/
sudo chmod 600 /home/botgaming/MonBotGaming/.env
```

## 📞 Support

- 📖 Documentation : `/docs/DEVELOPER.md`
- 🔧 Scripts diagnostics : `/scripts/diagnostic.py`
- 📊 Monitoring : `/scripts/health_check.sh --detailed`

---

**🎮 Bon gaming avec MonBotGaming ! 🎮**
