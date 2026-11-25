import sqlite3
from products import products

DB_NAME = "inventory.db"

#INITIALIZE DATABASE
def initialize_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                category TEXT NOT NULL DEFAULT 'Uncategorized'
            )
            
        """)
        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()
        
    
        
        
#LOADING SAMPLE PRODUCT
def load_sample_products():
    connection = sqlite3.connect(DB_NAME)
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        
        if count == 0:
            for product in products:
                if product.is_valid():
                    cursor.execute(
                        """
                        INSERT INTO products(name,price,quantity,category)
                        VALUES (?, ?, ?, ?)
                        """,
                        (product.name, product.price, product.quantity, product.category)  
                    )
                    
        connection.commit()
        
    finally:
        connection.close() 
#ADD PRODUCT
def add_product(name, price, quantity, category):
    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity, category) VALUES (?, ?, ?, ?)",
            (name, price, quantity, category)
        )
        connection.commit()
        
    except sqlite3.Error:
        connection.rollback()
        raise
        
    finally:
        connection.close()
        
#UPDATE PRODUCT
def update_product(product_id, name, price, quantity, category):
    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?, price = ?, quantity = ?, category = ?
            WHERE id = ?
        """, (name, price, quantity, category,  product_id))

        connection.commit()
        return cursor.rowcount
    
    except sqlite3.Error:
        connection.rollback()
        raise
        
    finally:
        connection.close()
        
        
#DELETE PRODUCT
def delete_product(product_id):
    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,)
        )
        connection.commit()
        return cursor.rowcount
    
    except sqlite3.Error:
        connection.rollback()
        raise
        
    finally:
        connection.close()
        
        
 #SEARCH PRODUCT       
def search_products(search_term):
    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM products
            WHERE name LIKE ?
        """, (f"%{search_term}%",))

        return cursor.fetchall()
    
        
    finally:
        connection.close()
        
        
 #GET PRODUCTS       
def get_products(category=None):
    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()

        if category and category != "All categories":
            cursor.execute(
                "SELECT * FROM products WHERE category = ?",
                (category,)
            )
        else:
            cursor.execute("SELECT * FROM products")

        return cursor.fetchall()

    except sqlite3.Error:
        raise

    finally:
        connection.close()

       