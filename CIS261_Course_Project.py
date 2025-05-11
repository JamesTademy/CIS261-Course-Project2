#James Tademy
#CIS 261 Course Project
#CIS261

def get_employee_name():
    return input("Enter employee name (or type 'End' to finish): ")

def get_total_hours():
    return float(input("Enter total hours worked: "))

def get_hourly_rate():
    return float(input("Enter hourly rate: "))

def get_tax_rate():
    return float(input("Enter income tax rate (as a decimal, e.g., 0.2 for 20%): "))

def calculate_pay(hours, rate, tax_rate):
    gross_pay = hours * rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay

def display_employee_info(name, hours, rate, gross, tax_rate, tax, net):
    print("\n--- Employee Pay Info ---")
    print(f"Name: {name}")
    print(f"Total Hours: {hours}")
    print(f"Hourly Rate: ${rate:.2f}")
    print(f"Gross Pay: ${gross:.2f}")
    print(f"Tax Rate: {tax_rate*100:.1f}%")
    print(f"Income Tax: ${tax:.2f}")
    print(f"Net Pay: ${net:.2f}\n")

def display_totals(emp_count, total_hours, total_gross, total_tax, total_net):
    print("\n=== Payroll Summary ===")
    print(f"Total Employees: {emp_count}")
    print(f"Total Hours Worked: {total_hours}")
    print(f"Total Gross Pay: ${total_gross:.2f}")
    print(f"Total Income Tax: ${total_tax:.2_}")
def main():
    employee_count = 0
    total_hours = total_gross = total_tax = total_net = 0

    while True:
        name = get_employee_name()
        if name.strip().lower() == "end":
            break

        hours = get_total_hours()
        rate = get_hourly_rate()
        tax_rate = get_tax_rate()

        gross, tax, net = calculate_pay(hours, rate, tax_rate)
        display_employee_info(name, hours, rate, gross, tax_rate, tax, net)

        # Accumulate totals
        employee_count += 1
        total_hours += hours
        total_gross += gross
        total_tax += tax
        total_net += net

    display_totals(employee_count, total_hours, total_gross, total_tax, total_net)

if __name__ == "__main__":
    main()

