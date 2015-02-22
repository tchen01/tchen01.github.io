//smoothScroll.init({
//    speed: 700, // Integer. How fast to complete the scroll in milliseconds
//    easing: 'easeInOutCubic', // Easing pattern to use
//    offset: window.innerHeight/20,
//});

var colors = ["rgb(39,170,225)", "red", "rgb(0, 167,157)", "rgb(247, 138, 30)", "rgb(28,117,188)", "rgb(238, 42,123)", "pink"];
//var menuItems = document.getElementsByClassName( 'menuItem' );
var sections = document.getElementsByTagName( 'section' );
var container = document.getElementById('contentContainer');
var whiteSpace = document.getElementById('whitespace');
var page = 0;
var animating = false;

for(var i=0; i<sections.length; i++){
   // menuItems[i].style.borderLeft = "5px solid " + colors[i];
    //menuItems[i].addEventListener('click', menuSelect);
    sections[i].addEventListener('mousedown', startTime, false);
    sections[i].addEventListener('mouseup', sectionClick, false);
    
    titles = sections[i].getElementsByClassName( 'title' );
    for(var j=0; j<titles.length;j++){
        titles[j].style.backgroundColor = colors[i];
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
    var tipSec = document.createElement('div');
    tipSec.innerHTML = "<section class='section' id='tip'><h3 class='about'>Click on a card to read more</h3><div class='titles'><div class='line toggle hidden' style='background-color: black;' onclick='tipRemove()'>remove</div></div><div class='description toggle hidden' onclick='tipRemove()'><div class='line'>click here to remove this card</div></div></section> ";
    tipSec.id = "tip";
    container.insertBefore(tipSec, sections[1])
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
        if (c.indexOf(name) == 0) return    c.substring(name.length,c.length);
    }
    return "";
}