function ASCIIAnimation(animArray, speed, DOMtarget) {
    var currentFrame = 0;
    for(var i = 0; i < animArray.length; i++) {
        animArray[i] = animArray[i].replace(/ /g,"&nbsp;");
        //animArray[i] = "<pre>" + animArray[i] + "</pre>";
    }
    DOMtarget.innerHTML = animArray[0];
    currentFrame++;
    this.animation = setInterval(function() {
        DOMtarget.innerHTML = animArray[currentFrame];
        currentFrame++;
        if(currentFrame >= animArray.length) currentFrame = 0;
    }, speed);
    this.getCurrentFrame = function() {
        return currentFrame;
    }
}
ASCIIAnimation.prototype.stopAnimation = function() {
    clearInterval(this.animation);
}
const button_loading = ["....", "-...", "'-..", "-'-.", ".-'-", "..-'", "...-", "....", "...."]

// toggle nav bar
var nav = document.querySelector(".div1");
var div2 = document.querySelector(".div2");
var parent = document.querySelector(".parent");
var navToggle = document.querySelector(".toggle-nav");

let colapse = false;

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0) === " ") {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length, cookie.length);
        }
    }
    return null;
}

let collapse = getCookie("navCollapsed") === "true"; // Get the saved state from the cookie

function updateNavState() {
    if (collapse) {
        nav.style.display = "none";
        parent.style.gridTemplateColumns = "1fr";
        div2.style.transition = "all 0.5s ease-in-out";
    } else {
        nav.style.display = "block";
        parent.style.gridTemplateColumns = "203px 1fr";
    }
}

updateNavState();

navToggle.addEventListener("click", function () {
    collapse = !collapse;
    updateNavState();
    setCookie("navCollapsed", collapse, 7); // Save the state in a cookie for 7 days
});


function checkIfOptionExists(input, select) {
    const inputValue = input;
    const options = select.options;

    if (inputValue === "") {
        return true; // Return false for empty input
    }

    for (let i = 0; i < options.length; i++) {
        if (inputValue === options[i].value) {
            options[i].selected = true;
            return true;
        }
    }

    return false;
}

function enter(event, nextfield) {
    if (event.keyCode === 13) {
        event.preventDefault();
        if (nextfield) {
            nextfield.focus();
        }
    }
}
let inputFields = document.querySelectorAll("input");

inputFields.forEach(function (input, index) {
    input.addEventListener("keydown", function (event) {
        if (index <= inputFields.length - 1) {
            enter(event, inputFields[index + 1]);
        } else {
            enter(event, button);
        }
    });
});
function formatDate(inputDate) {
    const date = new Date(inputDate);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}