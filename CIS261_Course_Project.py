import os
from datetime import datetime

EMPLOYEE_FILE = "employee_data.txt"
USER_FILE = "users.txt"

# ===============================
# CLASS FOR LOGIN OBJECT
# ===============================
class Login:
    def __init__(self, user_id, password, role):
        self.user_id = user_id
        self.password = password
        self.role = role

# ===============================
# USER MANAGEMENT FUNCTIONS
# ===============================
def load_users():
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                user_id, password, role = line.strip().split("|")
                users.append(Login(user_id, password, role))
    return users

def save_user(user_id, password, role):
    with open(USER_FILE, "a") as f:
        f.write(f"{user_id}|{password}|{role}\n")

def setup_users():
    users = load_users()
    existing_ids = [u.user_id for u in users]

    print("\n=== SETUP USERS ===")
    while True:
        user_id = input("Enter new user ID (or 'End' to stop): ")
        if user_id.lower() == "end":
            break
        if user_id in existing_ids:
            print("User ID already exists. Try another.")
            continue
        password = input("Enter password: ")
        role = input("Enter role (Admin/User): ").capitalize()
        if role not in ["Admin", "User"]:
            print("Invalid role. Must be 'Admin' or 'User'.")
            continue
        save_user(user_id, password, role)
        print(f"User '{user_id}' added as {role}.\n")
        existing_ids.append(user_id)

# ===============================
# LOGIN VALIDATION FUNCTION
# ===============================
def login_user():
    users = load_users()
    print("\n=== LOGIN ===")
    user_id = input("User ID: ")
    password = input("Password: ")
    for u in users:
        if u.user_id == user_id:
            if u.password == password:
                print(f"\nLogin successful. Welcome, {u.user_id} ({u.role})!\n")
                return u
            else:
                print("Incorrect password.\n")
                return None
    print("User not found.\n")
    return None

# ===============================
# PAYROLL FUNCTIONS
# ===============================
def get_employee_entry():
    from_date = input("Enter FROM date (mm/dd/yyyy): ")
    to_date = input("Enter TO date (mm/dd/yyyy): ")
    name = input("Enter employee name: ")
    hours = float(input("Enter total hours worked: "))
    rate = float(input("Enter hourly rate: "))
    tax_rate = float(input("Enter tax rate (e.g., 0.20 for 20%): "))
    return from_date, to_date, name, hours, rate, tax_rate

def calculate_pay(hours, rate, tax_rate):
    gross = hours * rate
    income_tax = gross * tax_rate
    net_pay = gross - income_tax
    return gross, income_tax, net_pay

def save_payroll_record(from_date, to_date, name, hours, rate, tax_rate):
    with open(EMPLOYEE_FILE, "a") as f:
        f.write(f"{from_date}|{to_date}|{name}|{hours}|{rate}|{tax_rate}\n")

def display_payroll_records():
    if not os.path.exists(EMPLOYEE_FILE):
        print("No payroll records found.")
        return

    filter_date = input("Enter FROM date to filter (mm/dd/yyyy) or 'All': ")

    totals = {"employees": 0, "hours": 0, "gross": 0, "tax": 0, "net": 0}
    with open(EMPLOYEE_FILE, "r") as f:
        for line in f:
            from_date, to_date, name, hours, rate, tax_rate = line.strip().split("|")
            if filter_date.lower() != "all" and from_date != filter_date:
                continue

            hours = float(hours)
            rate = float(rate)
            tax_rate = float(tax_rate)
            gross, tax, net = calculate_pay(hours, rate, tax_rate)

            print(f"\nFrom: {from_date}  To: {to_date}")
            print(f"Name: {name}")
            print(f"Hours: {hours:.2f}  Rate: ${rate:.2f}")
            print(f"Gross: ${gross:.2f}  Tax: ${tax:.2f}  Net: ${net:.2f}")

            totals["employees"] += 1
            totals["hours"] += hours
            totals["gross"] += gross
            totals["tax"] += tax
            totals["net"] += net

    print("\n===== PAYROLL SUMMARY =====")
    print(f"Employees: {totals['employees']}")
    print(f"Total Hours: {totals['hours']:.2f}")
    print(f"Total Gross Pay: ${totals['gross']:.2f}")
    print(f"Total Tax: ${totals['tax']:.2f}")
    print(f"Total Net Pay: ${totals['net']:.2f}")
    print("===========================\n")

# ===============================
# MAIN PROGRAM FLOW
# ===============================
def admin_menu():
    while True:
        print("A) Enter Payroll")
        print("B) View Payroll")
        print("C) Logout to Main Menu")
        option = input("Select option: ").upper()

        if option == "A":
            from_date, to_date, name, hours, rate, tax_rate = get_employee_entry()
            save_payroll_record(from_date, to_date, name, hours, rate, tax_rate)
            print("Record saved.\n")
        elif option == "B":
            display_payroll_records()
        elif option == "C":
            print("Returning to main menu.\n")
            break
        else:
            print("Invalid option.\n")

def user_menu():
    display_payroll_records()
    print("Returning to main menu.\n")

def main():
    while True:
        print("=== MAIN MENU ===")
        print("1. Setup Users")
        print("2. Login")
        print("3. End Program")
        choice = input("Choose an option: ")

        if choice == "1":
            setup_users()
        elif choice == "2":
            user = login_user()
            if user:
                print(f"User ID: {user.user_id} | Role: {user.role}\n")
                if user.role == "Admin":
                    admin_menu()
                elif user.role == "User":
                    user_menu()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid selection.\n")

if __name__ == "__main__":
    main()

