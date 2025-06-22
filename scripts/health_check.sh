#!/bin/bash
# health_check.sh - Contrôle de santé complet MonBotGaming
# Usage: ./health_check.sh [--detailed]

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Variables
BOT_USER="botgaming"
BOT_DIR="/home/${BOT_USER}/MonBotGaming"
DETAILED=${1:-""}

print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

echo -e "${BLUE}🏥 === HEALTH CHECK MonBotGaming ===${NC}"
echo ""

# 1. Service Status
echo -e "${YELLOW}📊 Status du Service${NC}"
systemctl is-active --quiet monbotgaming
SERVICE_STATUS=$?
print_status "Service MonBotGaming" $SERVICE_STATUS

systemctl is-enabled --quiet monbotgaming
ENABLED_STATUS=$?
print_status "Service activé au démarrage" $ENABLED_STATUS

# 2. Processus et ressources
echo -e "\n${YELLOW}🔧 Ressources Système${NC}"
BOT_PID=$(systemctl show --property MainPID --value monbotgaming)
if [ "$BOT_PID" != "0" ] && [ -n "$BOT_PID" ]; then
    echo -e "${GREEN}📍 PID: $BOT_PID${NC}"
    
    # Utilisation mémoire et CPU
    MEMORY_INFO=$(ps -p $BOT_PID -o pid,ppid,cmd,%mem,%cpu --no-headers 2>/dev/null)
    if [ -n "$MEMORY_INFO" ]; then
        echo -e "${GREEN}💾 Processus: $MEMORY_INFO${NC}"
    fi
else
    echo -e "${RED}❌ Aucun processus actif détecté${NC}"
fi

# 3. Espace disque
echo -e "\n${YELLOW}💽 Espace Disque${NC}"
DISK_USAGE=$(df /home/$BOT_USER --output=pcent | tail -1 | tr -d '% ')
if [ $DISK_USAGE -lt 80 ]; then
    echo -e "${GREEN}✅ Espace disque: ${DISK_USAGE}% utilisé${NC}"
else
    echo -e "${RED}⚠️  Espace disque critique: ${DISK_USAGE}% utilisé${NC}"
fi

# 4. Fichiers de configuration
echo -e "\n${YELLOW}📋 Configuration${NC}"
if [ -f "$BOT_DIR/.env" ]; then
    print_status "Fichier .env présent" 0
    
    # Vérification des tokens (sans les afficher)
    if grep -q "DISCORD_TOKEN=your_discord_bot_token_here" "$BOT_DIR/.env"; then
        print_status "Token Discord configuré" 1
        echo -e "${RED}  ⚠️  Token Discord non configuré !${NC}"
    else
        print_status "Token Discord configuré" 0
    fi
else
    print_status "Fichier .env présent" 1
fi

# 5. Logs récents
echo -e "\n${YELLOW}📝 Logs Récents${NC}"
if [ -f "/home/$BOT_USER/logs/bot.log" ]; then
    print_status "Fichier de logs présent" 0
    
    # Vérification d'erreurs récentes
    ERROR_COUNT=$(tail -50 /home/$BOT_USER/logs/bot.log 2>/dev/null | grep -i "error\|exception\|traceback" | wc -l)
    if [ $ERROR_COUNT -eq 0 ]; then
        print_status "Aucune erreur récente" 0
    else
        print_status "Erreurs détectées ($ERROR_COUNT)" 1
    fi
else
    print_status "Fichier de logs présent" 1
fi

# 6. Connectivité réseau
echo -e "\n${YELLOW}🌐 Connectivité${NC}"
if ping -c 1 discord.com &>/dev/null; then
    print_status "Connectivité Discord" 0
else
    print_status "Connectivité Discord" 1
fi

if ping -c 1 8.8.8.8 &>/dev/null; then
    print_status "Connectivité Internet" 0
else
    print_status "Connectivité Internet" 1
fi

# 7. Détails supplémentaires si demandés
if [ "$DETAILED" = "--detailed" ]; then
    echo -e "\n${BLUE}🔍 === DÉTAILS COMPLÉMENTAIRES ===${NC}"
    
    echo -e "\n${YELLOW}📊 Status systemd détaillé:${NC}"
    systemctl status monbotgaming --no-pager -l
    
    echo -e "\n${YELLOW}📝 Derniers logs (10 lignes):${NC}"
    journalctl -u monbotgaming --no-pager -n 10
    
    echo -e "\n${YELLOW}🔧 Configuration réseau:${NC}"
    ss -tuln | grep -E "(80|443|8000)"
    
    echo -e "\n${YELLOW}💾 Utilisation mémoire système:${NC}"
    free -h
fi

echo -e "\n${BLUE}=== FIN HEALTH CHECK ===${NC}"

# Code de sortie basé sur le status du service
exit $SERVICE_STATUS
