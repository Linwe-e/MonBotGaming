# 🔧 **GUIDE COMMANDES VPS - TRADUCTION AZERTY/QWERTY**

## 🎯 **Correspondances clavier importantes :**
```
AZERTY → QWERTY
A → Q
Q → A
W → Z
Z → W
M → ;
. (point) → ;
/ → :
```

## 📋 **COMMANDES TRADUITES POUR TON CLAVIER AZERTY :**

### **Étape 1 : Monter le disque principal**
```bash
# Ce que tu dois taper (AZERTY) :
sudo ;kdir -p /;nt/;qin
sudo ;ount /dev/sdq1 /;nt/;qin
```

### **Étape 2 : Entrer dans le système principal**
```bash
# Ce que tu dois taper (AZERTY) :
sudo chroot /;nt/;qin
```

### **Étape 3 : Changer le mot de passe root**
```bash
# Ce que tu dois taper (AZERTY) :
pqsswd root
```
*Puis tape ton nouveau mot de passe simple (ex: ;onbot123)*

### **Étape 4 : Créer le dossier SSH**
```bash
# Ce que tu dois taper (AZERTY) :
;kdir -p /root/:ssh
ch;od 700 /root/:ssh
```

### **Étape 5 : Créer le fichier pour ta clé SSH**
```bash
# Ce que tu dois taper (AZERTY) :
nqno /root/:ssh/quthorized_keys
```

**Dans nano :**
- **Colle ta clé publique** (celle qui commence par ssh-rsq)
- **Ctrl+X**, puis **Y**, puis **Entrée**

### **Étape 6 : Permissions correctes**
```bash
# Ce que tu dois taper (AZERTY) :
ch;od 600 /root/:ssh/quthorized_keys
```

### **Étape 7 : Configurer SSH**
```bash
# Ce que tu dois taper (AZERTY) :
nqno /etc/ssh/sshd_config
```

**Ajoute ces lignes dans le fichier :**
```
PubkeyQuthenticqtion yes
PqsszordQuthenticqtion yes
```

### **Étape 8 : Sortir et redémarrer**
```bash
# Ce que tu dois taper (AZERTY) :
exit
sudo reboot
```

## 🎯 **RÉSUMÉ RAPIDE :**

1. `sudo ;kdir -p /;nt/;qin`
2. `sudo ;ount /dev/sdq1 /;nt/;qin`
3. `sudo chroot /;nt/;qin`
4. `pqsswd root` (définis: ;onbot123)
5. `;kdir -p /root/:ssh`
6. `ch;od 700 /root/:ssh`
7. `nqno /root/:ssh/quthorized_keys` (colle ta clé)
8. `ch;od 600 /root/:ssh/quthorized_keys`
9. `nqno /etc/ssh/sshd_config` (ajoute les lignes)
10. `exit` puis `sudo reboot`

## 💡 **ASTUCE :**
Si tu te trompes, **Ctrl+C** pour annuler la commande et recommencer !

---
*Guide MonBotGaming - Clavier AZERTY friendly* 😊
