import csv
import io
from models.transaction import Transaction
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from sqlalchemy import extract

def generate_csv_report(user_id, month=None):
    query = Transaction.query.filter_by(user_id=user_id)
    if month:
        year, month_num = month.split("-")
        query = query.filter(
            extract("year", Transaction.date) == int(year),
            extract("month", Transaction.date) == int(month_num)
        )
    transactions = query.order_by(Transaction.date).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
    for t in transactions:
        writer.writerow([t.date, t.type, t.category, t.amount, t.description])

    output.seek(0)
    return output

def generate_pdf_report(user_id, month=None):
    query = Transaction.query.filter_by(user_id=user_id)
    if month:
        year, month_num = month.split("-")
        query = query.filter(
            extract("year", Transaction.date) == int(year),
            extract("month", Transaction.date) == int(month_num)
        )
    transactions = query.order_by(Transaction.date).all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = f"Transaction Report — {month}" if month else "Transaction Report (All Time)"
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    data = [["Date", "Type", "Category", "Amount", "Description"]]
    for t in transactions:
        data.append([str(t.date), t.type, t.category, f"{t.amount:.2f}", t.description or ""])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5fa")]),
    ]))

    story.append(table)
    doc.build(story)

    buffer.seek(0)
    return buffer