$(document).ready(function(){
    // AJAX request for the toggle status switch
    $('#status-switch').change(function() {
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

    // AJAX request for setting banana time
    $('#banana-time-form').submit(function(e) {
        e.preventDefault(); // avoid to execute the actual submit of the form

        const formElement = document.querySelector("#banana-time-form");
        const formData = getFormJSON(formElement);

        $.ajax({
            type:'POST',
            url:'/banana-time',
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            traditional: true,

            // Update the form with the new time
            success: function (data, status, xhr) {
                document.getElementById("banana-time-input").value = formatTime(data);
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
                location.reload();
            }
        });
    });

    // AJAX request for setting the banana time text
    $('#banana-time-text-form').submit(function(e) {
        e.preventDefault(); // avoid to execute the actual submit of the form

        const formElement = document.querySelector("#banana-time-text-form");
        const formData = getFormJSON(formElement);

        $.ajax({
            type:'POST',
            url:'/banana-text',
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            traditional: true,

            // Update the form with the new text
            success: function (data, status, xhr) {
                document.getElementById("banana-time-text-input").value = data;
            },

            // Create a popup if the server returns an error
            error: function (jqXhr, textStatus, errorMessage) {
                alert("Error: Operation failed - Check the logs for more information");
                location.reload();
            }
        });
    });

    $('.sidebar-option').click(function(e) {
        // Extract which sidebar option was clicked
        const clickedSidebarOption = $(this).attr('id');
        console.log(clickedSidebarOption);

        // Update the main-content and change sidebar option highlight
        switch(clickedSidebarOption) {
            case "sidebar-options":
                console.log("Clicked sidebar options");
                showOptions();
                break;
            case "sidebar-banana-time":
                console.log("Clicked sidebar banana time");
                showBananaTimeOptions();
                break;
        }
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

/**
 * Update the main-content div to show the Options
 */
function showOptions() {
    const mainContent = document.getElementById("main-content");

    // Create element (div with class container)

    // Add the content
    mainContent.innerHTML = `
        <div class="container">
            <br>
            <h3>Status</h3>
            <p><i>Toggles BananaBot on and off (dictates whether it will send messages)</i></p>
            <form class="form-switch form-check" method="POST" id="status-form">
                <label class="form-label">Active</label>
                <input class="form-check-input" id="status-switch" name="status" type="checkbox" role="switch" checked>
            </form>

            <hr>

            <h3>Day Selector</h3>
            <p><i>Choose which days BananaBot will send messages</i></p>
            <div class="row">
                <form method="POST" id="day-selector-form">
                    <div class="btn-group">
                        <input type="checkbox" name="monday" class="btn-check day-selector-checkbox" id="monday-checkbox" checked>
                        <label class="btn btn-outline-primary" for="monday-checkbox">Monday</label>

                        <input type="checkbox" name="tuesday" class="btn-check day-selector-checkbox" id="tuesday-checkbox" checked>
                        <label class="btn btn-outline-primary" for="tuesday-checkbox">Tuesday</label>

                        <input type="checkbox" name="wednesday" class="btn-check day-selector-checkbox" id="wednesday-checkbox" checked>
                        <label class="btn btn-outline-primary" for="wednesday-checkbox">Wednesday</label>

                        <input type="checkbox" name="thursday" class="btn-check day-selector-checkbox" id="thursday-checkbox" checked>
                        <label class="btn btn-outline-primary" for="thursday-checkbox">Thursday</label>

                        <input type="checkbox" name="friday" class="btn-check day-selector-checkbox" id="friday-checkbox" checked>
                        <label class="btn btn-outline-primary" for="friday-checkbox">Friday</label>

                        <input type="checkbox" name="saturday" class="btn-check day-selector-checkbox" id="saturday-checkbox" checked>
                        <label class="btn btn-outline-primary" for="saturday-checkbox">Saturday</label>

                        <input type="checkbox" name="sunday" class="btn-check day-selector-checkbox" id="sunday-checkbox" checked>
                        <label class="btn btn-outline-primary" for="sunday-checkbox">Sunday</label>
                    </div>
                </form>
            </div>
        </div>
    `;

    // Set attributes accordingly
    $.ajax({
        type:'GET',
        url:'/selected-days',
        // contentType: "application/json; charset=utf-8",
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
    })

    // Update main-content div
}

/**
 * Update the main-content div to show the Banana Time Options
 */
async function showBananaTimeOptions() {
    // Create the new content div
    let content = document.createElement("div");
    content.classList.add("container");

    // Get Banana Time
    const bananaTime = await getBananaTime();

    // Get Banana Message
    const bananaMessage = await getBananaText();

    // Set new HTML content
    content.innerHTML = `
        <br>
        <form class="row" method="POST" id="banana-time-form">
            <h3 for="" class="form-label">Banana Time</h3>
            <p><i>Sets Banana Time (Note: Any minutes before announcements are based on this time)</i></p>
            <div class="col-auto">
                <input id="banana-time-input" class="form-control" type="time" name="time" value="${bananaTime}">
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">Set</button>
            </div>
        </form>
        <hr>
        <form class="row" method="POST" id="banana-time-text-form">
            <h3 for="" class="form-label">Message</h3>
            <p><i>Sets the message BananaBot will send at Banana Time</i></p>
            <div class="col">
                <input id="banana-time-text-input" class="form-control" type="text" name="text" value="${bananaMessage}" required></input>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">Set</button>
            </div>
        </form>
    `;

    // Get the main content div and update it with the new content
    const mainContent = document.getElementById("main-content");
    mainContent.innerHTML = '';
    mainContent.appendChild(content);
}

/**
 * Get Banana Time from the server
 */
async function getBananaTime() {
    const response = await fetch('/banana-time');
    const timeString = await response.json();
    return formatTime(timeString);
}

/**
 * Get Banana Text from the server
 */
async function getBananaText() {
    const response = await fetch('/banana-text');
    const text = await response.json();
    console.log("Mesage: ", text);
    return text;
}

function showAnnouncements() {

}