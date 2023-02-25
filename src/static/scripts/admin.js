$(document).ready(function(){
    // AJAX request for the toggle status switch
    $('.status-switch').change(function() {
        let formData = $('#status-form').serialize();
        console.log('status changed: ', formData);
        $.ajax({
            type:'POST',
            url:'/toggle-status',
            data: formData,
            dataType: 'json',

            // Check the updated status value
            success: function (data, status, xhr) {
                if (data == true) {
                    document.getElementById('status-switch').setAttribute("checked", "");
                } else if (data == false) {
                    document.getElementById('status-switch').removeAttribute("checked");
                }
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
            }
        });
    });

    // $('.day-selector-checkbox').change(function() {
    //     var formData = $('#day-selector-form').serialize();
    //     $.ajax({
    //         type:'POST',
    //         url:'/admin',
    //         data: formData,
    //         dataType: 'json',
    //     });
    // });
});