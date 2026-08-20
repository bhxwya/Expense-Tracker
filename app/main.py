from app.menu import show_menu
from app.storage import (
    load_expenses,
    save_expenses,
    load_budget,
    save_budget,
    backup_expenses
)


def main():

    expenses = load_expenses()
    budgets = load_budget()

    backup_expenses()

    show_menu(expenses, budgets)
    save_expenses(expenses)
    save_budget(budgets)


if __name__ == "__main__":
    main()
