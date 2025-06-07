import os
from datetime import datetime

EMPLOYEE_FILE = "employee_data.txt"
USER_FILE = "users.txt"

# ===== Login Class =====
class Login:
    def __init__(self, user_id, password, role):
        self.user_id = user_id
        self.password = password
        self.role = role

# ===== File Handling Functions =====
def load_users():
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, password, role = line.strip().split("|")
                users.append(Login(user_id, password, role))
    return users

def save_user(user_id, password, role):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id}|{password}|{role}\n")

# ===== User Management =====
def user_setup():
    users = load_users()
    existing_ids = [u.user_id for u in users]

    while True:
        user_id = input("Enter new User ID (or 'End' to finish): ")
        if user_id.lower() == "end":
            break
        if user_id in existing_ids:
            print("User ID already exists.")
            continue
        password = input("Enter Password: ")
        role = input("Enter Role (Admin/User): ").capitalize()
        if role not in ["Admin", "User"]:
            print("Role must be 'Admin' or 'User'.")
            continue
        save_user(user_id, password, role)
        existing_ids.append(user_id)
        print("User saved.\n")

def login():
    users = load_users()
    user_id = input("Login User ID: ")
    password = input("Login Password: ")
    for u in users:
        if u.user_id == user_id:
            if u.password == password:
                print(f"Welcome {user_id} ({u.role})!\n")
                return u
            else:
                print("Incorrect password.")
                exit()
    print("User not found.")
    exit()

# ===== Payroll Entry & Display =====
def get_employee_input():
    from_date = input("Enter FROM date (mm/dd/yyyy): ")
    to_date = input("Enter TO date (mm/dd/yyyy): ")
    name = input("Enter employee name: ")
    hours = float(input("Enter total hours worked: "))
    rate = float(input("Enter hourly rate: "))
    tax = float(input("Enter tax rate (e.g. 0.20): "))
    return from_date, to_date, name, hours, rate, tax

def calculate_pay(hours, rate, tax):
    gross = hours * rate
    income_tax = gross * tax
    net = gross - income_tax
    return gross, income_tax, net

def write_employee_record(from_date, to_date, name, hours, rate, tax):
    with open(EMPLOYEE_FILE, "a") as file:
        file.write(f"{from_date}|{to_date}|{name}|{hours}|{rate}|{tax}\n")

def display_records():
    if not os.path.exists(EMPLOYEE_FILE):
        print("No payroll data found.")
        return

    filter_date = input("Enter FROM date to filter by (mm/dd/yyyy) or 'All': ")

    totals = {"employees": 0, "hours": 0, "gross": 0, "tax": 0, "net": 0}
    with open(EMPLOYEE_FILE, "r") as file:
        for line in file:
            from_date, to_date, name, hours, rate, tax = line.strip().split("|")
            if filter_date.lower() != "all" and from_date != filter_date:
                continue

            hours = float(hours)
            rate = float(rate)
            tax = float(tax)
            gross, income_tax, net = calculate_pay(hours, rate, tax)

            print(f"\nFrom: {from_date} To: {to_date}")
            print(f"Name: {name}")
            print(f"Hours: {hours:.2f}  Rate: ${rate:.2f}")
            print(f"Gross: ${gross:.2f}  Tax: ${income_tax:.2f}  Net: ${net:.2f}")

            totals["employees"] += 1
            totals["hours"] += hours
            totals["gross"] += gross
            totals["tax"] += income_tax
            totals["net"] += net

    print("\n===== PAYROLL SUMMARY =====")
    print(f"Employees: {totals['employees']}")
    print(f"Total Hours: {totals['hours']:.2f}")
    print(f"Total Gross Pay: ${totals['gross']:.2f}")
    print(f"Total Tax: ${totals['tax']:.2f}")
    print(f"Total Net Pay: ${totals['net']:.2f}")
    print("===========================\n")

# ===== Main Program =====
def main():
    print("1. Setup Users")
    print("2. Login and Use Payroll System")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        user_setup()
    elif choice == "2":
        user = login()
        if user.role == "Admin":
            while True:
                print("A) Add Payroll Entry")
                print("B) View Payroll Records")
                print("C) Logout")
                action = input("Select option: ").upper()
                if action == "A":
                    from_date, to_date, name, hours, rate, tax = get_employee_input()
                    write_employee_record(from_date, to_date, name, hours, rate, tax)
                    print("Payroll record saved.\n")
                elif action == "B":
                    display_records()
                elif action == "C":
                    break
        elif user.role == "User":
            display_records()
        else:
            print("Invalid role.")
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
