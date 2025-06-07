import os
from datetime import datetime

EMPLOYEE_FILE = "employee_data.txt"
USER_FILE = "user_login.txt"

# === Class Definition ===
class Login:
    def __init__(self, user_id, password, auth_code):
        self.user_id = user_id
        self.password = password
        self.auth_code = auth_code

# === User Management Functions ===
def add_users():
    print("=== Add New Users ===")
    user_ids = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            for line in file:
                existing_user_id = line.strip().split("|")[0]
                user_ids.append(existing_user_id)

    while True:
        user_id = input("Enter new user ID (or 'End' to stop): ")
        if user_id.lower() == "end":
            break
        if user_id in user_ids:
            print("User ID already exists. Try another.")
            continue

        password = input("Enter password: ")
        auth_code = input("Enter authorization (Admin/User): ")
        if auth_code.lower() not in ["admin", "user"]:
            print("Authorization must be 'Admin' or 'User'. Try again.")
            continue

        with open(USER_FILE, "a") as file:
            file.write(f"{user_id}|{password}|{auth_code}\n")
        user_ids.append(user_id)
        print("User added.\n")

def display_users():
    print("\n=== Registered Users ===")
    if not os.path.exists(USER_FILE):
        print("No users found.")
        return

    with open(USER_FILE, "r") as file:
        for line in file:
            user_id, password, auth_code = line.strip().split("|")
            print(f"User ID: {user_id}, Password: {password}, Role: {auth_code}")
    print()

def login():
    print("\n=== Login ===")
    if not os.path.exists(USER_FILE):
        print("No user login file found.")
        return None

    user_list = []
    with open(USER_FILE, "r") as file:
        for line in file:
            user_id, password, auth_code = line.strip().split("|")
            user_list.append((user_id, password, auth_code))

    user_id = input("Enter User ID: ")
    password = input("Enter Password:


