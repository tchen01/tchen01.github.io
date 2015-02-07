

var colors = ["rgb(39,170,225)", "red", "rgb(0, 167,157)", "rgb(247, 138, 30)", "rgb(28,117,188)", "rgb(238, 42,123)", "pink"];    
var menuItems = document.getElementsByClassName( 'menuItem' );
var section = document.getElementsByClassName( 'section' );
var container = document.getElementById('contentContainer');
var whiteSpace = document.getElementById('whitespace');
var page = 0;
var animating = false;

document.addEventListener("mousewheel", scroll, false);
// Firefox
document.addEventListener("DOMMouseScroll", scroll, false);

hide();
container.style.overflowY = "hidden";

var del = 0;
function scroll(e){
    if( !animating ){
        var threshold = 400;
        del += e.wheelDelta;
        if( del > threshold){
            cycle(5);
            page = mod(6, page -1);
            select();
            del = 0;
        }
        else if(del < -threshold){
            cycle(1);  
            page = mod(6, page +1);
            select();
            del = 0;

        }
    }
}
//container.addEventListener("scroll", scroller, false);

for(var i=0; i<menuItems.length; i++){
    menuItems[i].style.borderLeft = "5px solid " + colors[i];
    menuItems[i].addEventListener('click', menuSelect);
    
    titles = section[i].getElementsByClassName( 'title' );
    for(var j=0; j<titles.length;j++){
        titles[j].style.backgroundColor = colors[i];
    }
}

function mod(n, m) {
        return ((m % n) + n) % n;
}

function menuSelect(){
    //console.log(this.innerText); 
    var Npage = parseInt( this.dataset.num );
    
    //cycles sections
    console.log( mod(6, Npage - page) );
    //scroller()
    cycle( mod(6, Npage - page) );
    page = Npage;
    select();
}

function hide(){
    var sections = document.getElementsByClassName('section');
    for(var i=0; i<sections.length;i++){
        sections[i].classList.add( 'hidden' );
    }
    for(var i=0; i<3;i++){
        sections[i].classList.remove( 'hidden' );
    }
}

//add some sort of animation
function cycle(n){
    var sections = document.getElementsByClassName('section');
    if( n < 4 ){
        for(var i=0;i<n;i++){
            sections[0+i].classList.add('swipe');
            sections[3+i].classList.remove( 'hidden' );            
        }
        animating = true;
        setTimeout(function(){
            for(var i=0;i<n;i++){
                container.insertBefore(sections[0], whiteSpace);
                sections[5].classList.remove( 'swipe' );
                sections[5].classList.add( 'hidden' );
                animating = false;
            }
        }, 500);
    } else {
        for(var i=0;i<6-n;i++){
            container.insertBefore(sections[5], sections[0]);
            sections[0].classList.remove( 'hidden' );
            sections[3].classList.add('hidden');

            setTimeout(function(){
            }, 500);
            
        }
    }
}

function select(){
        //hides current visible section(s)
    var selected = document.getElementsByClassName( 'selected' );
    for(var i=0; i<selected.length; i++){
        selected[i].classList.remove( 'selected');
    }
    menuItems[page].classList.add( 'selected' );
}



function scroller(){
    var sections = document.getElementsByClassName('section');
    var height = 0;
    for(var i=0; i<sections.length;i++){
        console.log(sections[i].scrollHeight);
        height += sections[i].scrollHeight;
        if( height < container.scrollTop  ){
            console.log(i, height);
            container.insertBefore(sections[0], whiteSpace);
        }
    }
}
