document.addEventListener('DOMContentLoaded', function() {
    const addItemButton = document.getElementById('add-item-button');
    if(addItemButton != null) {
        addItemButton.addEventListener('click', function() {
            window.location.href = '/db/add-item';
        });
    }

    const modifyItemButtons = document.querySelectorAll('.modify-item-button');
    if(modifyItemButtons != null) {
        modifyItemButtons.forEach(button => {
            const itemId = button.getAttribute('item-id');
            button.addEventListener('click', function() {
                window.location.href = `/db/modify-item/${itemId}`;
            });
        });
    }

    const orderManagerButton = document.getElementById('order-manager-button');
    if(orderManagerButton != null) {
        orderManagerButton.addEventListener('click', function() {
            window.location.href = '/order-manager';
        });
    }

    const tableManagerButton = document.getElementById('table-manager-button');
    if(tableManagerButton != null) {
        tableManagerButton.addEventListener('click', function() {
            window.location.href = '/table-manager';
        });
    }

    const addTableButton = document.getElementById('add-table-button');
    if(addTableButton != null) {
        addTableButton.addEventListener('click', function() {
            window.location.href = '/db/add-table';
        });
    }

    const modifyTableButtons = document.querySelectorAll('.modify-table-button');
    if(modifyTableButtons != null) {
        modifyTableButtons.forEach(button => {
            const tableId = button.getAttribute('table-id');
            button.addEventListener('click', function() {
                window.location.href = `/db/modify-table/${tableId}`;
            });
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