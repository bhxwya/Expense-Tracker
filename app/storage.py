import json
from app.expense import Expense
from app.logger import logger
import shutil


def save_expenses(expenses):

    # Open a file for writing
    with open("data/expenses.json", "w") as file:
        data = []
        for expense in expenses:
            expense_data = {
                "id": expense.id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.date
            }

            data.append(expense_data)

        json.dump(data, file)
        logger.info("Expenses saved successfully")


def load_expenses():
    expenses = []
    try:
        with open("data/expenses.json", "r") as file:
            data = json.load(file)
            for expense_data in data:
                expense = Expense(
                    expense_data["id"],
                    expense_data["amount"],
                    expense_data["category"],
                    expense_data["description"],
                    expense_data["date"]
                )
                expenses.append(expense)

            logger.info("Expenses loaded successfully")
    except FileNotFoundError:
        logger.error("Expenses file not found.")
        expenses = []
    except json.JSONDecodeError:
        logger.error("Expenses file contains invalid JSON.")
        expenses = []

    return expenses


def save_budget(budgets):
    with open("data/budget.json", "w") as file:
        json.dump(budgets, file)

    logger.info("Budgets saved successfully")


def load_budget():
    try:
        with open("data/budget.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        logger.error("Budget file not found.")
        return {}

    except json.JSONDecodeError:
        logger.error("Budget file contains invalid JSON.")
        return {}


def backup_expenses():
    try:
        shutil.copy("data/expenses.json", "data/expenses_backup.json")
        logger.info("Expenses backup created successfully")

    except FileNotFoundError:
        logger.warning("No expenses file available to backup.")
