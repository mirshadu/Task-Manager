import hashlib
import os

USERS_FILE = "users.txt"
TASKS_DIR = "tasks"  # directory to store task files

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

def add_task(username):
    if not os.path.exists(TASKS_DIR):
        os.makedirs(TASKS_DIR)

    task_file = os.path.join(TASKS_DIR, f"{username}_tasks.txt")
    task_description = input("Enter task description: ").strip()

    task_id = 1
    if os.path.exists(task_file):
        with open(task_file, "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                task_id = int(last_line.split("|")[0]) + 1

    with open(task_file, "a") as f:
        f.write(f"{task_id}|{task_description}|Pending\n")

    print(f"Task '{task_description}' added with ID {task_id}.")

def main_menu(user):
    while True:
        print("\n--- Task Manager Menu ---")
        print("1. Add a Task")
        print("2. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(user)
        elif choice == "2":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please enter a valid choice (1 or 2).")

if __name__ == "__main__":
    while True:
        print("\n1. Register\n2. Login")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        else:
            print("Invalid option. Please enter 1 or 2.")
