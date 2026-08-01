from models.transaction import Transaction
from services.budget_service import get_budgets, get_budget_status
from sqlalchemy import extract
from datetime import date

def get_previous_month(month):
    year, month_num = map(int, month.split("-"))
    if month_num == 1:
        return f"{year - 1}-12"
    return f"{year}-{month_num - 1:02d}"

def get_summary(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')

    balance = total_income - total_expense

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    }

    
def get_expense_by_category(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id, type='expense').all()
    category_summary = {}

    for t in transactions:
        if t.category not in category_summary:
            category_summary[t.category] = 0
        category_summary[t.category] += t.amount

    return category_summary


def get_income_vs_expense_by_month(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    monthly_summary = {}
    for t in transactions:
        key = t.date.strftime("%Y-%m")
        if key not in monthly_summary:
            monthly_summary[key] = {
                "income": 0,
                "expense": 0
            }
        monthly_summary[key][t.type] += t.amount
    return monthly_summary

def get_budget_progress(user_id, month):
    budgets = get_budgets(user_id, month=month)
    progress = []

    for budget in budgets:
        status = get_budget_status(user_id, month, budget.category)
        if status["success"]:
            progress.append(status["budget"])

    return progress

def get_expense_by_category_for_month(user_id, month):
    year, month_num = month.split("-")

    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense",
        extract("year", Transaction.date) == int(year),
        extract("month", Transaction.date) == int(month_num)
    ).all()

    category_totals = {}
    for t in transactions:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

    return category_totals