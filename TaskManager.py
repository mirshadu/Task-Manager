import hashlib
import os

USERS_FILE = "users.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                username, hashed = line.strip().split(":")
                users[username] = hashed
    return users

def register():
    users = load_users()
    username = input("Enter a new username: ").strip()
    if username in users:
        print("Username already exists. Please try another.")
        return False
    password = input("Enter a new password: ").strip()
    hashed = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{hashed}\n")
    print("Registration successful!")
    return True

def login():
    users = load_users()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    hashed = hash_password(password)
    if username in users and users[username] == hashed:
        print("Login successful!")
        return username
    else:
        print("Invalid credentials.")
        return None

# Example usage:
if __name__ == "__main__":
    print("1. Register\n2. Login")
    choice = input("Choose an option: ")
    if choice == "1":
        register()
    elif choice == "2":
        user = login()
        if user:
            print(f"Welcome, {user}!")