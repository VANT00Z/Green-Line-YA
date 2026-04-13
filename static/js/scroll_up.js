window.onscroll = function () {
    let scrollUp = document.getElementById('scrollUp');
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollUp.style.display = "block";
    } else {
        scrollUp.style.display = "none";
    }
};
