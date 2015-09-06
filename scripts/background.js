
var sections = document.getElementsByTagName( 'section' );
var container = document.getElementById('contentContainer');
var whiteSpace = document.getElementById('whitespace');

for(var i=0; i<sections.length; i++){
    sections[i].addEventListener('mousedown', startTime, false);
    sections[i].addEventListener('mouseup', sectionClick, false);
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
    
    tipSec.outerHTML = "<section class='section' id='tip' ><div class='about'><h3>Click on a card to read more</h3></div><div class='item'><div class='title toggle hidden' onclick='tipRemove()'>remove</div><div class='content toggle hidden' onclick='tipRemove()'>click here to remove this card</div></div><div class='item'><div class='title toggle hidden'>cookies</div><div class='content toggle hidden'>I use one cookie. (apparently it's a trend to announce this)</div></div></section> ";
    

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