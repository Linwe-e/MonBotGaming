# 🚀 Guide d'Hébergement VPS - MonBotGaming

## 🎯 **Hébergement VPS Infomaniak - Guide Complet**

### 📋 **Prérequis VPS**
```bash
# Configuration minimale recommandée
- RAM : 1 GB (lite suffisant pour démarrer)
- CPU : 1 vCore
- Stockage : 20 GB SSD
- OS : Ubuntu 22.04 LTS (recommandé)
- Bande passante : Illimitée
```

### 🛠️ **Script d'Installation VPS**

<function_calls>
<invoke name="create_file">
<parameter name="content">#!/bin/bash
# setup_vps.sh - Installation automatique MonBotGaming sur VPS

set -e

echo "🚀 Installation MonBotGaming sur VPS..."

# 1. Mise à jour système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# 2. Installation Python 3.11+
echo "🐍 Installation Python..."
sudo apt install -y python3.11 python3.11-pip python3.11-venv git curl

# 3. Création utilisateur dédié (sécurité)
echo "👤 Création utilisateur bot..."
sudo useradd -m -s /bin/bash botgaming
sudo usermod -aG sudo botgaming

# 4. Configuration firewall
echo "🔥 Configuration firewall..."
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 8000  # Pour interface web future

# 5. Installation du bot
echo "🤖 Installation MonBotGaming..."
sudo -u botgaming bash << 'EOF'
cd /home/botgaming
git clone https://github.com/VOTRE_USERNAME/MonBotGaming.git
cd MonBotGaming
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
EOF

# 6. Configuration systemd (service automatique)
echo "⚙️ Configuration service systemd..."
sudo tee /etc/systemd/system/monbotgaming.service > /dev/null << 'EOF'
[Unit]
Description=MonBotGaming Discord Bot
After=network.target

[Service]
Type=simple
User=botgaming
WorkingDirectory=/home/botgaming/MonBotGaming
Environment=PATH=/home/botgaming/MonBotGaming/.venv/bin
ExecStart=/home/botgaming/MonBotGaming/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 7. Configuration log rotation
echo "📝 Configuration logs..."
sudo tee /etc/logrotate.d/monbotgaming > /dev/null << 'EOF'
/home/botgaming/MonBotGaming/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 0644 botgaming botgaming
}
EOF

# 8. Activation service
sudo systemctl daemon-reload
sudo systemctl enable monbotgaming

echo "✅ Installation terminée !"
echo "📝 Prochaines étapes :"
echo "1. Configurez /home/botgaming/MonBotGaming/.env avec vos tokens"
echo "2. sudo systemctl start monbotgaming"
echo "3. sudo systemctl status monbotgaming"
