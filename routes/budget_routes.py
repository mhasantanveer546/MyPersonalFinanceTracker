from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from services.budget_service import add_budget, get_budgets, get_budget_status, delete_budget

budget_bp = Blueprint("budget", __name__)

@budget_bp.route("/add-budget", methods=["GET"])
@login_required
def add_budget_page():
    return render_template("add_budget.html")

@budget_bp.route("/add-budget", methods=["POST"])
@login_required
def add_budget_route():
    category=request.form.get("category")
    limit_amount=float(request.form.get("limit_amount"))
    month=request.form.get("month")

    result = add_budget(current_user.id, category, limit_amount, month)

    if result["success"]:
        return redirect(url_for("budget.view_budgets"))
    else:
        return render_template("add_budget.html", error=result["message"])


@budget_bp.route("/budgets", methods=["GET"])
@login_required
def view_budgets():
    budgets=get_budgets(current_user.id)
    return render_template("budgets.html" , budgets=budgets)

@budget_bp.route("/delete-budget/<int:budget_id>", methods=["POST"])
@login_required
def delete_budget_route(budget_id):
    delete_budget(budget_id,current_user.id)
    return redirect(url_for("budget.view_budgets"))

