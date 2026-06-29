from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import hashlib
import ipaddress
import requests
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

DATABASE = "database.db"


# ===============================
# Database Setup
# ===============================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_type TEXT,
        input_value TEXT,
        result TEXT,
        score INTEGER,
        scan_time TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ===============================
# Home
# ===============================

@app.route("/")
def home():
    return render_template("index.html")


# ===============================
# Pages
# ===============================

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")


@app.route("/password")
def password():
    return render_template("password.html")


@app.route("/email")
def email():
    return render_template("email.html")


@app.route("/ip")
def ip():
    return render_template("ip.html")


@app.route("/hash")
def hash_page():
    return render_template("hash.html")


@app.route("/dashboard")
def dashboard():

    conn = get_db()

    scans = conn.execute(
        "SELECT * FROM scans ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        scans=scans
    )


# ===============================
# Save Scan
# ===============================

def save_scan(scan_type, value, result, score):

    conn = get_db()

    conn.execute(
        """
        INSERT INTO scans
        (scan_type,input_value,result,score,scan_time)
        VALUES(?,?,?,?,?)
        """,
        (
            scan_type,
            value,
            result,
            score,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

    # ===============================
# URL Scanner API
# ===============================

@app.route("/scan_url", methods=["POST"])
def scan_url():

    data = request.get_json()

    url = data.get("url", "")


    if url == "":

        return jsonify({

            "status":"URL Missing",

            "score":0

        })


    result = "Safe Website ✅"

    score = 95



    suspicious_words = [

        "login",
        "verify",
        "bank",
        "free",
        "gift",
        "update"

    ]


    for word in suspicious_words:


        if word in url.lower():


            result = "Suspicious Website ⚠️"

            score = 40

            break



    return jsonify({

        "status":result,

        "score":score

    })

# ===============================
# Password Checker API
# ===============================
@app.route("/check_password", methods=["POST"])
def check_password():

    data = request.get_json()

    password = data.get("password", "")

    score = 0

    if len(password) >= 8:
        score += 25

    if any(c.isupper() for c in password):
        score += 25

    if any(c.isdigit() for c in password):
        score += 25

    if any(not c.isalnum() for c in password):
        score += 25


    if score < 50:
        strength = "Weak ❌"

    elif score < 80:
        strength = "Medium ⚠️"

    else:
        strength = "Strong ✅"


    return jsonify({
        "strength": strength,
        "score": score
    })

# ===============================
# Email Checker API
# ===============================

@app.route("/check_email", methods=["POST"])
def check_email():

    try:

        data = request.get_json()

        email = data.get("email", "")

        if email.strip() == "":

            return jsonify({
                "status": "Email Missing",
                "score": 0
            })

        status = "Valid Email ✅"
        score = 95

        if "@" not in email or "." not in email:

            status = "Invalid Email ❌"
            score = 20


        return jsonify({
            "status": status,
            "score": score
        })

    except Exception as e:

        return jsonify({
            "status": str(e),
            "score": 0
        })

# ===============================
# IP Checker API
# ===============================
@app.route("/check_ip", methods=["POST"])
def check_ip():

    data = request.get_json()

    ip = data.get("ip", "").strip()

    try:

        ipaddress.ip_address(ip)

        return jsonify({
            "status": "Valid IP ✅",
            "score": 100
        })

    except:

        return jsonify({
            "status": "Invalid IP ❌",
            "score": 0
        })


# ===============================
# SHA-256 Hash Generator
# ===============================
@app.route("/generate_hash", methods=["POST"])
def generate_hash():

    data = request.get_json()

    text = data.get("text", "").strip()

    if text == "":

        return jsonify({
            "hash": ""
        })

    hash_value = hashlib.sha256(
        text.encode()
    ).hexdigest()

    return jsonify({
        "hash": hash_value
    })


# ===============================
# PDF Report
# ===============================

@app.route("/report")
def report():

    filename = "CyberShieldAI_Report.pdf"

    conn = get_db()

    scans = conn.execute(
        "SELECT * FROM scans ORDER BY id DESC"
    ).fetchall()

    conn.close()

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Cyber Shield AI Security Report",
            styles["Title"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["Normal"])
    )

    for scan in scans:

        story.append(
            Paragraph(
                f"""
                <b>Type:</b> {scan['scan_type']}<br/>
                <b>Input:</b> {scan['input_value']}<br/>
                <b>Result:</b> {scan['result']}<br/>
                <b>Score:</b> {scan['score']}<br/>
                <b>Time:</b> {scan['scan_time']}<br/><br/>
                """,
                styles["BodyText"]
            )
        )

    doc.build(story)

    return send_file(
        filename,
        as_attachment=True
    )


# ===============================
# Run Flask
# ===============================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
    