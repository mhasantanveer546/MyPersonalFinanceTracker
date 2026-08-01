from models.transaction import Transaction


def detect_unusual_spending(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id, type="expense").all()

    category_totals = {}
    category_counts = {}

    for t in transactions:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount
        category_counts[t.category] = category_counts.get(t.category, 0) + 1

    category_averages = {
        category: category_totals[category] / category_counts[category]
        for category in category_totals
    }

    unusual = []
    for t in transactions:
        average = category_averages[t.category]
        if t.amount > average * 2:
            unusual.append({
                "transaction_id": t.id,
                "category": t.category,
                "amount": t.amount,
                "average": round(average, 2),
                "message": f"Unusual spending detected: {t.category} transaction of {t.amount:.2f} is much higher than your average of {average:.2f}."
            })

    return unusual
    