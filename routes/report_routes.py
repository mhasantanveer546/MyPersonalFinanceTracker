from flask import Blueprint, Response
from flask_login import login_required, current_user
from analytics.reports import generate_csv_report, generate_pdf_report

report_bp = Blueprint("report", __name__)


@report_bp.route("/reports/csv")
@login_required
def export_csv():
    csv_data = generate_csv_report(current_user.id)

    return Response(
        csv_data.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"}
    )


@report_bp.route("/reports/pdf")
@login_required
def export_pdf():
    pdf_data = generate_pdf_report(current_user.id)

    return Response(
        pdf_data.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=transactions.pdf"}
    )