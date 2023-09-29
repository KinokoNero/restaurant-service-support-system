document.addEventListener('DOMContentLoaded', function() {
    const addItemButton = document.getElementById('add-item-button');
    if(addItemButton != null) {
        addItemButton.addEventListener('click', function() {
            window.location.href = '/db/add-item';
        });
    }

    const tableManagerButton = document.getElementById('table-manager-button');
    if(tableManagerButton != null) {
        tableManagerButton.addEventListener('click', function() {
            window.location.href = '/db/table-manager';
        });
    }

    const addTableButton = document.getElementById('add-table-button');
    if(addTableButton != null) {
        addTableButton.addEventListener('click', function() {
            window.location.href = '/db/add-table';
        });
    }

    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', handleDeleteButtonClick);
    });
});

function handleDeleteButtonClick(event) {
    console.log("button clicked");
    const button = event.target;
    const confirmation = confirm('Are you sure you want to delete this item?');

    if(confirmation) {
        const form = button.parentNode.querySelector('form');
        form.submit();
    }
    else {
        event.preventDefault();
    }
}