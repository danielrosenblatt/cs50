/// CURATEEXPLORE.HTML

//Reveal Functions
function revealAll() {
    revealButton();
    revealTime();
    revealColor();
    revealGallery();
}

function revealButton() {
    var x = document.getElementById("buttonz");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
function revealTime() {
    var x = document.getElementById("time");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function revealColor() {
    var x = document.getElementById("color");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function revealGallery() {
    var x = document.getElementById("gallery");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

// Button Parameter Functions and Variables //
// Time //

var time = "merp";

// Way Way Back
function waywaybackfunction() {
    if ( time === "waywayback") {
        time = "any";
        var d = document.getElementById("waywayback");
        d.className = "button buttonli";
    }
    else {
        time = "waywayback";
        var d = document.getElementById("waywayback");
        d.className += " clickedtime";
    }
}

// Way Back
function waybackfunction() {
    if ( time === "wayback") {
        time = "any";
        var d = document.getElementById("wayback");
        d.className = "button buttonli";
    }
    else {
        time = "wayback";
        var d = document.getElementById("wayback");
        d.className += " clickedtime";
    }
}

// Not So Far Back
function notsofarbackfunction() {
    if ( time === "notsofarback") {
        time = "any";
        var d = document.getElementById("notsofarback");
        d.className = "button buttonli";
    }
    else {
        time = "notsofarback";
        var d = document.getElementById("notsofarback");
        d.className += " clickedtime";
    }
}

// Color //
var color = "marp";

// Red
function redfunction() {
    if ( color === "red") {
        color = "any";
        var d = document.getElementById("buttonred");
        d.className = "colorbutton";
    }
    else {
        color = "red";
        var d = document.getElementById("buttonred");
        d.className += " clickedcolor";
    }
}

// Green
function greenfunction() {
    if ( color === "green") {
        color = "any";
        var d = document.getElementById("buttongreen");
        d.className = "colorbutton";
    }
    else {
        color = "green";
        var d = document.getElementById("buttongreen");
        d.className += " clickedcolor";
    }
}

// Yellow
function yellowfunction() {
    if ( color === "yellow") {
        color = "any";
        var d = document.getElementById("buttonyellow");
        d.className = "colorbutton";
    }
    else {
        color = "yellow";
        var d = document.getElementById("buttonyellow");
        d.className += " clickedcolor";
    }
}
// Black
function blackfunction() {
    if ( color === "black") {
        color = "any";
        var d = document.getElementById("buttonblack");
        d.className = "colorbutton";
    }
    else {
        color = "black";
        var d = document.getElementById("buttonblack");
        d.className += " clickedcolor";
    }
}

// White
function whitefunction() {
    if ( color === "white") {
        color = "any";
        var d = document.getElementById("buttonwhite");
        d.className = "colorbutton";
    }
    else {
        color = "white";
        var d = document.getElementById("buttonwhite");
        d.className += " clickedcolor";
    }
}

// Grey
function greyfunction() {
    if ( color === "grey") {
        color = "any";
        var d = document.getElementById("buttongrey");
        d.className = "colorbutton";
    }
    else {
        color = "grey";
        var d = document.getElementById("buttongrey");
        d.className += " clickedcolor";
    }
}

// Submit Form + Change Color, Time, Gallery Preference
function submitForm() {
    document.getElementById('hiddenTime').value = time;
    document.getElementById('hiddenColor').value = color;
    document.getElementById("myForm").submit();
}


// SAVEDTOURS.HTML

let activeBox = undefined;

function updateName(event) {
    let newText = event.target.value
    let idNum = event.target.name;
    $.post('/renametour', {'tourid': idNum, 'rename': newText}, function(data) {
        $("#tour" + idNum).html(newText);
        activeBox = undefined;

    })
}

$(document).on('click', '.tourname', function(event) {
    if (event.target.tagName == "INPUT") {
        return;
    }

    let idNum = event.target.id.substr(4);

    if (activeBox != undefined && activeBox.id != 'tour' + idNum) {
        $(document).off('change', '#inputBoxId', updateName);
        $('#' + activeBox.id).html(activeBox.origText);
    }


    activeBox = {
        origText: event.target.innerHTML,
        id: 'tour' + idNum
    }

    let target = $(event.target);
    let input_id = 'inputbox' + idNum;




    target.html("<input type='text' name='" + idNum +"' id='inputBoxId'></input>");

    $(document).on('change', '#inputBoxId', updateName);

})

// TOUR2.HTML
var slideIndex = 1;
var infoIndex = 1;
showSlides(slideIndex);
showInfo(infoIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
  showInfo(infoIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
  showInfo(infoIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

function showInfo(n) {
  var i;
  var info = document.getElementsByClassName("text");
  if (n > info.length) {infoIndex = 1}
  if (n < 1) {infoIndex = info.length}
  for (i = 0; i < info.length; i++) {
      info[i].style.display = "none";
  }
  info[infoIndex-1].style.display = "block";
}