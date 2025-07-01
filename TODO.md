# To-Do List - Améliorations du Code

Liste des tâches mise à jour après synchronisation avec le dépôt distant.

## 🚀 Tâche Prioritaire : Finaliser la Migration vers SQLite

- [ ] **Adapter le système RGPD à SQLite :** Le module `utils/data_management/rgpd_conversation_memory.py` fonctionne encore avec ses propres fichiers JSON. La tâche principale est de le modifier pour qu'il lise et écrive les consentements et les conversations dans la base de données SQLite gérée par `utils/database.py`. Cela unifiera la gestion des données.

## 🎨 Interface Utilisateur et Expérience

- [ ] **Harmoniser l'embed/visuel des réponses du bot :** Revoir la cohérence entre les réponses longues/tronquées et le style visuel (notamment la barre verte/format embed). Assurer que toutes les réponses du bot aient un format uniforme et professionnel, éviter les troncatures inattendues et maintenir la cohérence visuelle.

## 🧠 IA et Personnalisation

- [ ] **Créer un Profil IA Évolutif :** Au lieu de simplement supprimer les messages après 48h, implémenter une tâche qui demande à l'IA de résumer la conversation en un "profil de joueur" (ex: jeux préférés, style de jeu). Ce résumé serait stocké (avec consentement) et utilisé pour personnaliser les futures interactions, offrant une personnalisation à long terme sans stocker l'historique complet des messages.

## 🧹 Refactoring et Qualité du Code

- [ ] **Factoriser la gestion des réponses longues :** La logique pour découper les réponses de l'IA en plusieurs messages est présente à la fois dans `main.py` et dans plusieurs commandes de `cogs/ai_gaming.py`. Il faudrait la centraliser dans une fonction (par exemple dans `utils/discord_helpers/embed_helpers.py`) pour éviter la duplication.

- [ ] **Déplacer les imports locaux dans `main.py` :** La fonction `on_message` effectue des imports locaux. Pour une meilleure lisibilité et par convention, ils devraient être déplacés en haut du fichier.
