from getpass import getpass

from auth import register_admin
from database import initialize_db


def main():
    initialize_db()

    print("\nSMARTSTOCK ADMIN SETUP")

    username = input("Enter admin username: ")
    password = getpass("Enter admin password: ")
    confirm_password = getpass("Confirm admin password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    try:
        registered = register_admin(username, password)

        if registered:
            print("Administrator created successfully!")
        else:
            print("That username already exists.")

    except ValueError as error:
        print(f"Registration error: {error}")


if __name__ == "__main__":
    main()