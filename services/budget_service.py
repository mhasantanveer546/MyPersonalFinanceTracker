from models import db
from models.budget import Budget
from models.transaction import Transaction
from sqlalchemy import extract

def add_budget(user_id, category, limit_amount, month):
    if limit_amount <= 0:
        return {"success": False, "message": "Limit amount must be greater than zero."}
    existing_budget = Budget.query.filter_by(user_id=user_id, category=category, month=month).first()
    if existing_budget:
        return {"success": False, "message": "Budget for this category and month already exists."}
    budget = Budget(user_id=user_id, category=category, limit_amount=limit_amount, month=month)
    db.session.add(budget)
    db.session.commit()
    return {"success": True, "message": "Budget added successfully.", "budget": budget}

def get_budgets(user_id, month=None, category=None):
    query = Budget.query.filter_by(user_id=user_id)
    if month is not None:
        query = query.filter_by(month=month)
    if category is not None:
        query = query.filter_by(category=category)
    budgets = query.all()
    return budgets


def get_budget_status(user_id, month, category):
    budget = Budget.query.filter_by(user_id=user_id, month=month, category=category).first()
    if not budget:
        return {"success": False, "message": "Budget not found for the specified month and category."}

    year, month_num = month.split("-")   # "2026-07" -> "2026", "07"

    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.category == category,
        Transaction.type == "expense",
        extract("year", Transaction.date) == int(year),
        extract("month", Transaction.date) == int(month_num)
    ).all()

    total_spent = sum(t.amount for t in transactions)
    percent_used = (total_spent / budget.limit_amount) * 100

    return {
        "success": True,
        "budget": {
            "category": budget.category,
            "limit_amount": budget.limit_amount,
            "month": budget.month,
            "total_spent": total_spent,
            "remaining_amount": budget.limit_amount - total_spent,
            "percent_used": round(percent_used, 1)
        }
    }

def get_budget_alert(percent_used):
    if percent_used >= 100:
        return "You have exceeded your budget limit."
    elif percent_used >= 80:
        return f"You have used {percent_used}% of your budget."
    else:
        return None


def delete_budget(budget_id, user_id):
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    if not budget:
        return {"success": False, "message": "Budget not found."}

    db.session.delete(budget)
    db.session.commit()
    return {"success": True, "message": "Budget deleted successfully."}