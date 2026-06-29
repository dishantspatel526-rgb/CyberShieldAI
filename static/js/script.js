/* =====================================
   CYBER SHIELD AI
   Main JavaScript
===================================== */


// Page Load Animation

document.addEventListener(
    "DOMContentLoaded",
    function(){

        console.log(
            "Cyber Shield AI Loaded Successfully 🛡"
        );

    }
);



// Smooth Scroll

document.querySelectorAll("a").forEach(
    link => {

        link.addEventListener(
            "click",
            function(){

                console.log(
                    "Opening:",
                    this.href
                );

            }
        );

    }
);



// Alert Helper

function showMessage(message){

    alert(message);

}



// Loading Effect

function loading(button){


    button.innerHTML =
    "Scanning...";

    button.disabled=true;


}