document.addEventListener('DOMContentLoaded', function() {
    var statusForms = document.getElementsByClassName('status-form');
    var includeFinishedServiceRequestsCheckbox = document.getElementById('include-finished-service-requests-checkbox');

    includeFinishedServiceRequestsCheckbox.addEventListener('change', function() {
        var includeFinishedServiceRequestsForm = document.getElementById('include-finished-service-requests-form');
        includeFinishedServiceRequestsForm.submit();
    });

    for (var i = 0; i < statusForms.length; i++) {
        statusForms[i].addEventListener('change', function() {
            var statusForm = event.target;
            var orderIndex = parseInt(statusForm.id.match(/\d+/)[0]);
            var statusForm = statusForm.closest('form');

            saveScrollPosition();

            statusForm.submit();
        });
    }
});