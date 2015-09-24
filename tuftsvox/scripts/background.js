

var title = document.getElementById("title");
var menu = document.getElementById("menu");
var spacer = document.getElementById("menuSpacer");
var space = menu.offsetHeight;

smoothScroll.init({
    offset: space + 10, 
});

function fixMenu(){
    if( window.scrollY > title.scrollHeight){
        menu.classList.add("fixedmenu");
        spacer.style.height = space+'px';  
    } else {
        menu.classList.remove("fixedmenu");
        spacer.style.height = 0;
    }
}

document.addEventListener("scroll", fixMenu);

/*
$.getScript("https://api.tumblr.com/v2/blog/tuftsvox.tumblr.com/posts?_=1442926251207", function(script, textStatus, jqXHR) {
  console.log(window.tumblr_api_read);
});
*/

$.ajax({
    url: 'https://api.tumblr.com/v2/blog/tuftsvox.tumblr.com/posts?_=1442926251207&offset=0',
    dataType: 'JSONP',
    type: 'GET',
    success: function (data) {
        console.log(data);
    }
});