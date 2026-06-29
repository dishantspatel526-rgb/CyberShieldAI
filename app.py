import hashlib

import ipaddress

import os

from dotenv import load_dotenv
from openai import OpenAI

import sqlite3
import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_file

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from dotenv import load_dotenv
from openai import OpenAI


# ==========================
# AI Setup
# ==========================

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



app = Flask(__name__)

# ==========================
# OpenAI Setup
# ==========================

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==========================
# Database
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
# Pages
# ==========================

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
# ADVANCED URL SCANNER
# ==========================

@app.route('/scan_url', methods=['POST'])
def scan_url():

    url = request.form.get("url")


    if not url:

        return render_template(
            "scanner.html",
            result="Please enter URL"
        )


    score = 100


    bad_words = [
        "login",
        "verify",
        "free",
        "gift",
        "update",
        "password"
    ]


    for word in bad_words:

        if word in url.lower():

            score -= 15



    if url.startswith("http://"):

        score -= 20



    if score >= 80:

        status = "Safe 🟢"


    elif score >= 50:

        status = "Medium 🟡"


    else:

        status = "Dangerous 🔴"



    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    cursor.execute(

        "INSERT INTO scans(url,status,score,scan_time) VALUES(?,?,?,?)",

        (

        url,

        status,

        score,

        datetime.now()

        )

    )


    conn.commit()

    conn.close()



    result = f"""

🛡 Cyber Shield AI Scan Result


URL:
{url}


Security Score:
{score}%


Risk Level:
{status}

"""


    return render_template(

        "scanner.html",

        result=result

    )



# ==========================
# PREMIUM DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():


    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM scans ORDER BY id DESC"
    )

    scans = cursor.fetchall()



    total = len(scans)


    safe = 0
    risk = 0


    for scan in scans:

        if scan[2] == "Safe":

            safe += 1

        else:

            risk += 1



    conn.close()



    return render_template(

        "dashboard.html",

        scans=scans,

        total=total,

        safe=safe,

        risk=risk

    )
# ==========================
# PROFESSIONAL PDF REPORT
# ==========================

@app.route("/report")
def report():


    filename = "CyberShield_AI_Report.pdf"



    doc = SimpleDocTemplate(filename)



    styles = getSampleStyleSheet()



    content = []



    content.append(

        Paragraph(

            "🛡 Cyber Shield AI Security Report",

            styles["Title"]

        )

    )



    content.append(

        Paragraph(

            f"Generated Time: {datetime.now()}",

            styles["Normal"]

        )

    )




    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()



    cursor.execute(
        "SELECT * FROM scans"
    )



    scans = cursor.fetchall()



    conn.close()



    content.append(

        Paragraph(

            f"Total Scans: {len(scans)}",

            styles["Heading2"]

        )

    )





    for scan in scans:


        data = f"""

        <b>URL:</b> {scan[1]} <br/>

        <b>Status:</b> {scan[2]} <br/>

        <b>Security Score:</b> {scan[3]}% <br/>

        <b>Scan Time:</b> {scan[4]} <br/>

        <hr/>

        """



        content.append(

            Paragraph(

                data,

                styles["Normal"]

            )

        )




    doc.build(content)



    return send_file(filename, as_attachment=True)


# ==========================
# Password Checker
# ==========================

@app.route("/check_password", methods=["POST"])
def check_password():


    data=request.get_json()


    password=data.get("password")


    score=0


    if len(password)>=8:
        score+=25


    if any(c.isupper() for c in password):
        score+=25


    if any(c.isdigit() for c in password):
        score+=25


    if any(c in "!@#$%^&*" for c in password):
        score+=25



    return jsonify({

        "score":score,

        "strength":
        "Strong" if score>=75 else "Weak"

    })



# ==========================
# Email Checker
# ==========================

@app.route("/check_email", methods=["POST"])
def check_email():


    data=request.get_json()


    email=data.get("email")


    return jsonify({

        "email":email,

        "status":
        "Valid" if "@" in email else "Invalid"

    })

# ==========================
# IP SECURITY CHECKER
# ==========================

@app.route("/ip_checker", methods=["GET","POST"])
def ip_checker():


    result = None


    if request.method == "POST":


        ip = request.form.get("ip")


        try:


            ip_obj = ipaddress.ip_address(ip)



            if ip_obj.is_private:


                result = f"""
                IP Address: {ip}

                Type: Private IP

                Status: Safe Local Network

                Security Tip:
                Use firewall and keep router updated.
                """



            else:


                result = f"""
                IP Address: {ip}

                Type: Public IP

                Status: Internet Facing

                Security Tip:
                Avoid exposing unnecessary ports.
                """



        except:


            result = "Invalid IP Address"



    return render_template(

        "ip_checker.html",

        result=result

    )
# ==========================
# FILE HASH CHECKER
# ==========================

@app.route("/hash_checker", methods=["GET","POST"])
def hash_checker():

    result = None


    if request.method == "POST":


        file = request.files.get("file")


        if file:


            data = file.read()


            sha256 = hashlib.sha256(data).hexdigest()



            result = f"""
File Name: {file.filename}

SHA-256 Hash:

{sha256}


Security Tip:
Always verify unknown files before opening.
"""


        else:

            result = "Please upload a file"



    return render_template(

        "hash_checker.html",

        result=result

    )

# ==========================
# LOCAL CYBER AI CHATBOT
# ==========================

@app.route("/chatbot", methods=["GET","POST"])
def chatbot():

    reply = None
    message = None


    if request.method == "POST":


        message = request.form.get("message")

        msg = message.lower()



        if "password" in msg:

            reply = """
🔐 Password Security:

Strong password me:
• Minimum 8-12 characters
• Uppercase + lowercase
• Numbers
• Special symbols

Same password har jagah use mat karo.
"""


        elif "phishing" in msg:

            reply = """
⚠️ Phishing Attack:

Phishing ek fake website/email attack hota hai
jisme attacker password ya personal data chura sakta hai.

Safety:
• Unknown links mat kholo
• Sender verify karo
• 2FA enable karo
"""


        elif "malware" in msg or "virus" in msg:

            reply = """
🦠 Malware:

Malware ek harmful software hota hai jo
computer ko damage kar sakta hai.

Protection:
• Antivirus use karo
• Unknown files avoid karo
• System update rakho
"""


        elif "firewall" in msg:

            reply = """
🛡 Firewall:

Firewall network traffic ko monitor karta hai
aur unsafe connections ko block karta hai.
"""


        elif "sql injection" in msg:

            reply = """
💻 SQL Injection:

Ye ek web attack hai jisme attacker database
queries ko manipulate karne ki koshish karta hai.

Protection:
• Input validation
• Parameterized queries
"""


        elif "vpn" in msg:

            reply = """
🌐 VPN:

VPN internet connection ko secure karta hai
aur privacy improve karta hai.
"""


        elif "2fa" in msg or "two factor" in msg:

            reply = """
🔒 Two Factor Authentication:

Password ke sath extra security layer add karta hai.
Account protection ke liye enable karna chahiye.
"""


        elif "cyber security" in msg:

            reply = """
🛡 Cyber Security:

Devices, networks aur data ko cyber attacks
se protect karne ki practice hai.
"""


        else:

            reply = """
🤖 Cyber Shield AI:

Mujhe cyber security related question pucho.

Try:
• What is malware?
• What is phishing?
• What is SQL injection?
• How to secure password?
• What is firewall?
"""



    return render_template(
        "chatbot.html",
        reply=reply,
        message=message
    )
# ==========================
# START SERVER
# ==========================

if __name__ == "__main__":

    app.run(debug=True)