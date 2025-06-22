#!/bin/bash
# setup_vps.sh - Installation automatique MonBotGaming sur VPS
# Repo: https://github.com/Linwe-e/MonBotGaming/
# VPS: YOUR_VPS_IP
# Version: 2.0 - Optimisée pour bot gaming Discord

set -e

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuration
BOT_USER="botgaming"
BOT_DIR="/home/${BOT_USER}/MonBotGaming"
PYTHON_VERSION="3.11"

# Fonction de logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

log "🚀 Installation MonBotGaming sur VPS - Version Gaming Optimisée"
log "📍 IP VPS: Configuration en cours..."

# 1. Vérifications préliminaires
log "🔍 Vérifications système..."
if [[ $EUID -ne 0 ]]; then
   warn "Ce script doit être exécuté en tant que root pour certaines opérations"
fi

# Vérification de l'espace disque (minimum 2GB)
AVAILABLE_SPACE=$(df / | tail -1 | awk '{print $4}')
if [ $AVAILABLE_SPACE -lt 2097152 ]; then
    error "Espace disque insuffisant. Minimum 2GB requis."
fi

# 2. Mise à jour système
log "📦 Mise à jour du système..."
apt update && apt upgrade -y

# 3. Installation des dépendances système
log "� Installation des dépendances système..."
apt install -y \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-pip \
    python${PYTHON_VERSION}-venv \
    python${PYTHON_VERSION}-dev \
    git \
    curl \
    wget \
    htop \
    nano \
    screen \
    fail2ban \
    ufw \
    nginx \
    certbot \
    python3-certbot-nginx \
    build-essential \
    libssl-dev \
    libffi-dev

# 4. Création et configuration utilisateur dédié (sécurité)
log "👤 Configuration utilisateur bot..."
if ! id "$BOT_USER" &>/dev/null; then
    useradd -m -s /bin/bash $BOT_USER
    log "✅ Utilisateur $BOT_USER créé"
else
    log "ℹ️  Utilisateur $BOT_USER existe déjà"
fi

# Création des dossiers nécessaires
mkdir -p /home/$BOT_USER/{logs,backups,scripts}
chown -R $BOT_USER:$BOT_USER /home/$BOT_USER

# 5. Configuration sécurité avancée
log "🔒 Configuration sécurité..."

# Configuration fail2ban pour protection SSH
tee /etc/fail2ban/jail.local > /dev/null << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
EOF

systemctl enable fail2ban
systemctl start fail2ban

# Configuration firewall optimisée
log "🔥 Configuration firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw allow 8000/tcp   # Interface web future
ufw --force enable

# 6. Installation et configuration du bot
log "🤖 Installation MonBotGaming..."

# Clone ou mise à jour du repo
if [ -d "$BOT_DIR" ]; then
    log "📁 Dossier existant détecté, mise à jour..."
    cd $BOT_DIR
    sudo -u $BOT_USER git pull
else
    log "📥 Clonage du repository..."
    sudo -u $BOT_USER git clone https://github.com/Linwe-e/MonBotGaming.git $BOT_DIR
fi

cd $BOT_DIR

# Création de l'environnement virtuel
log "🐍 Configuration environnement Python..."
sudo -u $BOT_USER python${PYTHON_VERSION} -m venv .venv
sudo -u $BOT_USER .venv/bin/pip install --upgrade pip setuptools wheel

# Installation des dépendances
log "📚 Installation des dépendances Python..."
sudo -u $BOT_USER .venv/bin/pip install -r requirements.txt

# Création du fichier .env template si inexistant
if [ ! -f "$BOT_DIR/.env" ]; then
    log "📝 Création du fichier .env template..."
    sudo -u $BOT_USER tee $BOT_DIR/.env > /dev/null << 'EOF'
# 🔑 Configuration MonBotGaming
# ⚠️  IMPORTANT: Remplacez ces valeurs par vos vrais tokens !

# Discord Bot Token (requis)
DISCORD_TOKEN=your_discord_bot_token_here

# Gemini AI Token (optionnel mais recommandé pour l'IA gaming)
GEMINI_API_KEY=your_gemini_api_key_here

# Configuration base de données (optionnel)
DATABASE_URL=sqlite:///data/botgaming.db

# Configuration logging
LOG_LEVEL=INFO
LOG_FILE=/home/botgaming/logs/bot.log

# Configuration gaming
ENABLE_AI_GAMING=true
ENABLE_BUILD_SYSTEM=true
ENABLE_EVENTS_SYSTEM=true

# Configuration sécurité
ENCRYPT_USER_DATA=true
BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=24
EOF
    chown $BOT_USER:$BOT_USER $BOT_DIR/.env
    chmod 600 $BOT_DIR/.env
    warn "⚠️  N'oubliez pas de configurer le fichier .env avec vos vrais tokens !"
fi

# 7. Configuration systemd service optimisé
log "⚙️ Configuration service systemd..."
tee /etc/systemd/system/monbotgaming.service > /dev/null << EOF
[Unit]
Description=MonBotGaming Discord Bot - Serveur Gaming Communautaire
After=network-online.target
Wants=network-online.target
StartLimitBurst=3
StartLimitIntervalSec=60

