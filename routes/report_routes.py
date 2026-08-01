from flask import Blueprint, Response, render_template, request
from flask_login import login_required, current_user
from services.analytics_service import get_summary, get_expense_by_category
from services.analytics_service import get_summary, get_expense_by_category, get_expense_by_category_for_month
from analytics.reports import generate_csv_report, generate_pdf_report

report_bp = Blueprint("report", __name__)


@report_bp.route("/reports")
@login_required
def reports_page():
    month = request.args.get("month")
    summary = get_summary(current_user.id, month=month)
    expense_by_category = get_expense_by_category_for_month(current_user.id, month) if month else get_expense_by_category(current_user.id)
    return render_template("reports.html", summary=summary, expense_by_category=expense_by_category)

@report_bp.route("/reports/csv")
@login_required
def export_csv():
    month = request.args.get("month")
    csv_data = generate_csv_report(current_user.id, month=month)

    filename = f"transactions_{month}.csv" if month else "transactions.csv"
    return Response(
        csv_data.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@report_bp.route("/reports/pdf")
@login_required
def export_pdf():
    month = request.args.get("month")
    pdf_data = generate_pdf_report(current_user.id, month=month)

    filename = f"transactions_{month}.pdf" if month else "transactions.pdf"
    return Response(
        pdf_data.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )