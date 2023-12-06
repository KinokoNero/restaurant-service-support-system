document.addEventListener("DOMContentLoaded", function() {
    restoreScrollPosition();
});

const scrollDelay = 50; //ms

function saveScrollPosition() {
    localStorage.setItem('scrollPositionX', window.scrollX);
    localStorage.setItem('scrollPositionY', window.scrollY);
}

function restoreScrollPosition() {
    var scrollPositionX = localStorage.getItem('scrollPositionX');
    var scrollPositionY = localStorage.getItem('scrollPositionY');
    if (scrollPositionX !== null && scrollPositionY !== null) {
        setTimeout(function () {
            window.scrollTo(parseInt(scrollPositionX), parseInt(scrollPositionY));
        }, scrollDelay);
        localStorage.removeItem('scrollPositionX');
        localStorage.removeItem('scrollPositionY');
    }
}