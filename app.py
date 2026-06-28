import os
import sqlite3
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
# Pages Routes
# ==========================


@app.route("/")
def home():

    return render_template("index.html")



@app.route("/scanner")
def scanner():

    return render_template("scanner.html")



@app.route("/password")
def password():

    return render_template("password.html")



@app.route("/email")
def email():

    return render_template("email.html")
# ==========================
# URL Scanner
# ==========================

@app.route("/scan", methods=["POST"])
def scan_url():

    data = request.get_json()

    url = data.get("url")


    if not url:

        return jsonify({

            "error": "URL required"

        })


    # Simple security checking logic

    suspicious_words = [

        "login",
        "verify",
        "bank",
        "password",
        "free",
        "gift"

    ]


    score = 100
    status = "Safe"


    for word in suspicious_words:

        if word in url.lower():

            score -= 15
            status = "Suspicious"



    if score < 50:

        status = "Danger"



    # Save scan result

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    cursor.execute("""

    INSERT INTO scans

    (url,status,score,scan_time)

    VALUES (?,?,?,?)

    """,

    (

        url,

        status,

        score,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))


    conn.commit()

    conn.close()



    return jsonify({

        "url":url,

        "status":status,

        "score":score

    })





# ==========================
# Dashboard
# ==========================


@app.route("/dashboard")
def dashboard():


    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM scans ORDER BY id DESC"
    )


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


    content=[]


    content.append(

        Paragraph(

            "Cyber Shield AI Security Report",

            styles["Title"]

        )

    )


    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM scans"
    )


    data = cursor.fetchall()


    conn.close()



    for scan in data:


        text = f"""

        URL : {scan[1]} <br/>

        Status : {scan[2]} <br/>

        Score : {scan[3]} <br/>

        Time : {scan[4]}

        """


        content.append(

            Paragraph(

                text,

                styles["Normal"]

            )

        )



    doc.build(content)



    return send_file(filename)

# ==========================
# Password Checker
# ==========================


@app.route("/check_password", methods=["POST"])
def check_password():


    data = request.get_json()


    password = data.get("password")


    if not password:

        return jsonify({

            "error":"Password required"

        })


    score = 0


    if len(password) >= 8:

        score += 25


    if any(char.isupper() for char in password):

        score += 25


    if any(char.isdigit() for char in password):

        score += 25


    if any(char in "!@#$%^&*" for char in password):

        score += 25



    if score >= 75:

        strength = "Strong"


    elif score >= 50:

        strength = "Medium"


    else:

        strength = "Weak"



    return jsonify({

        "strength":strength,

        "score":score

    })





# ==========================
# Email Security Checker
# ==========================


@app.route("/check_email", methods=["POST"])
def check_email():


    data = request.get_json()


    email = data.get("email")


    if not email:

        return jsonify({

            "error":"Email required"

        })



    suspicious = [

        "gmail",

        "yahoo",

        "hotmail"

    ]


    status = "Normal"



    for item in suspicious:

        if item in email.lower():

            status="Valid Email"



    return jsonify({

        "email":email,

        "status":status

    })





# ==========================
# Start Server
# ==========================


if __name__ == "__main__":


    app.run(

        debug=True

    )