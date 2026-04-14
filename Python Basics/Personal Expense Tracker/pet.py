import os
import csv
from datetime import datetime


file_name = 'data.csv'
data = []
expenses = []
monthly_budget = None

# 1. =====Add an expense:=====
# check date
def valid_date(date):
    format_pattern = "%Y-%m-%d"
    try: 
        datetime.strptime(date, format_pattern)
        return date
    except ValueError:
        return 


# check category
def valid_category(category):
    if category:
        return category
    else:
        return 
    

# check amount
def valid_amount(amount):
    try:
        amt = float(amount)
        return amt
    except ValueError:
        return
    

# check description
def valid_descrip(description):
    if description:
        return description
    else:
        return 


def add_expense():
    print('\n==Add an expense:==\n')
    exp = {}
    # The date of the expense in the format YYYY-MM-DD
    date = input("Enter date (YYYY-MM-DD): ").strip()
    exp['date'] = valid_date(date)
    # The category of the expense, such as Food or Travel
    category = input("Enter category (Such as:Food, Travel): ").strip()
    exp['category'] = valid_category(category)
    # The amount spent
    amount = input("Enter amount spent: ").strip()
    exp['amount'] = valid_amount(amount)
    # A brief description of the expense
    description = input("Enter description: ").strip()
    exp['description'] = valid_descrip(description)
    expenses.append(exp)
    print("\nExpense added!")


# 2. =====View expenses:=====
def check_missing(exp):
    missing_keys = []
    for key, value in exp.items():
        if value in (None, ""):
            missing_keys.append(key)
    return missing_keys


def view_expenses():
    print("\n==View Expenses==\n")
    stored_expenses = []
    stored_expenses = data + expenses
    if not stored_expenses:
        print("No expenses recorded yet.")
        return
    else:
        for index, exp in enumerate(stored_expenses):
            missing = check_missing(exp)

            if missing:
                print(f"Entry {index} is incomplete, missing {missing}")
            else:
                print(f"Entry {index}: "
                      f"Date: {exp['date']}, "
                      f"Category: {exp['category']}, "
                      f"Amount: ${float(exp['amount']):.2f}, "
                      f"Description: {exp['description']}")


# =====3. Set and track the budget:=====
def set_budget():
    print("\n==Set Monthly Budget==\n")
    global monthly_budget
    while True:
        budget_input = input("Enter your monthly budget: ").strip()

        try:
            monthly_budget = float(budget_input)

            if monthly_budget > 0:
                break
            else:
                print("Budget must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    print(f"Monthly budget set to ${monthly_budget:.2f}")

def track_budget():
    
    set_budget()
    stored_expenses = []
    stored_expenses = data + expenses
    total_expenses = 0.0
    for exp in stored_expenses:
        if not check_missing(exp):
            total_expenses += float(exp['amount'])
    print("\n==Track Monthly Budget==\n")
    print(f"Total expenses: ${total_expenses:.2f}")
    print(f"Monthly budget: ${monthly_budget:.2f}")

    if total_expenses > monthly_budget:
        print("You have exceeded your budget!")
    else:
        remaining = monthly_budget - total_expenses
        print(f"You have ${remaining:.2f} left for the month.")





# 4.=====Save and load expenses:=====
# load csv file
headers = ['date', 'category', 'amount', 'description']
def load_csv(filename = file_name):
    rows = []
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
        print("No existing file, File created.")
    else:
        with open("data.csv", mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
    data.clear()
    data.extend(rows)

# save csv file
def save_csv(filename = file_name):
    # headers = ['date', 'category', 'amount', 'description']
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # writer.writeheader()
        writer.writerows(expenses)


# 5. Create an interactive menu:
def menu():
    print("\n<<Personal Expense Tracker>>\n")
    print("1) Add expense")
    print("2) View expenses")
    print("3) Track budget")
    print("4) Save expenses to the file")
    print("5) Save expenses and exit the program")


def main():
    load_csv('data.csv')

    # print(data)
    while True:
        menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            track_budget()
        elif choice == "4":
            save_csv('data.csv')
        elif choice == "5":
            save_csv('data.csv')
            print("Save the expenses and Exit")
            break
        # elif choice == "6":
        #     break
        else:
            print("Invalid. Please enter a number from 1 to 5.")
    
if __name__ == "__main__":
    main()