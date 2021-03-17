document.addEventListener("DOMContentLoaded", function(){
    window.addEventListener("scroll", function() {
        var menu = document.getElementsByTagName("nav")[0];
        var footer = document.getElementsByClassName("footer")[0];
        var rect1 = menu.getBoundingClientRect();
        var rect2 = footer.getBoundingClientRect();
        var overlap = !(rect1.bottom < rect2.top)

        if (overlap) {
            menu.style.height = (rect1.height - (rect1.bottom - rect2.top) + 1) +"px"
        } else {
            if ((rect1.height - (rect1.bottom - rect2.top) + 1) < window.innerHeight)  {
                menu.style.height = (rect1.height - (rect1.bottom - rect2.top) + 1) +"px"
            } else {
                menu.style.height = "";
            }
        }

    })
});
