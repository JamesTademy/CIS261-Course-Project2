# James Tademy II - CIS261 - Course Project Phase 3
import os
from datetime import datetime

EMPLOYEE_FILE = "employee_data.txt"
USER_FILE = "user_login.txt"

class Login:
    def __init__(self, user_id, password, auth_code):
        self.user_id = user_id
        self.password = password
        self.auth_code = auth_code

# --- USER ACCOUNT MANAGEMENT FUNCTIONS ---

def load_users():
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, password, auth_code = line.strip().split("|")
                users.append(Login(user_id, password, auth_code))
    return users

def add_users():
    existing_users = load_users()
    user_ids = [u.user_id for u in existing_users]

    print("\n=== Add New Users ===")
    while True:
        user_id = input("Enter new User ID (or 'End' to finish): ")
        if user_id.lower() == "end":
            break
        if user_id in user_ids:
            print("User ID already exists.")
            continue
        password = input("Enter password: ")
        auth_code = input("Enter authorization code (Admin/User): ").capitalize()
        if auth_code not in ["Admin", "User"]:
            print("Invalid authorization code.")
            continue
        with open(USER_FILE, "a") as file:
            file.write(f"{user_id}|{password}|{auth_code}\n")
        user_ids.append(user_id)
        print("User added.\n")

def display_users():
    print("\n=== Current Users ===")
    if not os.path.exists(USER_FILE):
        print("No user data found.")
        return
    with open(USER_FILE, "r") as file:
        for line in file:
            user_id, password, auth_code = line.strip().split("|")
            print(f"User ID: {user_id} | Password: {password} | Role: {auth_code}")
    print("=====================\n")

def login():
    users = load_users()
    user_map = {u.user_id: u for u in users}

    user_id = input("Enter your User ID: ")
    if user_id not in user_map:
        print("User ID not found.")
        return None

    password = input("Enter your password: ")
    user = user_map[user_id]

    if user.password != password:
        print("Incorrect password.")
        return None

    print(f"\nWelcome, {user.user_id} ({user.auth_code})\n")
    return user

# --- PAYROLL ENTRY FUNCTIONS ---

def get_date_range():
    from_date = input("Enter FROM date (mm/dd/yyyy): ")
    to_date = input("Enter TO date (mm/dd/yyyy): ")
    return from_date, to_date

def get_employee_name():
    return input("Enter employee's name (or type 'End' to finish): ")

def get_total_hours():
    return float(input("Enter total hours worked: "))

def get_hourly_rate():
    return float(input("Enter hourly rate: "))

def get_tax_rate():
    return float(input("Enter income tax rate (e.g., 0.20 for 20%): "))

def calculate_pay(total_hours, hourly_rate, tax_rate):
    gross_pay = total_hours * hourly_rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay

def write_employee_record(record):
    with open(EMPLOYEE_FILE, "a") as file:
        file.write(record + "\n")

def display_totals(totals):
    print("\n======= Payroll Summary =======")
    print(f"Total Employees: {totals['employees']}")
    print(f"Total Hours: {totals['hours']:.2f}")
    print(f"Total Gross Pay: ${totals['gross_pay']:.2f}")
    print(f"Total Income Tax: ${totals['income_tax']:.2f}")
    print(f"Total Net Pay: ${totals['net_pay']:.2f}")
    print("===============================\n")

def read_and_display_records(user_obj):
    if not os.path.exists(EMPLOYEE_FILE):
        print("No payroll data file found.")
        return

    print(f"\nLogged in as: {user_obj.user_id} | Role: {user_obj.auth_code}")
    user_date = input("Enter FROM date to filter by (mm/dd/yyyy) or 'All': ")

    if user_date.lower() != "all":
        try:
            datetime.strptime(user_date, "%m/%d/%Y")
        except ValueError:
            print("Invalid date format.")
            return

    totals = {
        "employees": 0,
        "hours": 0,
        "gross_pay": 0,
        "income_tax": 0,
        "net_pay": 0
    }

    with open(EMPLOYEE_FILE, "r") as file:
        for line in file:
            from_date, to_date, name, hours, rate, tax_rate = line.strip().split("|")
            if user_date.lower() == "all" or from_date == user_date:
                hours = float(hours)
                rate = float(rate)
                tax_rate = float(tax_rate)
                gross, tax, net = calculate_pay(hours, rate, tax_rate)

                print(f"\nFrom Date: {from_date}")
                print(f"To Date: {to_date}")
                print(f"Employee Name: {name}")
                print(f"Total Hours: {hours:.2f}")
                print(f"Hourly Rate: ${rate:.2f}")
                print(f"Gross Pay: ${gross:.2f}")
                print(f"Income Tax Rate: {tax_rate:.2%}")
                print(f"Income Tax: ${tax:.2f}")
                print(f"Net Pay: ${net:.2f}")

                totals["employees"] += 1
                totals["hours"] += hours
                totals["gross_pay"] += gross
                totals["income_tax"] += tax
                totals["net_pay"] += net

    display_totals(totals)

# --- MAIN PROGRAM ---

def main():
    print("=== CIS261 Payroll System ===")
    mode = input("Do you want to (L)ogin or (A)dd Users? ").lower()

    if mode == "a":
        add_users()
        display_users()
        return

    user = login()
    if not user:
        return

    if user.auth_code.lower() == "admin":
        print("=== Employee Payroll Entry ===")
        while True:
            name = get_employee_name()
            if name.lower() == "end":
                break
            from_date, to_date = get_date_range()
            hours = get_total_hours()
            rate = get_hourly_rate()
            tax_rate = get_tax_rate()

            record = f"{from_date}|{to_date}|{name}|{hours}|{rate}|{tax_rate}"
            write_employee_record(record)
            print("Record saved.\n")

    print("\n=== Payroll Report ===")
    read_and_display_records(user)

if __name__ == "__main__":
    main()
