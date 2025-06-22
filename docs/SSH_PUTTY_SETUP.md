# 🔑 Instructions Configuration SSH PuTTY pour MonBotGaming VPS

## 📋 **Étapes pour configurer PuTTY avec clé SSH**

### **Étape 1: Génération de la clé SSH** ✅

Tu as PuTTY installé, parfait ! Utilisons **PuTTYgen** pour générer directement une clé au bon format.

### **Étape 2: Utiliser PuTTYgen**

1. **Lance PuTTYgen** (devrait être installé avec PuTTY)
2. **Paramètres de génération :**
   - Type: `RSA`
   - Number of bits: `4096`
3. **Clique sur "Generate"**
4. **Bouge la souris** dans la zone vide pour générer de l'aléatoire
5. **Sauvegarde :**
   - **"Save public key"** → `monbotgaming_public.pub`
   - **"Save private key"** → `monbotgaming_private.ppk`

### **Étape 3: Configuration VPS Infomaniak**

#### **Option A: Via Console VNC**
1. Connecte-toi à la **Console VNC** sur Manager Infomaniak
2. **Login avec ton mot de passe VPS**
3. **Ajoute la clé publique :**

```bash
# Création du dossier .ssh
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Ajouter ta clé publique (copie le contenu de monbotgaming_public.pub)
nano ~/.ssh/authorized_keys
# Colle le contenu de ta clé publique ici
# Sauvegarde avec Ctrl+X, Y, Enter

# Permissions correctes
chmod 600 ~/.ssh/authorized_keys
chown -R root:root ~/.ssh
```

#### **Option B: Via Interface Infomaniak** 
Certains Manager Infomaniak permettent d'uploader directement les clés SSH :
1. **Manager Infomaniak** > **VPS** > **Sécurité/SSH**
2. **Upload** ou **Add SSH Key**
3. **Colle le contenu** de `monbotgaming_public.pub`

### **Étape 4: Configuration PuTTY**

1. **Lance PuTTY**
2. **Configuration :**
   - **Host Name** : `YOUR_VPS_IP`
   - **Port** : `22`
   - **Connection type** : `SSH`

3. **Dans le menu gauche :**
   - **Connection** > **SSH** > **Auth** > **Credentials**
   - **Private key file** : Browse → `monbotgaming_private.ppk`

4. **Sauvegarde la session :**
   - **Session** (menu gauche)
   - **Saved Sessions** : `MonBotGaming-VPS`
   - **Save**

### **Étape 5: Test de Connexion**

1. **Double-clique** sur `MonBotGaming-VPS` dans tes sessions sauvées
2. **Login as** : `root` (ou l'utilisateur de ton VPS)
3. **Tu devrais être connecté sans mot de passe !** 🎉

### **Étape 6: Installation Bot (une fois connecté)**

```bash
# Une fois connecté via PuTTY :
wget https://raw.githubusercontent.com/Linwe-e/MonBotGaming/main/scripts/setup_vps.sh
chmod +x setup_vps.sh
sudo ./setup_vps.sh
```

## 🎯 **Avantages PuTTY + Clé SSH :**

- ✅ **Sécurité renforcée** (plus de mot de passe)
- ✅ **Connexion rapide** (double-clic)
- ✅ **Sessions sauvegardées**
- ✅ **Copier/coller** facile entre Windows et Linux
- ✅ **Tunneling** pour interfaces web

## 🔧 **Fichiers générés :**

- `monbotgaming_private.ppk` : **Clé privée PuTTY** (à garder secrète !)
- `monbotgaming_public.pub` : **Clé publique** (à installer sur le VPS)

## 🆘 **En cas de problème :**

**Connexion refusée :**
- Vérifier que le port 22 est ouvert dans le firewall Infomaniak
- S'assurer que SSH est activé sur le VPS

**Authentication failed :**
- Vérifier que la clé publique est bien dans `~/.ssh/authorized_keys`
- Vérifier les permissions (600 pour authorized_keys, 700 pour .ssh)

---

**🎮 Une fois connecté, on lance l'installation de ton bot gaming ! 🎮**
