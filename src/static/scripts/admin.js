$(document).ready(function(){
    // AJAX request for the toggle status switch
    $('.status-switch').change(function() {
        $.ajax({
            type:'POST',
            url:'/toggle-status',

            // Check the updated status value
            success: function (data, status, xhr) {
                if (data == true) {
                    document.getElementById('status-switch').setAttribute("checked", "");
                    alert("BananaBot is now ACTIVE");
                } else if (data == false) {
                    document.getElementById('status-switch').removeAttribute("checked");
                    alert("BananaBot is now INACTIVE");
                }
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
                location.reload();
            }
        });
    });

    // AJAX request for updating selected days
    $('.day-selector-checkbox').change(function() {
        var formData = $('#day-selector-form').serialize();
        
        console.log("Form Data:");
        console.log(formData);

        $.ajax({
            type:'POST',
            url:'/selected-days',
            data: formData,
            dataType: 'json',
        });
    });
});