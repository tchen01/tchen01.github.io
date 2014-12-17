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

