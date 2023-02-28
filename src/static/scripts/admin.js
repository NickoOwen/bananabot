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
        const formElement = document.querySelector('#day-selector-form');
        const formData = getFormJSON(formElement);

        $.ajax({
            type:'POST',
            url:'/selected-days',
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            traditional: true,

            // Update the buttons with the latest selected_days
            success: function (data, status, xhr) {
                if(data['monday']) {
                    document.getElementById('monday-checkbox').setAttribute("checked", "");
                } else if(data['monday'] == false) {
                    document.getElementById('monday-checkbox').removeAttribute("checked");
                }

                if(data['tuesday']) {
                    document.getElementById('tuesday-checkbox').setAttribute("checked", "");
                } else if(data['tuesday'] == false) {
                    document.getElementById('tuesday-checkbox').removeAttribute("checked");
                }

                if(data['wednesday']) {
                    document.getElementById('wednesday-checkbox').setAttribute("checked", "");
                } else if(data['wednesday'] == false) {
                    document.getElementById('wednesday-checkbox').removeAttribute("checked");
                }

                if(data['thursday']) {
                    document.getElementById('thursday-checkbox').setAttribute("checked", "");
                } else if(data['thursday'] == false) {
                    document.getElementById('thursday-checkbox').removeAttribute("checked");
                }

                if(data['friday']) {
                    document.getElementById('friday-checkbox').setAttribute("checked", "");
                } else if(data['friday'] == false) {
                    document.getElementById('friday-checkbox').removeAttribute("checked");
                }

                if(data['saturday']) {
                    document.getElementById('saturday-checkbox').setAttribute("checked", "");
                } else if(data['saturday'] == false) {
                    document.getElementById('saturday-checkbox').removeAttribute("checked");
                }

                if(data['sunday']) {
                    document.getElementById('sunday-checkbox').setAttribute("checked", "");
                } else if(data['sunday'] == false) {
                    document.getElementById('sunday-checkbox').removeAttribute("checked");
                }
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
                location.reload();
            }
        });
    });
});

/**
 * Creates a json object including fields in the form
 *
 * @param {HTMLElement} form The form element to convert
 * @return {Object} The form data
 */
const getFormJSON = (form) => {
    const data = new FormData(form);
    return Array.from(data.keys()).reduce((result, key) => {
      result[key] = data.get(key);
      return result;
    }, {});
};
