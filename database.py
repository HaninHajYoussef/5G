import bcrypt
import sqlite3

DB_NAME = "users.db"

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    conn.commit()
    conn.close()

# Ajouter un utilisateur
def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        return False  # L'utilisateur existe déjà
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur SQL : {e}")
        conn.close()
        return False
    finally:
        conn.close()
    
    return True

# Vérifier l'utilisateur
def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    return False

# Initialisation de la base de données
init_db()

# Ajouter l'utilisateur
username = "zainebhanin"
password = "zaineb2002"

if add_user(username, password):
    print(f"Utilisateur {username} ajouté avec succès.")
else:
    print("L'utilisateur existe déjà ou une erreur est survenue.")

# Vérifier les identifiants
if verify_user(username, password):
    print("Connexion réussie !")
else:
    print("Identifiants incorrects.")