
var sections = document.getElementsByTagName( 'section' );
var titles = document.getElementsByClassName( 'about' );
var container = document.getElementById('contentContainer');
var whiteSpace = document.getElementById('whitespace');

for(var i=0; i<titles.length; i++){
    titles[i].addEventListener('mouseup', titleClick, false);
}


if( getCookie("tip") !== "false" ){
    tipCreate();
}

function titleClick(e){
    var em = this.parentNode.getElementsByClassName( 'toggle' );
    for(i=0;i<em.length;i++){
        em[i].classList.contains('hidden') ? em[i].classList.remove( 'hidden' ) : em[i].classList.add( 'hidden' );
    } 
}

function tipCreate(){
    var tipSec = document.createElement('section');
    tipSec.id = "tip";
    container.insertBefore(tipSec, sections[1])
    var tipSec = document.getElementById( 'tip' );
    
    tipSec.outerHTML = "<section class='section' id='tip' ><div class='about'><h3>Click on a title to read more...</h3></div><div class='item'><a><div class='title toggle hidden' onclick='tipRemove()'>remove</div><div class='content toggle hidden' onclick='tipRemove()'>click here to remove this section</div></a></div><div class='item'><div class='title toggle hidden'>cookies</div><div class='content toggle hidden'>I use one cookie. (to hide this section in the future)</div></div></section> ";
    

    var tipSec = document.getElementById('tip');
    tipSec.addEventListener('mouseup', titleClick, false);
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