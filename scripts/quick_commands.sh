#!/bin/bash
# quick_commands.sh - Commandes rapides pour gérer MonBotGaming
# Usage: ./quick_commands.sh [start|stop|restart|status|logs|backup|update]

BOT_USER="botgaming"
BOT_DIR="/home/${BOT_USER}/MonBotGaming"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

case "$1" in
    start)
        echo -e "${GREEN}🚀 Démarrage MonBotGaming...${NC}"
        systemctl start monbotgaming
        systemctl status monbotgaming --no-pager -l
        ;;
    
    stop)
        echo -e "${YELLOW}⏹️  Arrêt MonBotGaming...${NC}"
        systemctl stop monbotgaming
        echo -e "${GREEN}✅ Bot arrêté${NC}"
        ;;
    
    restart)
        echo -e "${BLUE}🔄 Redémarrage MonBotGaming...${NC}"
        systemctl restart monbotgaming
        sleep 3
        systemctl status monbotgaming --no-pager -l
        ;;
    
    status)
        echo -e "${BLUE}📊 Status MonBotGaming${NC}"
        systemctl status monbotgaming --no-pager -l
        echo ""
        $BOT_DIR/../scripts/monitor_bot.sh 2>/dev/null || echo "Script monitor non trouvé"
        ;;
    
    logs)
        echo -e "${BLUE}📝 Logs MonBotGaming (temps réel)${NC}"
        echo "Appuyez sur Ctrl+C pour quitter"
        journalctl -u monbotgaming -f
        ;;
    
    backup)
        echo -e "${GREEN}💾 Création backup...${NC}"
        sudo -u $BOT_USER $BOT_DIR/../scripts/backup_bot.sh
        ;;
    
    update)
        echo -e "${BLUE}📥 Mise à jour MonBotGaming...${NC}"
        $BOT_DIR/../scripts/deploy.sh
        ;;
    
    health)
        echo -e "${BLUE}🏥 Health Check${NC}"
        $BOT_DIR/../scripts/health_check.sh
        ;;
    
    *)
        echo -e "${YELLOW}🎮 MonBotGaming - Commandes Rapides${NC}"
        echo ""
        echo "Usage: $0 [commande]"
        echo ""
        echo "Commandes disponibles:"
        echo -e "  ${GREEN}start${NC}     - Démarrer le bot"
        echo -e "  ${YELLOW}stop${NC}      - Arrêter le bot"
        echo -e "  ${BLUE}restart${NC}   - Redémarrer le bot"
        echo -e "  ${BLUE}status${NC}    - Afficher le status"
        echo -e "  ${BLUE}logs${NC}      - Suivre les logs en temps réel"
        echo -e "  ${GREEN}backup${NC}    - Créer un backup"
        echo -e "  ${BLUE}update${NC}    - Mettre à jour le bot"
        echo -e "  ${BLUE}health${NC}    - Vérification santé complète"
        echo ""
        echo "Exemples:"
        echo "  $0 start"
        echo "  $0 logs"
        echo "  $0 health"
        ;;
esac
