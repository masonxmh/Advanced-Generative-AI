# Personal Expense Tracker

This project is a simple command-line expense tracker written in Python. It lets you add expenses, view saved and current expenses, set a monthly budget, and save expense data to a CSV file.

## Files

- `pet.py`: Main Python application.
- `data.csv`: Stores saved expense records.
- `.gitignore`: Ignores generated PDF, PNG, and Jupyter checkpoint files for this project.

## Features

- Add an expense with:
  - date
  - category
  - amount
  - description
- View all loaded and newly added expenses
- Set and track a monthly budget
- Save expenses to `data.csv`
- Load previously saved expenses from `data.csv` when the program starts

## How It Works

When the program starts, it loads existing expense data from `data.csv`.

You then interact with a menu:

1. Add expense
2. View expenses
3. Track budget
4. Save expenses to the file
5. Save expenses and exit the program

New expenses are stored in memory first and can later be appended to the CSV file.

## Validation

The script includes simple validation helpers:

- `valid_date(date)`: Accepts dates in `YYYY-MM-DD` format
- `valid_category(category)`: Ensures category is not empty
- `valid_amount(amount)`: Converts the amount to `float`
- `valid_descrip(description)`: Ensures description is not empty

If a value is invalid or missing, the program may still store the entry, and `view_expenses()` will mark incomplete entries when displaying them.

## Main Functions

- `add_expense()`: Collects expense details from user input
- `view_expenses()`: Displays stored and newly added expenses
- `set_budget()`: Prompts the user for a monthly budget
- `track_budget()`: Compares total expenses against the budget
- `load_csv()`: Loads existing expense records from the CSV file
- `save_csv()`: Appends new expenses to the CSV file
- `menu()`: Prints the interactive menu
- `main()`: Runs the application loop

## Run The Program

From the `Personal Expense Tracker` directory:

```powershell
python pet.py
```

## Notes

- Saved expenses are appended to `data.csv`, so running save multiple times without clearing `expenses` may duplicate rows.
- `track_budget()` asks for the monthly budget each time it runs.
- The script uses global lists (`data` and `expenses`) to combine loaded and new entries during runtime.