[Service]
Type=simple
User=$BOT_USER
Group=$BOT_USER
WorkingDirectory=$BOT_DIR
Environment=PATH=$BOT_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$BOT_DIR
ExecStart=$BOT_DIR/.venv/bin/python main.py
ExecReload=/bin/kill -HUP \$MAINPID

# Redémarrage automatique en cas de crash
Restart=always
RestartSec=10
TimeoutStopSec=30

# Sécurité du processus
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=$BOT_DIR /home/$BOT_USER/logs /home/$BOT_USER/backups

# Logging
StandardOutput=append:/home/$BOT_USER/logs/bot.log
StandardError=append:/home/$BOT_USER/logs/bot_error.log
SyslogIdentifier=monbotgaming

[Install]
WantedBy=multi-user.target
EOF

# 8. Configuration log rotation avancée
log "📝 Configuration logs et monitoring..."
tee /etc/logrotate.d/monbotgaming > /dev/null << EOF
/home/$BOT_USER/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 $BOT_USER $BOT_USER
    postrotate
        systemctl reload monbotgaming || true
    endscript
}
EOF

# Création des dossiers de logs
mkdir -p /home/$BOT_USER/logs
chown -R $BOT_USER:$BOT_USER /home/$BOT_USER/logs

# 9. Script de monitoring du bot
log "📊 Création script de monitoring..."
tee /home/$BOT_USER/scripts/monitor_bot.sh > /dev/null << 'EOF'
#!/bin/bash
# Script de monitoring MonBotGaming

BOT_STATUS=$(systemctl is-active monbotgaming)
BOT_PID=$(systemctl show --property MainPID --value monbotgaming)

echo "=== Status MonBotGaming ==="
echo "Service: $BOT_STATUS"
echo "PID: $BOT_PID"
echo "Mémoire utilisée:"
if [ "$BOT_PID" != "0" ]; then
    ps -p $BOT_PID -o pid,ppid,cmd,%mem,%cpu --no-headers
fi
echo "=========================="

# Logs récents
echo "=== Derniers logs ==="
tail -10 /home/botgaming/logs/bot.log 2>/dev/null || echo "Pas de logs disponibles"
EOF

chmod +x /home/$BOT_USER/scripts/monitor_bot.sh
chown -R $BOT_USER:$BOT_USER /home/$BOT_USER/scripts

# 10. Script de backup automatique
log "💾 Configuration système de backup..."
tee /home/$BOT_USER/scripts/backup_bot.sh > /dev/null << 'EOF'
#!/bin/bash
# Backup automatique MonBotGaming

BACKUP_DIR="/home/botgaming/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BOT_DIR="/home/botgaming/MonBotGaming"

mkdir -p $BACKUP_DIR

# Backup des données
tar -czf "$BACKUP_DIR/botgaming_data_$DATE.tar.gz" \
    "$BOT_DIR/data" \
    "$BOT_DIR/.env" \
    --exclude="*.pyc" \
    --exclude="__pycache__"

# Garder seulement les 7 derniers backups
find $BACKUP_DIR -name "botgaming_data_*.tar.gz" -mtime +7 -delete

echo "Backup créé: botgaming_data_$DATE.tar.gz"
EOF

chmod +x /home/$BOT_USER/scripts/backup_bot.sh

# Crontab pour backup automatique quotidien
(crontab -u $BOT_USER -l 2>/dev/null; echo "0 3 * * * /home/$BOT_USER/scripts/backup_bot.sh >> /home/$BOT_USER/logs/backup.log 2>&1") | crontab -u $BOT_USER -

# 11. Configuration Nginx (interface web future)
log "🌐 Configuration Nginx pour interface web..."
tee /etc/nginx/sites-available/monbotgaming > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /home/botgaming/MonBotGaming/static/;
        expires 30d;
    }
}
EOF

# Activation du site (mais pas encore le service nginx)
ln -sf /etc/nginx/sites-available/monbotgaming /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 12. Finalisation et activation des services
log "🔄 Activation des services..."
systemctl daemon-reload
systemctl enable monbotgaming
systemctl enable nginx

# Test de configuration nginx
nginx -t

log "✅ Installation terminée avec succès !"
log ""
log "� === PROCHAINES ÉTAPES === "
log "1. 🔑 Configurez vos tokens dans: $BOT_DIR/.env"
log "2. 🚀 Démarrez le bot: systemctl start monbotgaming"
log "3. 📊 Vérifiez le status: systemctl status monbotgaming"
log "4. 📝 Surveillez les logs: tail -f /home/$BOT_USER/logs/bot.log"
log "5. 🔧 Script monitoring: /home/$BOT_USER/scripts/monitor_bot.sh"
log ""
log "🎮 === COMMANDES UTILES ==="
log "• Redémarrer bot: systemctl restart monbotgaming"
log "• Logs en temps réel: journalctl -u monbotgaming -f"
log "• Backup manuel: /home/$BOT_USER/scripts/backup_bot.sh"
log "• Status système: /home/$BOT_USER/scripts/monitor_bot.sh"
log ""
warn "⚠️  IMPORTANT: N'oubliez pas de configurer le fichier .env !"
log "🔗 Guide configuration: https://github.com/Linwe-e/MonBotGaming/blob/main/docs/DEVELOPER.md"
