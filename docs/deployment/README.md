# 🚀 Guide de Déploiement Complet - MonBotGaming sur VPS

Ce guide centralise toutes les étapes nécessaires pour déployer, configurer et maintenir le bot MonBotGaming sur un VPS Infomaniak.

## 📋 Table des Matières
1.  [Prérequis](#-prérequis)
2.  [Étape 1 : Configuration de l'Accès SSH](#-étape-1--configuration-de-laccès-ssh)
    *   [Génération des Clés SSH](#génération-des-clés-ssh)
    *   [Ajout de la Clé Publique au VPS](#ajout-de-la-clé-publique-au-vps)
    *   [Configuration du Client SSH (PuTTY)](#configuration-du-client-ssh-putty)
3.  [Étape 2 : Installation Initiale du VPS](#-étape-2--installation-initiale-du-vps)
4.  [Étape 3 : Déploiement du Bot](#-étape-3--déploiement-du-bot)
5.  [Étape 4 : Gestion Quotidienne du Bot](#-étape-4--gestion-quotidienne-du-bot)
6.  [🔧 Dépannage (Troubleshooting)](#-dépannage-troubleshooting)
    *   [Problème : `Permission denied (publickey)`](#problème--permission-denied-publickey)
    *   [Autres Erreurs Courantes](#autres-erreurs-courantes)

---

## ✅ Prérequis

*   Un VPS Infomaniak (ou autre) avec un système d'exploitation Debian ou Ubuntu.
*   Le client [PuTTY](https://www.putty.org/) installé sur votre machine Windows.

---

## 🔑 Étape 1 : Configuration de l'Accès SSH

La connexion par clé SSH est la méthode la plus sécurisée pour accéder à votre VPS.

### Génération des Clés SSH

Nous utilisons **PuTTYgen** pour créer une paire de clés (publique et privée).

1.  **Lancez PuTTYgen.**
2.  Sélectionnez `RSA` comme type de clé et `4096` pour le nombre de bits.
3.  Cliquez sur **"Generate"** et bougez votre souris pour créer de l'aléa.
4.  Une fois la clé générée :
    *   **Sauvegardez la clé publique** : Cliquez sur "Save public key" et nommez-la `monbotgaming_public.pub`.
    *   **Sauvegardez la clé privée** : Cliquez sur "Save private key" et nommez-la `monbotgaming_private.ppk`. **Ne partagez jamais ce fichier !**

### Ajout de la Clé Publique au VPS

Vous devez copier le contenu de votre clé publique (`monbotgaming_public.pub`) sur le VPS.

1.  Connectez-vous au **Manager Infomaniak**.
2.  Allez dans la section de gestion de votre VPS, trouvez l'option "Clés SSH" ou "Accès SSH".
3.  Cliquez sur "Ajouter une clé SSH".
4.  Ouvrez votre fichier `monbotgaming_public.pub` avec un éditeur de texte, copiez tout son contenu et collez-le dans le champ prévu sur l'interface d'Infomaniak.

### Configuration du Client SSH (PuTTY)

1.  **Lancez PuTTY.**
2.  Dans `Session` :
    *   **Host Name (or IP address)**: `83.228.195.70`
    *   **Port**: `22`
3.  Dans `Connection > SSH > Auth > Credentials` :
    *   Cliquez sur **"Browse..."** à côté de "Private key file for authentication".
    *   Sélectionnez votre fichier de clé privée `monbotgaming_private.ppk`.
4.  Retournez dans `Session`, donnez un nom à votre session (ex: `MonBotGaming VPS`) et cliquez sur **"Save"**.

Vous pouvez maintenant vous connecter en double-cliquant sur la session sauvegardée. Le login est `root`.

---

## ⚙️ Étape 2 : Installation Initiale du VPS

Une fois connecté en SSH, lancez le script d'installation complet. Ce script va préparer l'environnement, installer Python, sécuriser le serveur et mettre en place les services.

```bash
# Télécharger le script d'installation
wget https://raw.githubusercontent.com/Linwe-e/MonBotGaming/main/scripts/setup_vps.sh
chmod +x setup_vps.sh

# Exécuter l'installation
sudo ./setup_vps.sh
```

---

## 🚀 Étape 3 : Déploiement du Bot

Après l'installation, configurez et lancez le bot.

1.  **Configurez les secrets :**
    ```bash
    # Éditez le fichier .env pour y mettre vos tokens
    nano /home/botgaming/MonBotGaming/.env
    ```
    Remplissez `DISCORD_TOKEN` et `GEMINI_API_KEY` avec vos valeurs.

2.  **Démarrez le service du bot :**
    ```bash
    sudo systemctl start monbotgaming
    ```

3.  **Vérifiez que tout fonctionne :**
    ```bash
    sudo systemctl status monbotgaming
    # Pour voir les logs en direct
    tail -f /home/botgaming/logs/bot.log
    ```

---

## 🎮 Étape 4 : Gestion Quotidienne du Bot

Des scripts sont à votre disposition pour gérer le bot facilement.

*   **Mettre à jour le bot :** `sudo /home/botgaming/scripts/deploy.sh`
*   **Vérifier la santé du bot :** `sudo /home/botgaming/scripts/health_check.sh`
*   **Commandes rapides (start, stop, restart, status, logs) :** `/home/botgaming/scripts/quick_commands.sh [commande]`

---

## 🔧 Dépannage (Troubleshooting)

### Problème : `Permission denied (publickey)`

C'est l'erreur la plus courante. Elle signifie que le serveur refuse votre clé.

**Solutions (en mode rescue) :**

Si vous ne pouvez plus vous connecter, passez le VPS en **mode rescue** depuis le manager Infomaniak et connectez-vous avec le mot de passe temporaire fourni.

Ensuite, montez votre système de fichiers :
```bash
mount /dev/sda2 /mnt
mount /dev/sda1 /mnt/boot
chroot /mnt
```

1.  **Vérifier la présence de la clé :**
    ```bash
    cat /root/.ssh/authorized_keys
    ```
    Assurez-vous que le contenu de votre clé publique y figure. Si ce n'est pas le cas, ajoutez-le.

2.  **Vérifier les permissions des fichiers :** C'est une cause très fréquente.
    ```bash
    chmod 700 /root/.ssh
    chmod 600 /root/.ssh/authorized_keys
    chown -R root:root /root/.ssh
    ```

3.  **Vérifier la configuration du service SSH :**
    ```bash
    grep -E "(PubkeyAuthentication|PasswordAuthentication|PermitRootLogin)" /etc/ssh/sshd_config
    ```
    Assurez-vous que `PubkeyAuthentication` est bien sur `yes`.

4.  **Tester la configuration SSH :**
    ```bash
    sshd -t
    ```
    Cette commande ne doit retourner aucune erreur.

Une fois les corrections faites, quittez le mode `chroot`, démontez les disques et redémarrez le VPS en mode normal.

### Autres Erreurs Courantes

| Erreur | Cause probable | Solution |
|---|---|---|
| `Connection refused` | Le service SSH n'est pas démarré ou n'écoute pas sur le bon port. | En mode rescue, activez le service : `systemctl enable sshd` |
| `Host key verification failed` | La clé d'hôte du serveur a changé. | Supprimez l'ancienne clé de votre PC : `ssh-keygen -R 83.228.195.70` |
| `Connection timed out` | Un firewall bloque la connexion. | Vérifiez la configuration du firewall sur le manager Infomaniak et sur le VPS (`ufw status`). |
