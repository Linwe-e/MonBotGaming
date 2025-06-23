# Configuration PuTTY Optimisée pour MonBotGaming VPS

## 🎯 Configuration Session PuTTY

### **1. Connexion de Base**
- **Host Name** : `83.228.195.70`
- **Port** : `22`
- **Connection type** : `SSH`

### **2. Paramètres Terminal (si écran noir)**
- **Terminal** > **Features** :
  - ✅ Enable blinking text
  - ✅ Use background colour to erase screen
- **Terminal** > **Bell** :
  - ✅ Visual bell (flash window)
- **Window** > **Colours** :
  - Use system colours: **No**
  - Foreground: **White** (255,255,255)
  - Background: **Black** (0,0,0)

### **3. Connexion (si lenteur)**
- **Connection** :
  - TCP keepalives: **15** seconds
  - Reuse connection: **Yes**
- **Connection** > **SSH** :
  - SSH protocol version: **2 only**
  - Compression: **Enable**

### **4. Sauvegarde Session**
1. Retourne à **Session**
2. **Saved Sessions** : `MonBotGaming-VPS-Optimized`
3. **Save**

## 🚀 Test de Connexion Rapide

### **Méthode 1: Reset Complet**
1. **Ferme PuTTY**
2. **Relance PuTTY**
3. **Tape directement** :
   - Host: `83.228.195.70`
   - **Open** (sans sauvegarder)

### **Méthode 2: Test avec Telnet**
Pour vérifier si le port est accessible :
```cmd
telnet 83.228.195.70 22
```
Si ça marche, tu verras : `SSH-2.0-OpenSSH_...`

### **Méthode 3: Alternative - Console VNC**
Si PuTTY pose problème :
1. **Manager Infomaniak** > **VPS** > **Console**
2. **Console VNC** (dans le navigateur)
3. Direct accès au terminal !

## 🔧 Commandes Test une fois connecté

Quand tu auras un terminal qui répond :
```bash
# Test de base
whoami
pwd
ls -la

# Si ça marche, on lance l'installation
wget https://raw.githubusercontent.com/Linwe-e/MonBotGaming/main/scripts/setup_vps.sh
chmod +x setup_vps.sh
sudo ./setup_vps.sh
```

## 📞 Solutions de Secours

**Si PuTTY ne fonctionne vraiment pas :**

1. **WSL** (Windows Subsystem for Linux) :
   ```cmd
   ssh root@83.228.195.70
   ```

2. **PowerShell SSH** :
   ```powershell
   ssh root@83.228.195.70
   ```

3. **Console Web Infomaniak** (la plus fiable)

---

**🎮 L'objectif reste le même : accéder au terminal de ton VPS pour installer le bot gaming ! 🎮**
