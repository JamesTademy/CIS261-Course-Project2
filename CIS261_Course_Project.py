## Name: James TAdemy
# Course: CIS261
# Lab Title: Course project 3

import os
from datetime import datetime

FILENAME = "employee_data.txt"

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

def display_totals(totals):
    print("\n======= Payroll Summary =======")
    print(f"Total Employees: {totals['employees']}")
    print(f"Total Hours: {totals['hours']:.2f}")
    print(f"Total Gross Pay: ${totals['gross_pay']:.2f}")
    print(f"Total Income Tax: ${totals['income_tax']:.2f}")
    print(f"Total Net Pay: ${totals['net_pay']:.2f}")
    print("===============================\n")

def write_to_file(record):
    with open(FILENAME, "a") as file:
        file.write(record + "\n")

def read_and_display_records():
    if not os.path.exists(FILENAME):
        print("No data file found.")
        return

    user_date = input("Enter FROM date to filter by (mm/dd/yyyy) or 'All' to show all: ")

    if user_date.lower() != "all":
        try:
            datetime.strptime(user_date, "%m/%d/%Y")
        except ValueError:
            print("Invalid date format. Please use mm/dd/yyyy.")
            return

    totals = {
        "employees": 0,
        "hours": 0,
        "gross_pay": 0,
        "income_tax": 0,
        "net_pay": 0
    }

    with open(FILENAME, "r") as file:
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

def main():
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
        write_to_file(record)
        print("Employee data saved.\n")

    print("\n=== Payroll Report ===")
    read_and_display_records()

if __name__ == "__main__":
    main()
