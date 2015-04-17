var colors = ["rgb(39,170,225)","rgb(238, 42,123)", "rgb(0, 167,157)","red",  "rgb(28,117,188)", "rgb(247, 138, 30)", "rgb(181, 129, 188)"];

var blues = ["rgb(88, 147, 172)","rgb(97, 112, 152)", "rgb(86, 129, 167)","#7085cc",  "rgb(44, 115, 170)", "rgb(70, 85, 170)", "rgb(112, 126, 201)"];

var reds = ["rgb(172, 88, 117)","rgb(152, 97, 97)", "rgb(167, 86, 111)","#cc7b70",  "rgb(170, 44, 44)", "rgb(170, 70, 85)", "rgb(201, 112, 112)"];


var sections = document.getElementsByTagName( 'section' );
var container = document.getElementById('contentContainer');
var whiteSpace = document.getElementById('whitespace');
var page = 0;
var animating = false;


var offset = Math.floor(Math.random() * colors.length)
for(var i=0; i<sections.length; i++){
    sections[i].addEventListener('mousedown', startTime, false);
    sections[i].addEventListener('mouseup', sectionClick, false);
    
    titles = sections[i].getElementsByClassName( 'title' );
//    sections[i].style.borderTop = "2px solid " + colors[ (i + offset) % colors.length];;
    for(var j=0; j<titles.length;j++){
        titles[j].style.backgroundColor = colors[ (i + offset) % colors.length];
    }
}

if( getCookie("tip") !== "false" ){
    tipCreate();
}

function startTime(){
    time = new Date();
}
function sectionClick(e){
    if( new Date() - time < 250){
        var em = this.getElementsByClassName( 'toggle' );
        for(i=0;i<em.length;i++){
            em[i].classList.contains('hidden') ? em[i].classList.remove( 'hidden' ) : em[i].classList.add( 'hidden' );
        } 
    }
    
}

function tipCreate(){
    var tipSec = document.createElement('section');
    tipSec.id = "tip";
    container.insertBefore(tipSec, sections[1])
    var tipSec = document.getElementById( 'tip' );
    
    tipSec.outerHTML = "<section class='section' id='tip'><h3 class='about'>Click on a card to read more</h3><div class='titles'><div class='line toggle hidden' style='background-color: black;' onclick='tipRemove()'>remove</div></div><div class='description toggle hidden' onclick='tipRemove()'><div class='line'>click here to remove this card</div></div></section> ";
    // style='border-top: 2px solid black;'

    var tipSec = document.getElementById('tip');
    tipSec.addEventListener('mousedown', startTime, false);
    tipSec.addEventListener('mouseup', sectionClick, false);
}

function tipRemove(){
    document.cookie = "tip = false";
    container.removeChild(document.getElementById('tip'));
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}