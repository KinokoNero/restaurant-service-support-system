document.addEventListener("DOMContentLoaded", function() {
    var statusForms = document.getElementsByClassName("status-form");

    for (var i = 0; i < statusForms.length; i++) {
        statusForms[i].addEventListener("change", function() {
            var statusForm = event.target;
            var orderIndex = parseInt(statusForm.id.match(/\d+/)[0]);
            var statusForm = statusForm.closest("form");

            saveScrollPosition();

            statusForm.submit();
        });
    }
});