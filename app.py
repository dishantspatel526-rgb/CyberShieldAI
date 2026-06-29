import os
import sqlite3
import hashlib
import ipaddress
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_file

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# ==========================
# Database Setup
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
# Home
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
# URL Scanner
# ==========================

@app.route("/scan", methods=["POST"])
def scan():

    data = request.get_json()

    url = data.get("url")

    if not url:
        return jsonify({
            "url": "",
            "status": "No URL Entered",
            "score": 0
        })

    status = "Safe ✅"
    score = 95

    suspicious = [
        "login",
        "verify",
        "bank",
        "free",
        "gift",
        "paypal",
        "secure",
        "update"
    ]

    for word in suspicious:
        if word in url.lower():
            status = "Suspicious ⚠️"
            score = 40
            break

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO scans(url,status,score,scan_time)
        VALUES(?,?,?,?)
        """,
        (
            url,
            status,
            score,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "url": url,
        "status": status,
        "score": score
    })


# ==========================
# Password Checker Page
# ==========================

@app.route("/password")
def password():
    return render_template("password.html")


# ==========================
# Password Checker API
# ==========================

@app.route("/check_password", methods=["POST"])
def check_password():

    data = request.get_json()

    password = data.get("password")

    if not password:
        return jsonify({
            "strength": "Weak",
            "score": 0
        })

    score = 0

    if len(password) >= 8:
        score += 25

    if any(c.isupper() for c in password):
        score += 25

    if any(c.isdigit() for c in password):
        score += 25

    if any(c in "!@#$%^&*" for c in password):
        score += 25

    if score >= 75:
        strength = "Strong 💪"
    elif score >= 50:
        strength = "Medium 🙂"
    else:
        strength = "Weak ❌"

    return jsonify({
        "strength": strength,
        "score": score
    })

# ==========================
# Email Checker Page
# ==========================

@app.route("/email")
def email():
    return render_template("email.html")


# ==========================
# Email Checker API
# ==========================

@app.route("/check_email", methods=["POST"])
def check_email():

    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({
            "email": "",
            "status": "Invalid Email"
        })

    status = "Safe Email ✅"

    if "@" not in email or "." not in email:
        status = "Invalid Email ❌"

    elif any(word in email.lower() for word in [
        "support", "verify", "security", "admin", "update"
    ]):
        status = "Suspicious Email ⚠️"

    return jsonify({
        "email": email,
        "status": status
    })


# ==========================
# IP Checker Page
# ==========================

@app.route("/ip_checker")
def ip_checker():
    return render_template("ip_checker.html")


# ==========================
# IP Checker API
# ==========================

@app.route("/check_ip", methods=["POST"])
def check_ip():

    data = request.get_json()

    ip = data.get("ip")

    try:
        ipaddress.ip_address(ip)

        return jsonify({
            "ip": ip,
            "status": "Valid IP Address ✅"
        })

    except:

        return jsonify({
            "ip": ip,
            "status": "Invalid IP Address ❌"
        })


# ==========================
# Hash Checker Page
# ==========================

@app.route("/hash_checker")
def hash_checker():
    return render_template("hash_checker.html")


# ==========================
# Hash Generator API
# ==========================

@app.route("/generate_hash", methods=["POST"])
def generate_hash():

    data = request.get_json()

    text = data.get("text")

    if not text:

        return jsonify({
            "hash": ""
        })

    hash_value = hashlib.sha256(text.encode()).hexdigest()

    return jsonify({
        "hash": hash_value
    })


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans ORDER BY id DESC")

    scans = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        scans=scans
    )


# ==========================
# PDF Report
# ==========================

@app.route("/report")
def report():

    filename = "CyberShield_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Cyber Shield AI Security Report",
            styles["Title"]
        )
    )

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans")

    data = cursor.fetchall()

    conn.close()

    for row in data:

        story.append(
            Paragraph(
                f"""
                URL : {row[1]}<br/>
                Status : {row[2]}<br/>
                Score : {row[3]}<br/>
                Time : {row[4]}<br/><br/>
                """,
                styles["Normal"]
            )
        )

    doc.build(story)

    return send_file(filename, as_attachment=True)
# ==========================
# Run Server
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
    