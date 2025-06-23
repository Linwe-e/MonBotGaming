# 🔐 **Connexion PuTTY avec Clé SSH - Guide Étape par Étape**

## 🎯 **Tu es ici : Utiliser ta clé privée pour te connecter**

### **Étape 1 : Localiser ta clé privée**
- Tu as généré une clé avec le script batch
- Cherche le fichier **`monbotgaming_private.ppk`** sur ton ordinateur
- Il devrait être dans le dossier où tu as exécuté le script

### **Étape 2 : Configuration PuTTY avec clé**

1. **Lance PuTTY**

2. **Configuration de base :**
   - **Host Name** : `[TON_IP_VPS]`
   - **Port** : `22`
   - **Connection type** : `SSH`

3. **Configuration de la clé (IMPORTANT) :**
   - Dans le menu de gauche : **Connection > SSH > Auth > Credentials**
   - **"Private key file for authentication"** :
     - Clique sur **"Browse..."**
     - Sélectionne ton fichier **`monbotgaming_private.ppk`**

4. **Retour à Session :**
   - Nomme ta session : `VPS MonBot`
   - Clique sur **"Save"**

5. **Connexion :**
   - Clique sur **"Open"**
   - **Login as:** `root`
   - **Pas de mot de passe !** (authentification automatique par clé)

## 🔍 **Si ça ne marche toujours pas...**

### **Vérification 1 : Format de la clé**
Ta clé privée doit être au format `.ppk` (PuTTY Private Key).

### **Vérification 2 : Clé publique sur le serveur**
Il faut que ta clé publique soit présente sur le VPS. Deux méthodes :

#### **Méthode A : Console VNC Infomaniak**
1. **Manager Infomaniak** → **Produits** → **Ton VPS**
2. **Console VNC** (icône écran)
3. **Login** : `root` + mot de passe VPS
4. **Commandes** :
```bash
# Création dossier SSH
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Éditer le fichier authorized_keys
nano ~/.ssh/authorized_keys
```
5. **Colle le contenu de ton fichier `monbotgaming_public.pub`**
6. **Sauvegarde** : `Ctrl+X`, puis `Y`, puis `Enter`
7. **Permissions** :
```bash
chmod 600 ~/.ssh/authorized_keys
chown root:root ~/.ssh/authorized_keys
```

#### **Méthode B : Interface Manager (si disponible)**
- **Manager Infomaniak** → **VPS** → **SSH Keys**
- **Add Key** → Colle le contenu de `monbotgaming_public.pub`

## 🚨 **Dépannage Avancé**

### **Si l'authentification par clé échoue encore :**

1. **Réactiver temporairement l'authentification par mot de passe** (via console VNC) :
```bash
# Éditer la config SSH
nano /etc/ssh/sshd_config

# Trouver et modifier ces lignes :
PasswordAuthentication yes
PubkeyAuthentication yes
AuthenticationMethods publickey password

# Redémarrer SSH
systemctl restart sshd
```

2. **Puis te reconnecter avec PuTTY** et tester l'authentification par mot de passe.

## 📞 **Besoin d'aide ?**

Si tu es bloquée, dis-moi :
1. **As-tu trouvé ton fichier `.ppk` ?**
2. **L'erreur exacte** que tu reçois
3. **Préfères-tu** que je t'aide via console VNC ?

---
*Guide MonBotGaming - Configuration SSH sécurisée*
