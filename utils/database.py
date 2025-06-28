import sqlite3
import os

DATABASE_NAME = 'monbotgaming.db'
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', DATABASE_NAME)

class Database:
    def __init__(self, db_path=None):
        self.conn = None
        self.cursor = None
        self.db_path = db_path or DB_PATH
        self._connect()
        self._initialize_db()

    def _connect(self):
        """Établit la connexion à la base de données."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"✅ Connecté à la base de données : {self.db_path}")
        except sqlite3.Error as e:
            print(f"❌ Erreur de connexion à la base de données : {e}")
            # Gérer l'erreur de manière plus robuste en production

    def _initialize_db(self):
        """Initialise les tables nécessaires si elles n'existent pas."""
        if not self.conn:
            return

        try:
            # Exemple de table pour les utilisateurs
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    last_activity TEXT,
                    consent_given INTEGER DEFAULT 0,
                    consent_date TEXT
                )
            """)
            # Exemple de table pour les builds de jeux
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_builds (
                    build_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_name TEXT NOT NULL,
                    build_name TEXT NOT NULL,
                    description TEXT,
                    author_id INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (author_id) REFERENCES users(user_id)
                )
            """)
            self.conn.commit()
            print("✅ Tables de la base de données vérifiées/créées.")
        except sqlite3.Error as e:
            print(f"❌ Erreur lors de l'initialisation de la base de données : {e}")
            self.conn.rollback()

    def execute_query(self, query, params=()):
        """Exécute une requête SQL et retourne les résultats."""
        if not self.conn:
            print("⚠️ Pas de connexion à la base de données.")
            return None
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Erreur lors de l'exécution de la requête : {e}")
            self.conn.rollback()
            return None

    def close(self):
        """Ferme la connexion à la base de données."""
        if self.conn:
            self.conn.close()
            print("🔌 Connexion à la base de données fermée.")

# Instancier la base de données pour l'importation
# (utilise le chemin par défaut)
db = Database()

# Assurez-vous que le dossier 'data' existe
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
os.makedirs(data_dir, exist_ok=True)
