smoothScroll.init({
    speed: 700, // Integer. How fast to complete the scroll in milliseconds
    easing: 'easeInOutCubic', // Easing pattern to use
});



window.onload = function listen(){
  var sections = document.getElementsByTagName( 'section' );
  console.log( sections.length );
  for( l=0; l<sections.length; l++){
    sections[l].addEventListener("mouseup", switcher );
  }
}

function switcher(){
  var em = this.getElementsByClassName( 'toggle' );
  for(i=0;i<em.length;i++){
    em[i].style.display == 'none' ? em[i].style.display = 'block' : em[i].style.display = 'none';
  }
}

document.addEventListener( 'scroll', hidename );

function hidename(){
  var logoDisp = document.getElementById('logo').style.display;
  if(document.getElementById('home').offsetHeight - 50 <= document.body.scrollTop){
    document.getElementById('logo').style.display = 'block'
  } else {
    document.getElementById('logo').style.display = 'none';
    
  }
}