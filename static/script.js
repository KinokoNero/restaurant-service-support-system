document.addEventListener('DOMContentLoaded', function() {
    const addItemButton = document.getElementById('add-item-button');

    addItemButton.addEventListener('click', function() {
        window.location.href = '/add-item';
    });
});