/* ======================================
   Cyber Shield AI - script.js
   PART 1
====================================== */

// Matrix Background Effect
const canvas = document.getElementById("matrix");

if (canvas) {

    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const letters = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&@";
    const fontSize = 16;
    const columns = Math.floor(canvas.width / fontSize);

    const drops = [];

    for (let i = 0; i < columns; i++) {
        drops[i] = 1;
    }

    function drawMatrix() {

        ctx.fillStyle = "rgba(0,0,0,0.08)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#00ff66";
        ctx.font = fontSize + "px monospace";

        for (let i = 0; i < drops.length; i++) {

            const text =
                letters.charAt(
                    Math.floor(Math.random() * letters.length)
                );

            ctx.fillText(
                text,
                i * fontSize,
                drops[i] * fontSize
            );

            if (
                drops[i] * fontSize > canvas.height &&
                Math.random() > 0.97
            ) {
                drops[i] = 0;
            }

            drops[i]++;
        }
    }

    setInterval(drawMatrix, 35);

    window.addEventListener("resize", function () {

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

    });

}


// =========================
// URL Scanner
// =========================

async function scanURL() {

    const url =
        document.getElementById("urlInput").value.trim();

    if (url === "") {

        alert("Please enter a website URL.");

        return;

    }

    try {

        const response = await fetch("/scan_url", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                url: url

            })

        });

        const data = await response.json();

        let html = `
            <h2>${data.status}</h2>
            <h3>Security Score : ${data.score}/100</h3>
        `;

        if (data.reasons.length > 0) {

            html += "<ul>";

            data.reasons.forEach(function (reason) {

                html += `<li>${reason}</li>`;

            });

            html += "</ul>";

        }

        document.getElementById("result").innerHTML = html;

    }

    catch (error) {

        document.getElementById("result").innerHTML =
            "<h2>Server Error</h2>";

        console.log(error);

    }

}
// =========================
// Password Strength Checker
// =========================

function checkPassword() {

    const password = document.getElementById("passwordInput").value;
    const result = document.getElementById("passwordResult");

    let score = 0;
    let tips = [];

    if (password.length >= 8) score += 20;
    else tips.push("Minimum 8 characters");

    if (/[A-Z]/.test(password)) score += 20;
    else tips.push("Add an uppercase letter");

    if (/[a-z]/.test(password)) score += 20;
    else tips.push("Add a lowercase letter");

    if (/[0-9]/.test(password)) score += 20;
    else tips.push("Add a number");

    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 20;
    else tips.push("Add a special character");

    let status = "";

    if (score === 100)
        status = "🟢 Very Strong";
    else if (score >= 80)
        status = "🟢 Strong";
    else if (score >= 60)
        status = "🟡 Medium";
    else
        status = "🔴 Weak";

    result.innerHTML = `
        <h2>${status}</h2>
        <h3>Score : ${score}/100</h3>
        <ul>
            ${tips.map(t => `<li>${t}</li>`).join("")}
        </ul>
    `;
}


// =========================
// Email Phishing Checker
// =========================

function scanEmail() {

    const email = document
        .getElementById("emailInput")
        .value
        .toLowerCase();

    const result =
        document.getElementById("emailResult");

    if (email === "") {

        result.innerHTML =
            "<h3>Please paste an email.</h3>";

        return;
    }

    let score = 100;

    let reasons = [];

    const keywords = [

        "urgent",
        "verify",
        "click here",
        "free",
        "winner",
        "bank",
        "otp",
        "gift",
        "password",
        "login",
        "confirm"

    ];

    keywords.forEach(word => {

        if (email.includes(word)) {

            score -= 8;

            reasons.push(
                "Suspicious keyword : " + word
            );

        }

    });

    if (email.includes("http://")) {

        score -= 20;

        reasons.push("HTTP link detected");

    }

    if (email.includes(".xyz")) {

        score -= 15;

        reasons.push("Unknown domain detected");

    }

    let status = "";

    if (score >= 80)
        status = "🟢 SAFE";
    else if (score >= 50)
        status = "🟡 SUSPICIOUS";
    else
        status = "🔴 PHISHING";

    if (reasons.length === 0) {

        reasons.push(
            "No suspicious indicators detected."
        );

    }

    result.innerHTML = `
        <h2>${status}</h2>
        <h3>Risk Score : ${score}/100</h3>
        <ul>
            ${reasons.map(r => `<li>${r}</li>`).join("")}
        </ul>
    `;
}


// =========================
// Console Message
// =========================

console.log("Cyber Shield AI Loaded Successfully");