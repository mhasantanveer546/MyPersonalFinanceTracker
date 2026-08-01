import numpy as np
from sklearn.linear_model import LinearRegression
from services.analytics_service import get_income_vs_expense_by_month


def predict_next_month_expense(user_id):
    monthly_data = get_income_vs_expense_by_month(user_id)

    months = sorted(monthly_data.keys())

    if len(months) < 3:
        return None

    X = np.array(range(len(months))).reshape(-1, 1)
    y = np.array([monthly_data[m]["expense"] for m in months])

    model = LinearRegression()
    model.fit(X, y)

    next_index = np.array([[len(months)]])
    prediction = model.predict(next_index)[0]

    return round(max(prediction, 0), 2)