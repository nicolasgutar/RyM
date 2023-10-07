var flag = true
function toggleMenu(){
    var navLinks = document.getElementById('nav-items');
    if (flag){
        navLinks.style.display = "flex";
        flag = false;
    }
    else{
        navLinks.style.display = "none";
        flag = true;
    }
}