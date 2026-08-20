from app.expense import Expense
from datetime import datetime
from app.logger import logger
from app.utils import (
    get_valid_amount,
    get_valid_category,
    get_valid_description,
    get_valid_date,
    get_next_id,
    get_valid_month,
    get_monthly_total,
    get_monthly_expenses,
    get_category_totals
)


def display_expense(expense):
    print(
        f"id          :{expense.id}\n"
        f"amount      :{expense.amount}\n"
        f"category    :{expense.category}\n"
        f"description :{expense.description}\n"
        f"date        :{expense.date}"
    )


def edit_expense(expenses):
    try:
        expense_id = int(input("Enter expense ID to edit: "))

    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    found = False

    for expense in expenses:
        if expense.id == expense_id:
            display_expense(expense)

            found = True

            print("\nWhat do you want to edit?")
            print("1. Amount")
            print("2. Category")
            print("3. Description")
            print("4. Date")
            print("5. Cancel")

            edit_choice = input("Enter your choice: ")

            if edit_choice == "1":
                expense.amount = get_valid_amount()

            elif edit_choice == "2":
                expense.category = get_valid_category()

            elif edit_choice == "3":
                expense.description = get_valid_description()

            elif edit_choice == "4":
                expense.date = get_valid_date()

            elif edit_choice == "5":
                break

            else:
                print("Invalid Choice. Please try again.")

            break

    if not found:
        print("No expense found with that ID.")

    if found and edit_choice in ["1", "2", "3", "4"]:
        print("\nExpense edited successfully.\n")
        logger.info(f"Expense edited: ID {expense.id}")


def show_menu(expenses, budgets):

    while True:
        print("\n================================")
        print("        EXPENSE TRACKER")
        print("================================")
        print("1.  Add Expense")
        print("2.  View Expenses")
        print("3.  Edit Expense")
        print("4.  Delete Expense")
        print("5.  Search Expenses")
        print("6.  Monthly Total")
        print("7.  Set Budget")
        print("8.  Recently Added Expenses")
        print("9.  Statistics")
        print("10. Exit")
        print()

        choice = input("Enter your choice: ")

        print()

        if choice == "1":
            print("\n--- Add New Expense ---")

            amount = get_valid_amount()

            category = get_valid_category()

            description = get_valid_description()

            date = get_valid_date()

            expense = Expense(get_next_id(expenses), amount,
                              category, description, date)
            expenses.append(expense)
            print("\nExpense added successfully.\n")
            logger.info(f"Expense added: ID {expense.id}")

        elif choice == "2":
            
            if not expenses:
                print("No expenses")
            else:
                for expense in expenses:
                    display_expense(expense)
                    print()

        elif choice == "3":
            edit_expense(expenses)

        elif choice == "4":
            while True:
                try:
                    expense_id = int(input("Enter expense ID to delete: "))
                    break
                except ValueError:
                    print("Invalid ID. Please enter a number.")

            found = False

            for expense in expenses:
                if expense.id == expense_id:
                    expenses.remove(expense)
                    print("\nExpense deleted successfully.\n")
                    logger.info(f"Expense deleted: ID {expense.id}")
                    found = True
                    break

            if not found:
                print("No expense found with that ID.")

        elif choice == "5":
            while True:
                print(
                    f"1. Search by Category\n"
                    f"2. Search by Date\n"
                    f"3. Search by Amount\n"
                    f"4. Back\n"
                )

                search_choice = input("Enter your choice: ")
                print()

                if search_choice == "1":
                    category = get_valid_category()
                    print()
                    found = False

                    for expense in expenses:
                        if expense.category.lower() == category.lower():
                            display_expense(expense)
                            print()
                            found = True

                    if not found:
                        print("No expenses found.")

                elif search_choice == "2":
                    date = get_valid_date()
                    print()
                    found = False

                    for expense in expenses:
                        if expense.date == date:
                            display_expense(expense)
                            print()
                            found = True

                    if not found:
                        print("No expenses found.")

                elif search_choice == "3":
                    amount = get_valid_amount()
                    print()
                    found = False

                    for expense in expenses:
                        if expense.amount == amount:
                            display_expense(expense)
                            print()
                            found = True

                    if not found:
                        print("No expenses found.")

                elif search_choice == "4":
                    break

                else:
                    print("Invalid Choice. Please try again.")

        elif choice == "6":
            month_date = get_valid_month()
            total = get_monthly_total(expenses, month_date)

            print(f"\nMonthly total: {total}\n")

        elif choice == "7":
            while True:
                print(
                    f"1. Set Monthly Budget\n"
                    f"2. View Monthly Budget\n"
                    f"3. Budget Status\n"
                    f"4. Back\n"
                )
                budget_choice = input("Enter your choice: ")
                print()

                if budget_choice == "1":
                    month_date = get_valid_month()
                    month = month_date.strftime("%m-%y")

                    amount = get_valid_amount()

                    budgets[month] = amount

                    print("\nMonthly budget set successfully.\n")
                    logger.info(f"Monthly budget set: {month} - {amount}")

                elif budget_choice == "2":
                    month_date = get_valid_month()
                    month = month_date.strftime("%m-%y")

                    if month in budgets:
                        print(f"Monthly budget: {budgets[month]:.2f}")
                    else:
                        print("No budget set for this month.")

                elif budget_choice == "3":
                    month_date = get_valid_month()
                    month = month_date.strftime("%m-%y")

                    if month not in budgets:
                        print("No budget set for this month.")
                        continue

                    total = get_monthly_total(expenses, month_date)

                    budget = budgets[month]
                    remaining = budget - total
                    percentage = (total / budget) * 100

                    print(f"Budget: {budget}")
                    print(f"Spent: {total}")
                    print(f"Remaining: {remaining}")

                    if percentage >= 100:
                        print("Budget exceeded!")
                    elif percentage >= 80:
                        print(
                            f"Warning: You have used {percentage:.1f}% of your budget.")

                elif budget_choice == "4":
                    break

                else:
                    print("Invalid Choice. Please try again.")

        elif choice == "8":
            if not expenses:
                print("No expenses found.")
            else:
                print("Recently Added Expenses:\n")

                for expense in reversed(expenses[-5:]):
                    display_expense(expense)
                    print()

        elif choice == "9":
            month_date = get_valid_month()
            monthly_expenses = get_monthly_expenses(expenses, month_date)

            if not monthly_expenses:
                print("No expenses found for this month.")
                continue

            total = sum(expense.amount for expense in monthly_expenses)
            average = total / len(monthly_expenses)
            highest = max(monthly_expenses, key=lambda expense: expense.amount)

            category_totals = get_category_totals(monthly_expenses)

            top_category = max(
                category_totals,
                key=category_totals.get
            )

            print(f"Total expenses       : {total}")
            print(f"Average expense      : {average:.2f}")
            print(f"Highest expense      : {highest.amount}")
            print(f"Number of expenses   : {len(monthly_expenses)}")

            print("\nCategory Spending")
            print("-----------------")

            for category, amount in category_totals.items():
                print(f"{category:<22}: {amount}")

            print(f"\nTop spending category : {top_category}")
            print(f"Category spending     : {category_totals[top_category]}")

        elif choice == "10":
            print("Thank you for using Expense Tracker.")
            break

        else:
            print("Invalid Choice. Please try again.")
