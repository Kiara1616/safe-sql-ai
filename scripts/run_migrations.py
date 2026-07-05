import sqlite3
import os

# Base de datos estará en la raíz del proyecto cuando se ejecute desde allí
DB_NAME = "safe_sql_demo.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def setup_db():
    print("Iniciando migraciones...")
    if os.path.exists(DB_NAME):
        print("Eliminando base de datos antigua...")
        os.remove(DB_NAME)
    
    with get_connection() as conn:
        with open("migrations/schema.sql", "r") as f:
            conn.executescript(f.read())
        with open("migrations/sample_data.sql", "r") as f:
            conn.executescript(f.read())
            
    print("Migraciones ejecutadas exitosamente. Base de datos lista.")

if __name__ == "__main__":
    setup_db()
