function toggleMenu(){
    var navLinks = document.getElementById('nav-items');
    navLinks.classList.toggle('navbar-nav-active');
}

window.onscroll = function() {
    var navHeight = document.getElementById('navbar').clientHeight + document.getElementById('separador').clientHeight + document.getElementById('subtitulo').clientHeight;
    var scrollButton = document.getElementById('scroll');
    scrollButton.style.top = document.getElementById('filtros').clientHeight + 200 + "px";
    if (document.body.scrollTop >= navHeight || document.documentElement.scrollTop >= navHeight){
        scrollButton.style.display = "flex";
    } else {
        scrollButton.style.display = "none";
    }
}

function scrollToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}