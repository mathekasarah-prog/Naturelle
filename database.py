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
        
def load_sample_products():
    connection = sqlite3.connect(DB_NAME)
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM prooducts")
        count = cursor.fetchone()[0]
        
        if count == 0:
            for product in products:
                if product.is_valid():
                    cursor.execute(
                        """
                        INSERT INTO products(name,price,quantity)
                        VALUES (?, ?, ?)
                        """,
                        (product.name, product.price, product.quantity)  
                    )
                    
        connection.commit()
        
    finally:connection.close()        