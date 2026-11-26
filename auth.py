import bcrypt
import sqlite3

from database import DB_NAME


def hash_password(password):
    password_bytes = password.encode("utf-8")

    password_hash = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return password_hash.decode("utf-8")


def verify_password(password, stored_hash):
    password_bytes = password.encode("utf-8")
    stored_hash_bytes = stored_hash.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        stored_hash_bytes
    )
    
def register_admin(username, password):

    # Validate username
    username = username.strip()

    if not username:
        raise ValueError("Username cannot be empty.")

    # Validate password
    if not password:
        raise ValueError("Password cannot be empty.")

    if len(password) < 12:
        raise ValueError("Password must contain at least 12 characters.")

    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password cannot exceed 72 UTF-8 bytes.")

    # Hash the password
    password_hash = hash_password(password)

    # Connect to database
    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO admin_users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))

        connection.commit()

        return True

    except sqlite3.IntegrityError:
        connection.rollback()
        return False

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()
        
        
def authenticate_admin(username, password):
    username = username.strip()

    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, username, password_hash
            FROM admin_users
            WHERE username = ?
        """, (username,))

        admin = cursor.fetchone()

        if admin is None:
            return None

        admin_id, stored_username, stored_hash = admin

        if verify_password(password, stored_hash):
            return {
                "id": admin_id,
                "username": stored_username
            }

        return None

    finally:
        connection.close()
