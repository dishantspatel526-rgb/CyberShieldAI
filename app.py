import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_file

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# ==========================
# Database Initialization
# ==========================

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        status TEXT,
        score INTEGER,
        scan_time TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# URL Scanner Page
# ==========================

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")


# ==========================
# Password Checker Page
# ==========================

@app.route("/password")
def password():
    return render_template("password.html")


# ==========================
# Email Checker Page
# ==========================

@app.route("/email")
def email():
    return render_template("email.html")


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE status='SAFE'")
    safe = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE status='SUSPICIOUS'")
    suspicious = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE status='DANGEROUS'")
    dangerous = cursor.fetchone()[0]

    cursor.execute("""
    SELECT url, status, score, scan_time
    FROM scans
    ORDER BY id DESC
    LIMIT 10
    """)

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        safe=safe,
        suspicious=suspicious,
        dangerous=dangerous,
        history=history
    )
# ==========================
# URL Scanner API
# ==========================

@app.route("/scan_url", methods=["POST"])
def scan_url():

    data = request.get_json()
    url = data.get("url", "").lower().strip()

    score = 100
    reasons = []

    if not url:
        return jsonify({
            "status": "ERROR",
            "score": 0,
            "reasons": ["Please enter a URL."]
        })

    if "http://" in url:
        score -= 25
        reasons.append("Website is not using HTTPS.")

    if "@" in url:
        score -= 20
        reasons.append("Suspicious @ symbol found.")

    if ".xyz" in url:
        score -= 20
        reasons.append("Unknown domain extension.")

    if "login" in url:
        score -= 15
        reasons.append("Login keyword detected.")

    if "verify" in url:
        score -= 15
        reasons.append("Verification keyword detected.")

    if len(url) > 45:
        score -= 10
        reasons.append("Very long URL.")

    if score >= 80:
        status = "SAFE"
    elif score >= 50:
        status = "SUSPICIOUS"
    else:
        status = "DANGEROUS"

    # Save Scan in Database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans(url, status, score, scan_time)
        VALUES (?, ?, ?, ?)
    """, (
        url,
        status,
        score,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": status,
        "score": score,
        "reasons": reasons
    })

@app.route("/download_report")
def download_report():

    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate("CyberShieldAI_Report.pdf")

    elements = []

    elements.append(Paragraph("Cyber Shield AI Report", styles["Title"]))
    elements.append(Paragraph("Developer : Dishant Patel", styles["Normal"]))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT url, status, score, scan_time
    FROM scans
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    for row in rows:
        elements.append(
            Paragraph(
                f"{row[3]} | {row[0]} | {row[1]} | Score: {row[2]}",
                styles["BodyText"]
            )
        )

    pdf.build(elements)

    return send_file("CyberShieldAI_Report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    