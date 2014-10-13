//smooth scroll
$(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});


//reveal any elements with ".extra" class
$(function(){
    $("section").click(function(event) {
        $(this).find('.extra').toggle();
		$(this).find('.hide').toggle();		//is slideToggle() slow?
    });
});
