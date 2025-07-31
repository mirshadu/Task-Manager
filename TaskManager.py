import hashlib
import os
import sys

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
    print("\n=== User Registration ===")
    users = load_users()
    username = input("Enter a new username: ").strip()
    if username in users:
        print("⚠️ Username already exists. Please try another.")
        return False
    password = input("Enter a new password: ").strip()
    hashed = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{hashed}\n")
    print("✅ Registration successful!")
    return True

def login():
    print("\n=== User Login ===")
    users = load_users()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    hashed = hash_password(password)
    if username in users and users[username] == hashed:
        print(f"✅ Login successful! Welcome, {username}!")
        return username
    else:
        print("❌ Invalid credentials.")
        return None

def add_task(username):
    print("\n📌 Add New Task")
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

    print(f"✅ Task added with ID {task_id}.")

def view_tasks(username):
    print("\n📋 Your Task List")
    task_file = os.path.join(TASKS_DIR, f"{username}_tasks.txt")
    if not os.path.exists(task_file) or os.path.getsize(task_file) == 0:
        print("ℹ️ No tasks found.")
        return
    with open(task_file, "r") as f:
        print("-" * 40)
        print(f"{'ID':<5} {'Description':<20} {'Status':<10}")
        print("-" * 40)
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 3:
                print(f"{parts[0]:<5} {parts[1]:<20} {parts[2]:<10}")
        print("-" * 40)

def mark_task_completed(username):
    print("\n✅ Mark Task as Completed")
    task_file = os.path.join(TASKS_DIR, f"{username}_tasks.txt")
    if not os.path.exists(task_file):
        print("ℹ️ No tasks to update.")
        return

    task_id = input("Enter the ID of the task to mark as completed: ").strip()
    updated = False
    new_lines = []

    with open(task_file, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 3 and parts[0] == task_id:
                if parts[2] == "Completed":
                    print("⚠️ Task is already completed.")
                else:
                    parts[2] = "Completed"
                    print(f"✅ Task ID {task_id} marked as completed.")
                updated = True
                new_lines.append("|".join(parts) + "\n")
            else:
                new_lines.append(line)

    with open(task_file, "w") as f:
        f.writelines(new_lines)

    if not updated:
        print("❌ Task ID not found.")

def delete_task(username):
    print("\n🗑️ Delete Task")
    task_file = os.path.join(TASKS_DIR, f"{username}_tasks.txt")
    if not os.path.exists(task_file):
        print("ℹ️ No tasks to delete.")
        return

    task_id = input("Enter the ID of the task to delete: ").strip()
    deleted = False
    new_lines = []

    with open(task_file, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 3 and parts[0] == task_id:
                deleted = True
                continue  # Skip this line (delete)
            new_lines.append(line)

    with open(task_file, "w") as f:
        f.writelines(new_lines)

    if deleted:
        print(f"✅ Task ID {task_id} deleted.")
    else:
        print("❌ Task ID not found.")

def main_menu(user):
    while True:
        print("\n🔸🔹🔸 Task Manager Menu 🔸🔹🔸")
        print("1. ➕ Add a Task")
        print("2. 📄 View Tasks")
        print("3. ✅ Mark Task as Completed")
        print("4. 🗑️ Delete a Task")
        print("5. 🚪 Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(user)
        elif choice == "2":
            view_tasks(user)
        elif choice == "3":
            mark_task_completed(user)
        elif choice == "4":
            delete_task(user)
        elif choice == "5":
            print("👋 Logged out successfully.")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    print("📌 Welcome to Task Manager with User Authentication 📌")
    while True:
        print("\nMain Menu")
        print("1. 📝 Register")
        print("2. 🔐 Login")
        print("3. ❌ Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please enter 1, 2, or 3.")
