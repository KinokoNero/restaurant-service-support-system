document.addEventListener('DOMContentLoaded', function() {
    var itemCountForms = document.getElementsByClassName('item-count-form');
    var additionalInfoForms = document.getElementsByClassName('additional-info-form');
    var itemCountInputs = document.getElementsByClassName('item-count');
    var additionalInfoTextAreas = document.getElementsByClassName('additional-info');
    var submitOrderButton = document.getElementById('submit-order-button');

    for (var i = 0; i < itemCountInputs.length; i++) {
        itemCountInputs[i].addEventListener('change', function() {
            var itemCountInput = event.target;
            var closestForm = itemCountInput.closest('form');
            itemCountInput.value = Math.max(1, Math.round(Number(itemCountInput.value)));
            saveScrollPosition();
            closestForm.submit();
        });

        itemCountInputs[i].addEventListener('focus', function() {
            submitOrderButton.disabled = true;
        });

        itemCountInputs[i].addEventListener('blur', function() {
            submitOrderButton.disabled = false;
        });
    }

    for (var i = 0; i < additionalInfoTextAreas.length; i++) {
        additionalInfoTextAreas[i].addEventListener('change', function() {
            var additionalInfoTextarea = event.target;
            var closestForm = additionalInfoTextarea.closest('form');
            saveScrollPosition();
            closestForm.submit();
        });

        additionalInfoTextAreas[i].addEventListener('focus', function() {
            submitOrderButton.disabled = true;
        });

        additionalInfoTextAreas[i].addEventListener('blur', function() {
            submitOrderButton.disabled = false;
        });
    }
});