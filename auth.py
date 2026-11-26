import bcrypt


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