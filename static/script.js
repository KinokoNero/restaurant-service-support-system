document.addEventListener('DOMContentLoaded', function() {
    const addItemButton = document.getElementById('add-item-button');    
    addItemButton.addEventListener('click', function() {
        window.location.href = 'admin/database/add-item';
    });

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