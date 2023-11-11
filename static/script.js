document.addEventListener("DOMContentLoaded", function () {
    var textareas = document.querySelectorAll('[id^="additional-info-"]');

    textareas.forEach(function(textarea) {
        textarea.addEventListener("input", function() {
            var index = textarea.id.split('-').pop();
            var newValue = textarea.value;

            var url = `{{ url_for('session_routes.update_order_item', item_index=${index}) }}`;
            var data = {
                additional_info: newValue
            };

            //TODO: pass the new value to the update function
            /*fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });*/
        });
    });
});