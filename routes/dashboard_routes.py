from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
from services.analytics_service import (
    get_summary,
    get_expense_by_category,
    get_income_vs_expense_by_month,
    get_budget_progress
)
from ai.recommendation import get_spending_analysis, get_smart_suggestion
from ai.anomaly_detection import detect_unusual_spending
from ai.predictor import predict_next_month_expense

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    summary = get_summary(current_user.id)
    expense_by_category = get_expense_by_category(current_user.id)
    income_vs_expense = get_income_vs_expense_by_month(current_user.id)

    current_month = datetime.utcnow().strftime("%Y-%m")
    budget_progress = get_budget_progress(current_user.id, current_month)

    spending_insights = get_spending_analysis(current_user.id, current_month)
    smart_suggestion = get_smart_suggestion(current_user.id, current_month)
    unusual_spending = detect_unusual_spending(current_user.id)
    predicted_expense = predict_next_month_expense(current_user.id)

    return render_template(
        "dashboard.html",
        summary=summary,
        expense_by_category=expense_by_category,
        income_vs_expense=income_vs_expense,
        budget_progress=budget_progress,
        spending_insights=spending_insights,
        smart_suggestion=smart_suggestion,
        unusual_spending=unusual_spending,
        predicted_expense=predicted_expense
    )