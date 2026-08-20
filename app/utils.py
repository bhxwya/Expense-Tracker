from datetime import datetime
import re


def get_next_id(expenses):
    if not expenses:
        return 1

    return max(expense.id for expense in expenses) + 1


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def capitalize_first(value):
    return value[:1].upper() + value[1:]


def is_valid_text(value):
    pattern = r"[A-Za-z0-9 ]+"
    return bool(re.fullmatch(pattern, value))


def get_valid_category():
    while True:
        category = input("Enter category: ").strip()

        if not category.strip():
            print("Category cannot be empty.")
            continue

        if not is_valid_text(category):
            print("Category can only contain letters, numbers, and spaces.")
            continue

        return capitalize_first(category)


def get_valid_description():
    while True:
        description = input("Enter description: ").strip()

        if not description.strip():
            print("Description cannot be empty.")
            continue

        return capitalize_first(description)


def get_valid_date():
    while True:
        date = input("Enter date (DD-MM-YY): ")

        try:
            datetime.strptime(date, "%d-%m-%y")
            return date

        except ValueError:
            print("Invalid date. Please use DD-MM-YY.")


def get_valid_month():
    while True:
        month_date = input("Enter month and year (MM-YY): ")

        try:
            return datetime.strptime(month_date, "%m-%y")

        except ValueError:
            print("Invalid date. Please use MM-YY.")


def get_monthly_expenses(expenses, month_date):
    monthly_expenses = []

    for expense in expenses:
        expense_date = datetime.strptime(expense.date, "%d-%m-%y")

        if expense_date.month == month_date.month and expense_date.year == month_date.year:
            monthly_expenses.append(expense)

    return monthly_expenses


def get_monthly_total(expenses, month_date):
    monthly_expenses = get_monthly_expenses(expenses, month_date)

    return sum(expense.amount for expense in monthly_expenses)


def get_category_totals(expenses):
    category_totals = {}

    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = 0

        category_totals[expense.category] += expense.amount

    return category_totals
