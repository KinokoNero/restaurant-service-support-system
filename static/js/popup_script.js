setTimeout(function() {
    var alerts = document.querySelectorAll('[class*="alert"]');
    alerts.forEach(function(alert) {
        new bootstrap.Alert(alert).close();
    });
}, 5000);