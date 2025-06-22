#!/bin/bash
# deploy.sh - Script de déploiement rapide MonBotGaming
# Usage: ./deploy.sh [production|staging]

set -e

# Variables
ENVIRONMENT=${1:-production}
BOT_USER="botgaming"
BOT_DIR="/home/${BOT_USER}/MonBotGaming"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[DEPLOY] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

log "🚀 Déploiement MonBotGaming - Environnement: $ENVIRONMENT"

# Vérification des prérequis
if [ ! -d "$BOT_DIR" ]; then
    echo "❌ Erreur: Le bot n'est pas installé. Exécutez d'abord setup_vps.sh"
    exit 1
fi

# Backup avant déploiement
log "💾 Création backup pré-déploiement..."
sudo -u $BOT_USER $BOT_DIR/../scripts/backup_bot.sh

# Arrêt du service
log "⏹️  Arrêt du service bot..."
systemctl stop monbotgaming

# Mise à jour du code
log "📥 Mise à jour du code..."
cd $BOT_DIR
sudo -u $BOT_USER git fetch origin
sudo -u $BOT_USER git pull origin main

# Mise à jour des dépendances
log "📚 Mise à jour des dépendances..."
sudo -u $BOT_USER .venv/bin/pip install -r requirements.txt --upgrade

# Vérification de la configuration
log "🔍 Vérification configuration..."
if [ ! -f "$BOT_DIR/.env" ]; then
    warn "⚠️  Fichier .env manquant ! Créer la configuration avant de continuer."
    exit 1
fi

# Tests rapides (si disponibles)
if [ -f "$BOT_DIR/tests/test_bot_basic.py" ]; then
    log "🧪 Exécution tests basiques..."
    sudo -u $BOT_USER $BOT_DIR/.venv/bin/python -m pytest tests/test_bot_basic.py -q
fi

# Redémarrage du service
log "🔄 Redémarrage du service..."
systemctl start monbotgaming

# Vérification du démarrage
sleep 5
if systemctl is-active --quiet monbotgaming; then
    log "✅ Déploiement réussi ! Bot en fonctionnement"
    log "📊 Status: $(systemctl is-active monbotgaming)"
else
    warn "❌ Problème détecté lors du démarrage"
    log "📝 Derniers logs:"
    journalctl -u monbotgaming --no-pager -n 20
    exit 1
fi

log "🎮 MonBotGaming déployé avec succès !"
log "🔗 Surveillez les logs: journalctl -u monbotgaming -f"
