document.addEventListener("DOMContentLoaded", function() {
    const serviceRequestTypeDropdown = document.getElementById('request-type');
    const customInfoLabel = document.getElementById('custom-info-label');
    const customInfoTextarea = document.getElementById('custom-info');

    serviceRequestTypeDropdown.addEventListener('change', function() {
        const selectedValue = this.value;
        if (selectedValue === 'custom') {
            customInfoLabel.style.display = 'block';
            customInfoTextarea.style.display = 'block';
            customInfoTextarea.disabled = false;
        }
        else {
            customInfoLabel.style.display = 'none';
            customInfoTextarea.style.display = 'none';
            customInfoTextarea.disabled = true;
        }
    });
});