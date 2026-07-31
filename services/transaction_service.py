from models import db
from models.transaction import Transaction

def add_transaction(user_id, type, category, amount, date, description=None):
    if type not in ['income', 'expense']:
        return {"success": False, "message": "Invalid transaction type. Must be 'income' or 'expense'."}

    if amount <= 0:
        return {"success": False, "message": "Amount must be greater than zero."}

    transaction = Transaction(user_id=user_id, type=type, category=category, amount=amount, date=date, description=description)
    db.session.add(transaction)
    db.session.commit()
    return {"success": True, "message": "Transaction added successfully.", "transaction": transaction}

def get_transactions(user_id, type=None, category=None, start_date=None, end_date=None):
    query = Transaction.query.filter_by(user_id=user_id)

    if type:
        query = query.filter_by(type=type)

    if category:
        query = query.filter_by(category=category)

    if start_date:
        query = query.filter(Transaction.date >= start_date)

    if end_date:
        query = query.filter(Transaction.date <= end_date)

    transactions = query.all()
    return transactions

def get_transaction_by_id(transaction_id, user_id):
    return Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()

def delete_transaction(transaction_id, user_id):
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return {"success": False, "message": "Transaction not found."}

    db.session.delete(transaction)
    db.session.commit()
    return {"success": True, "message": "Transaction deleted successfully."}



def edit_transaction(transaction_id, user_id, **kwargs):
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()

    if not transaction:
        return {"success": False, "message": "Transaction not found."}

    kwargs = {k: v for k, v in kwargs.items() if k not in ("id", "user_id")}

    for key, value in kwargs.items():
        if hasattr(transaction, key):
            setattr(transaction, key, value)

    db.session.commit()
    return {"success": True, "message": "Transaction updated successfully.", "transaction": transaction}
