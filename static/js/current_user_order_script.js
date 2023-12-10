document.addEventListener('DOMContentLoaded', function() {
    var itemCountForms = document.getElementsByClassName('item-count-form');
    var additionalInfoForms = document.getElementsByClassName('additional-info-form');
    var itemCountInputs = document.getElementsByClassName('item-count');
    var additionalInfoTextAreas = document.getElementsByClassName('additional-info');

    for (var i = 0; i < itemCountInputs.length; i++) {
        itemCountInputs[i].addEventListener('change', function() {
            var itemCountInput = event.target;
            var closestForm = itemCountInput.closest('form');
            itemCountInput.value = Math.max(1, Math.round(Number(itemCountInput.value)));
            saveScrollPosition();
            closestForm.submit();
        });
    }

    for (var i = 0; i < additionalInfoTextAreas.length; i++) {
        additionalInfoTextAreas[i].addEventListener('change', function() {
            var additionalInfoTextarea = event.target;
            var closestForm = additionalInfoTextarea.closest('form');
            saveScrollPosition();
            closestForm.submit();
        });
    }
});