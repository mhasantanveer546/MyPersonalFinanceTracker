from services.analytics_service import get_expense_by_category_for_month,get_previous_month

def get_spending_analysis(user_id, current_month):
    previous_month = get_previous_month(current_month)

    current_data = get_expense_by_category_for_month(user_id, current_month)
    previous_data = get_expense_by_category_for_month(user_id, previous_month)

    insights = []

    for category, current_amount in current_data.items():
        previous_amount = previous_data.get(category, 0)

        # New category this month
        if previous_amount == 0:
            insights.append(
                f"You started spending on {category} this month."
            )
            continue

        percent_change = ((current_amount - previous_amount) / previous_amount) * 100

        # Ignore insignificant changes
        if abs(percent_change) < 10:
            continue

        if percent_change > 0:
            insights.append(
                f"Your {category} expenses increased by {percent_change:.1f}% compared to last month."
            )
        else:
            insights.append(
                f"Your {category} expenses decreased by {abs(percent_change):.1f}% compared to last month."
            )

    return insights



def get_smart_suggestion(user_id, current_month):
    current_data = get_expense_by_category_for_month(user_id, current_month)

    if not current_data:
        return None

    top_category = max(current_data, key=current_data.get)
    top_amount = current_data[top_category]

    potential_savings = top_amount * 0.10

    return (
        f"You spend the most on {top_category} ({top_amount:.2f}) this month. "
        f"Reducing it by 10% could save you {potential_savings:.2f}."
    )