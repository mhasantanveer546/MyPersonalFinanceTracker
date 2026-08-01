from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from services.transaction_service import add_transaction, get_transactions, delete_transaction, edit_transaction, get_transaction_by_id

transaction_bp = Blueprint("transaction", __name__)


@transaction_bp.route("/add-transaction", methods=["GET"])
@login_required
def add_transaction_page():
    return render_template("add_transaction.html")


@transaction_bp.route("/add-transaction", methods=["POST"])
@login_required
def add_transaction_route():
    type = request.form.get("type")
    category = request.form.get("category")
    amount = float(request.form.get("amount"))
    date = request.form.get("date")
    description = request.form.get("description")
    result = add_transaction(current_user.id, type, category, amount, date, description)
    if result["success"]:
        return redirect(url_for("transaction.view_transactions"))
    else:
        return render_template("add_transaction.html", error=result["message"])


@transaction_bp.route("/transactions", methods=["GET"])
@login_required
def view_transactions():
    type_filter = request.args.get("type")
    category_filter = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    transactions = get_transactions(
        current_user.id,
        type=type_filter,
        category=category_filter,
        start_date=start_date,
        end_date=end_date
    )
    return render_template("transactions.html", transactions=transactions)


@transaction_bp.route("/delete-transaction/<int:transaction_id>", methods=["POST"])
@login_required
def delete_transaction_route(transaction_id):
    delete_transaction(transaction_id, current_user.id)
    return redirect(url_for("transaction.view_transactions"))


@transaction_bp.route("/edit-transaction/<int:transaction_id>", methods=["GET"])
@login_required
def edit_transaction_page(transaction_id):
    transaction = get_transaction_by_id(transaction_id, current_user.id)
    if not transaction:
        return redirect(url_for("transaction.view_transactions"))
    return render_template("edit_transaction.html", transaction=transaction)


@transaction_bp.route("/edit-transaction/<int:transaction_id>", methods=["POST"])
@login_required
def edit_transaction_route(transaction_id):
    type = request.form.get("type")
    category = request.form.get("category")
    amount = float(request.form.get("amount"))
    date = request.form.get("date")
    description = request.form.get("description")
    result = edit_transaction(
        transaction_id, current_user.id,
        type=type, category=category, amount=amount, date=date, description=description
    )
    if result["success"]:
        return redirect(url_for("transaction.view_transactions"))
    else:
        return result["message"], 404