/* =====================================
   CYBER SHIELD AI
   PART 3 - JAVASCRIPT
===================================== */

// =========================
// Loader
// =========================

window.addEventListener("load", function () {

    const loader = document.getElementById("loader");

    setTimeout(() => {

        loader.style.opacity = "0";

        loader.style.visibility = "hidden";

    }, 1800);

});


// =========================
// Matrix Rain Effect
// =========================

const canvas = document.getElementById("matrix");

if (canvas) {

    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const letters =
        "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&@";

    const fontSize = 16;

    const columns =
        canvas.width / fontSize;

    const drops = [];

    for (let i = 0; i < columns; i++) {

        drops[i] = 1;

    }

    function drawMatrix() {

        ctx.fillStyle = "rgba(5,8,22,0.08)";
        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.fillStyle = "#00ffe7";
        ctx.font = fontSize + "px monospace";

        for (let i = 0; i < drops.length; i++) {

            const text =
                letters.charAt(
                    Math.floor(
                        Math.random() *
                        letters.length
                    )
                );

            ctx.fillText(
                text,
                i * fontSize,
                drops[i] * fontSize
            );

            if (
                drops[i] * fontSize >
                    canvas.height &&
                Math.random() > 0.97
            ) {

                drops[i] = 0;

            }

            drops[i]++;

        }

    }

    setInterval(drawMatrix, 35);

    window.addEventListener("resize", () => {

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

    });

}


// =========================
// Hero Typing Effect
// =========================

const heading =
document.querySelector(".hero-text h1");

if (heading) {

    const original =
        heading.innerHTML;

    heading.innerHTML = "";

    let i = 0;

    function type() {

        if (i < original.length) {

            heading.innerHTML +=
                original.charAt(i);

            i++;

            setTimeout(type, 35);

        }

    }

    setTimeout(type, 2000);

}


// =========================
// Navbar Scroll Effect
// =========================

window.addEventListener("scroll", () => {

    const nav =
        document.querySelector("nav");

    if (window.scrollY > 50) {

        nav.style.background =
            "#02040d";

    }

    else {

        nav.style.background =
            "rgba(0,0,0,.45)";

    }

});


// =========================
// Reveal Animation
// =========================

const sections =
document.querySelectorAll("section");

window.addEventListener("scroll", reveal);

function reveal() {

    const trigger =
        window.innerHeight - 120;

    sections.forEach(sec => {

        const top =
            sec.getBoundingClientRect().top;

        if (top < trigger) {

            sec.style.opacity = "1";
            sec.style.transform =
            "translateY(0px)";

        }

    });

}


// =========================
// Card Hover Sound
// =========================

const cards =
document.querySelectorAll(".card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform =
        "translateY(-12px) scale(1.03)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform =
        "translateY(0px)";

    });

});


// =========================
// Ripple Button
// =========================

const buttons =
document.querySelectorAll("button");

buttons.forEach(btn => {

    btn.addEventListener("click", function (e) {

        const circle =
        document.createElement("span");

        circle.classList.add("ripple");

        const rect =
        btn.getBoundingClientRect();

        circle.style.left =
        e.clientX - rect.left + "px";

        circle.style.top =
        e.clientY - rect.top + "px";

        btn.appendChild(circle);

        setTimeout(() => {

            circle.remove();

        }, 600);

    });

});


// =========================
// Fake Scan Counter
// =========================

let count = 0;

const interval =
setInterval(() => {

    count++;

    console.log(
        "Cyber Scan : " + count
    );

    if (count == 100) {

        clearInterval(interval);

    }

}, 80);


// =========================
// Console Message
// =========================

console.log(

"%cCyber Shield AI Loaded Successfully",

"color:#00ffe7;font-size:20px;font-weight:bold"

);

async function scanURL() {

    let url = document.getElementById("urlInput").value;

    if (url == "") {
        alert("Please Enter URL");
        return;
    }

    let response = await fetch("/scan", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        data =  requestAnimationFrame.get__json()
            url: data.get("url")  

    })

    let data = await response.json();

    let html = `
        <h2>${data.status}</h2>
        <h3>Risk Score : ${data.score}/100</h3>
    `;

    data.reasons.forEach(function(reason){

        html += `<p>• ${reason}</p>`;

    });

    document.getElementById("resultBox").innerHTML = html;

}

function checkPassword(){

let password=document.getElementById("passwordInput").value;

let result=document.getElementById("passwordResult");

let score=0;

let tips=[];

if(password.length>=8){

score+=20;

}else{

tips.push("Minimum 8 characters");

}

if(/[A-Z]/.test(password)){

score+=20;

}else{

tips.push("Add uppercase letter");

}

if(/[a-z]/.test(password)){

score+=20;

}else{

tips.push("Add lowercase letter");

}

if(/[0-9]/.test(password)){

score+=20;

}else{

tips.push("Add number");

}

if(/[!@#$%^&*(),.?":{}|<>]/.test(password)){

score+=20;

}else{

tips.push("Add special character");

}

let status="";
let color="";

if(score==100){

status="Very Strong";

color="safe";

}

else if(score>=80){

status="Strong";

color="safe";

}

else if(score>=60){

status="Medium";

color="warning";

}

else{

status="Weak";

color="danger";

}

result.innerHTML=`

<h2 class="${color}">${status}</h2>

<h3>Password Score : ${score}/100</h3>

<p>${tips.join("<br>")}</p>

`;

}

function scanEmail(){

let email =
document.getElementById("emailInput").value.toLowerCase();

let result =
document.getElementById("emailResult");

if(email==""){

result.innerHTML="<h2>Please paste an email.</h2>";

return;

}

let score=100;

let reasons=[];

const keywords=[

"urgent",
"verify",
"click here",
"free",
"winner",
"bank",
"otp",
"gift",
"password",
"limited time",
"login",
"confirm"

];

keywords.forEach(word=>{

if(email.includes(word)){

score-=8;

reasons.push("Suspicious keyword detected : "+word);

}

});

if(email.includes("http://")){

score-=20;

reasons.push("Unsafe HTTP link found");

}

if(email.includes(".xyz")){

score-=15;

reasons.push("Unknown domain extension");

}

let status="";
let color="";

if(score>=80){

status="SAFE";

color="safe";

}

else if(score>=50){

status="SUSPICIOUS";

color="warning";

}

else{

status="PHISHING";

color="danger";

}

if(reasons.length==0){

reasons.push("No suspicious indicators found.");

}

result.innerHTML=

`

<h2 class="${color}">${status}</h2>

<h3>Trust Score : ${score}/100</h3>

<p>${reasons.join("<br>")}</p>

`;

}

/* ======================
Dashboard Counter
====================== */

function animateValue(id,end){

let obj=document.getElementById(id);

if(!obj) return;

let start=0;

let speed=25;

let timer=setInterval(function(){

start++;

obj.innerHTML=start;

if(start>=end){

clearInterval(timer);

}

},speed);

}

animateValue("safeCount",158);

animateValue("warningCount",39);

animateValue("dangerCount",18);

animateValue("totalCount",215);