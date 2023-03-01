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

    // AJAX request for sending an instant message
    $('#instant-announcement-form').submit(function(e) {
        e.preventDefault(); // avoid to execute the actual submit of the form

        const formElement = document.querySelector("#instant-announcement-form");
        const formData = getFormJSON(formElement);

        $.ajax({
            type:'POST',
            url:'/announcements',
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            traditional: true,

            // Let the admin know their message was sent and reset the form
            success: function (data, status, xhr) {
                document.getElementById("instant-message-input").value = "";
                alert("Your message was sent");
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
                location.reload();
            }
        });
    });

    // AJAX request for adding a time announcement
    $('#time-announcement-form').submit(function(e) {
        e.preventDefault(); // avoid to execute the actual submit of the form

        const formElement = document.querySelector("#time-announcement-form");
        const formData = getFormJSON(formElement);

        $.ajax({
            type:'POST',
            url:'/announcements',
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            traditional: true,

            success: function (data, status, xhr) {
                // Update the announcements table
                addTimeAnnouncement(data.id, data.time, data.text);

                // Reset the form
                document.getElementById("time-input").value = "";
                document.getElementById("time-input-text").value = "";
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
                location.reload();
            }
        });
    });

    // AJAX request for adding a mins_before announcement
    $('#mins-before-announcement-form').submit(function(e) {
        e.preventDefault(); // avoid to execute the actual submit of the form

        const formElement = document.querySelector("#mins-before-announcement-form");
        const formData = getFormJSON(formElement);

        $.ajax({
            type:'POST',
            url:'/announcements',
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            traditional: true,

            success: function (data, status, xhr) {
                // Update the announcements table
                addMinsBeforeAnnouncement(data.id, data.mins_before, data.text);

                // Reset the form
                document.getElementById("mins-before-input").value = "";
                document.getElementById("mins-before-text-input").value = "";
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
                location.reload();
            }
        });
    });
});

// AJAX request for deleting announcements
$(document).on('click', '.remove-announcement-button', function() {
    const id = this.id;

    $.ajax({
        type:'DELETE',
        url:'/announcements/' + id,

        // Remove the announcement from the table
        success: function (data, status, xhr) {
            document.getElementById("announcement-id-"+id).remove();
        },

        // Create a popup if the server returns an error
        error: function (jqXhr, textStatus, errorMessage) {
            alert("Error: Operation failed - Check the logs for more information");
            location.reload();
        }
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

/**
 * Add a time announcement to the announcements table
 * 
 * @param {String} id The id of the announcement
 * @param {String} time The announcement time in the format HH:MM:SS 
 * @param {String} text The announcement text
 */
function addTimeAnnouncement(id, time, text) {
    // Update the table
    $("#announcement-table").append($(`<tr id="announcement-id-${id}"> \
        <input type="hidden" name="announcement_id" value="${id}"> \
        <td>${formatTime(time)}</td> \
        <td>${text}</td> \
        <td title="Remove announcement"><button id="${id}" class="btn btn-danger remove-announcement-button">Remove</button></td> \
    </tr>`));
}

/**
 * Add a mins_before announcement to the announcements table
 * 
 * @param {String} id The id of the announcement
 * @param {int} minsBefore The number of minutes before banana time the announcement will trigger 
 * @param {String} text The announcement text
 */
function addMinsBeforeAnnouncement(id, minsBefore, text) {
    // Update the table
    $("#announcement-table").append($(`<tr id="announcement-id-${id}"> \
            <input type="hidden" name="announcement_id" value="${id}"> \
            <td>${minsBefore} minutes before banana time</td> \
            <td>${text}</td> \
            <td title="Remove announcement"><button id="${id}" class="btn btn-danger remove-announcement-button">Remove</button></td> \
    </tr>`));
}

/**
 * Format a time string from HH:MM:SS to HH:MM
 * 
 * @param {String} time The time to be formatted. Must be in the format HH:MM:SS
 */
function formatTime(time) {
    // time is in the format HH:MM:SS as a string
    const splitTime = time.split(":");
    return splitTime[0]+":"+splitTime[1];
}