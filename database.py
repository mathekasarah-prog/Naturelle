import sqlite3
from products import products

DB_NAME = "inventory.db"

def initialize_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
            
        """)
        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()
        
        