$(document).ready(function(){
    $('.sidebar-option').click(function(e) {
        // Extract which sidebar option was clicked
        const clickedSidebarOption = $(this).attr('id');

        // Update the sidebar
        setSidebarSelected(clickedSidebarOption);

        // Set main content div to loading
        document.getElementById("main-content").innerHTML = "Loading...";

        // Update the main-content and change sidebar option highlight
        switch(clickedSidebarOption) {
            case "sidebar-options":
                showOptions();
                break;
            case "sidebar-banana-time":
                showBananaTimeOptions();
                break;
            case "sidebar-announcements":
                showAnnouncements();
                break;
            case "sidebar-add-announcements":
                showAddAnnouncements();
                break;
        }
    });
});

// AJAX request for the toggle status switch
$(document).on('change', '#status-switch', function() {
    $.ajax({
        type:'POST',
        url:'/toggle-status',

        // Check the updated status value
        success: function (data, status, xhr) {
            if (data == true) {
                document.getElementById('status-switch').setAttribute("checked", "");
                alert("Success: BananaBot is now ACTIVE");
            } else if (data == false) {
                document.getElementById('status-switch').removeAttribute("checked");
                alert("Success: BananaBot is now INACTIVE");
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
$(document).on('change', '.day-selector-checkbox', function() {
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
            daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

            daysOfWeek.forEach(day => {
                if (data[day]) {
                    document.getElementById(`${day}-checkbox`).setAttribute('checked', '');
                } else {
                    document.getElementById(`${day}-checkbox`).removeAttribute('checked');
                }
            });
        },

        // Create a popup if the server returns an error
        error: function (jqXhr, textStatus, errorMessage) {
            alert("Error: Operation failed - Check the logs for more information");
            location.reload();
        }
    });
});

// AJAX request for sending an instant message
$(document).on('submit', '#instant-announcement-form', function(e) {
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
            alert("Success: Your message was sent");
        },

        // Create a popup if the server returns an error
        error: function (jqXhr, textStatus, errorMessage) {
            alert("Error: Operation failed - Check the logs for more information");
            location.reload();
        }
    });
});

// AJAX request for adding a time announcement
$(document).on('submit', '#time-announcement-form', function(e) {
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
            // Reset the form and alert user
            document.getElementById("time-input").value = "";
            document.getElementById("time-input-text").value = "";
            alert("Success: New announcement added");
        },

        // Create a popup if the server returns an error
        error: function (jqXhr, textStatus, errorMessage) {
            alert("Error: Operation failed - Check the logs for more information");
            location.reload();
        }
    });
});

// AJAX request for adding a mins_before announcement
$(document).on('submit', '#mins-before-announcement-form', function(e) {
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
            // Reset the form and alert the user
            document.getElementById("mins-before-input").value = "";
            document.getElementById("mins-before-text-input").value = "";
            alert("Success: New announcement added");
        },

        // Create a popup if the server returns an error
        error: function (jqXhr, textStatus, errorMessage) {
            alert("Error: Operation failed - Check the logs for more information");
            location.reload();
        }
    });
});

// AJAX request for setting banana time
$(document).on('submit', '#banana-time-form', function(e) {
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
            alert("Success: Banana Time is now " + formatTime(data));
        },

        // Create a popup if the server returns an error
        error: function (jqXhr, textStatus, errorMessage) {
            alert("Error: Operation failed - Check the logs for more information");
            location.reload();
        }
    });
});

// AJAX request for setting the banana time text
$(document).on('submit', '#banana-time-text-form', function(e) {
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
            alert(`Success: Banana Time message is now '${data}'`);
        },

        // Create a popup if the server returns an error
        error: function (jqXhr, textStatus, errorMessage) {
            alert("Error: Operation failed - Check the logs for more information");
            location.reload();
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
 * Format a time string from HH:MM:SS to HH:MM
 * 
 * @param {String} time The time to be formatted. Must be in the format HH:MM:SS
 * @return {String} Returns a time string formatted as "HH:MM"
 */
function formatTime(time) {
    // time is in the format HH:MM:SS as a string
    const splitTime = time.split(":");
    return splitTime[0]+":"+splitTime[1];
}

/**
 * Update the main-content div to show the Options
 */
async function showOptions() {
    // Create the new content div
    let content = document.createElement("div");

    // Get the status
    const status = await getStatus();

    // Get the selected days
    const selectedDays = await getSelectedDays();

    // Add the content
    content.innerHTML = `
        <div class="container">
            <br>
            <h3>Status</h3>
            <p><i>Toggles BananaBot on and off (dictates whether it will send messages)</i></p>
            <form class="form-switch form-check" method="POST" id="status-form">
                <label class="form-label">Active</label>
                <input class="form-check-input" id="status-switch" name="status" type="checkbox" role="switch" ${status ? 'checked' : ''}>
            </form>

            <hr>

            <h3>Day Selector</h3>
            <p><i>Choose which days BananaBot will send messages</i></p>
            <div class="row">
                <form method="POST" id="day-selector-form">
                    <div class="btn-group">
                        <input type="checkbox" name="monday" class="btn-check day-selector-checkbox" id="monday-checkbox" ${selectedDays.monday ? 'checked' : ''}>
                        <label class="btn btn-outline-primary" for="monday-checkbox">Monday</label>

                        <input type="checkbox" name="tuesday" class="btn-check day-selector-checkbox" id="tuesday-checkbox" ${selectedDays.tuesday ? 'checked' : ''}>
                        <label class="btn btn-outline-primary" for="tuesday-checkbox">Tuesday</label>

                        <input type="checkbox" name="wednesday" class="btn-check day-selector-checkbox" id="wednesday-checkbox" ${selectedDays.wednesday ? 'checked' : ''}>
                        <label class="btn btn-outline-primary" for="wednesday-checkbox">Wednesday</label>

                        <input type="checkbox" name="thursday" class="btn-check day-selector-checkbox" id="thursday-checkbox" ${selectedDays.thursday ? 'checked' : ''}>
                        <label class="btn btn-outline-primary" for="thursday-checkbox">Thursday</label>

                        <input type="checkbox" name="friday" class="btn-check day-selector-checkbox" id="friday-checkbox" ${selectedDays.friday ? 'checked' : ''}>
                        <label class="btn btn-outline-primary" for="friday-checkbox">Friday</label>

                        <input type="checkbox" name="saturday" class="btn-check day-selector-checkbox" id="saturday-checkbox" ${selectedDays.saturday ? 'checked' : ''}>
                        <label class="btn btn-outline-primary" for="saturday-checkbox">Saturday</label>

                        <input type="checkbox" name="sunday" class="btn-check day-selector-checkbox" id="sunday-checkbox" ${selectedDays.sunday ? 'checked' : ''}>
                        <label class="btn btn-outline-primary" for="sunday-checkbox">Sunday</label>
                    </div>
                </form>
            </div>
        </div>
    `;

    // Get the main content div and update it with the new content
    const mainContent = document.getElementById("main-content");
    mainContent.innerHTML = '';
    mainContent.appendChild(content);
}


/**
 * Gets the current status of BananaBot
 * @return {Boolean} Returns true or false depending on the status of BananaBot
 */
async function getStatus() {
    // Fetch the current status
    const response = await fetch('/status');
    const status = await response.json();

    return status;
}


/**
 * Gets the selected days from BananaBot
 * @return {Object} Returns an array of the selected days
 */
async function getSelectedDays() {
    const response = await fetch('/selected-days');
    const selectedDays = await response.json();

    return selectedDays;
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
 * Sets what is selected on the sidebar
 * 
 * @param {String} selected The ID of the sidebar option to be selected
 */
function setSidebarSelected(selected) {
    // Deselect all
    document.getElementById("sidebar-options").classList.remove('active');
    document.getElementById("sidebar-banana-time").classList.remove('active');
    document.getElementById("sidebar-announcements").classList.remove('active');
    document.getElementById("sidebar-add-announcements").classList.remove('active');

    // Select the requested element
    document.getElementById(selected).classList.add('active');
}

/**
 * Get Banana Time from the server
 * @return {String} Banana Time in the format "HH:MM"
 */
async function getBananaTime() {
    const response = await fetch('/banana-time');
    const timeString = await response.json();
    return formatTime(timeString);
}

/**
 * Get Banana Text from the server
 * @return {String} The Banana Time text as a string
 */
async function getBananaText() {
    const response = await fetch('/banana-text');
    const text = await response.json();
    return text;
}

/**
 * Update the main-content div to show the Announcements table
 */
async function showAnnouncements() {
    // Create the new content div
    let content = document.createElement("div");
    content.classList.add("container");

    // Get current announcements
    const announcements = await getAnnouncements();

    // Generate the announcements table
    let announcementTable = `
        <table class="table" id="announcement-table">
        <tr>
            <th>Time</th>
            <th>Message</th>
            <th></th>
        </tr>
    `;

    Object.keys(announcements).forEach(function(key) {
        const value = announcements[key];

        // Check if announcement is a Minutes Before Announcement
        if (value.type == "mins_before") {
            announcementTable += `
                <tr id="announcement-id-${value.id}">
                    <input type="hidden" name="announcement_id" value="${value.id}">
                    <td>${value.mins_before} minutes before banana time</td>
                    <td>${value.text}</td>
                    <td title="Remove announcement"><button id="${value.id}" class="btn btn-danger remove-announcement-button">Remove</button></td>
                </tr>
            `;
        } else {
            announcementTable += `
                <tr id="announcement-id-${value.id}" class="remove-announcement-form">
                    <input type="hidden" name="announcement_id" value="${value.id }">
                    <td>${formatTime(value.time)}</td>
                    <td>${value.text}</td>
                    <td title="${value.id === 'banana_time' ? 'Cannot remove banana time announcement' : 'Remove announcement'}">
                        <button ${value.id !== 'banana_time' ? `id="${value.id}"` : ''} class="${value.id !== 'banana_time' ? 'btn btn-danger remove-announcement-button' : 'btn btn-secondary'}" ${value.id === 'banana_time' ? 'disabled' : ''}>Remove</button>
                    </td>                    
                </tr>
            `;
        }
    });

    // Add the table to content
    content.innerHTML = `
        <br>
        <h3>Scheduled Announcements</h3>
        <p><i>Shows all currently scheduled announcements</i></p>
        ${announcementTable}
        </table>
    `;

    // Get the main content div and update it with the new content
    const mainContent = document.getElementById("main-content");
    mainContent.innerHTML = '';
    mainContent.appendChild(content);
}


/**
 * Gets the announcements from the server
 */
async function getAnnouncements() {
    const response = await fetch('/announcements');
    const announcements = await response.json();
    return announcements;
}

/**
 * Update the main-content div to show the add announcements forms
 */
async function showAddAnnouncements() {
    // Create the new content div
    let content = document.createElement("div");
    content.classList.add("container");

    // Set new HTML content
    content.innerHTML = `
        <br>
        <div class="row">
            <h3>Instant Message</h3>
            <p><i>Instantly send a message as BananaBot</i></p>
            <form method="POST" class="row" id="instant-announcement-form">
                <input type="hidden" name="type" value="instant">
                <div class="col">
                    <input class="form-control" id="instant-message-input" type="text" name="text" required>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary">Send</button>
                </div>
            </form>
        </div>

        <hr>

        <div class="row">
            <h3>Time Announcement</h3>
            <p><i>Add a time announcement that will send a message at a set time</i></p>
            <form method="POST" class="row" id="time-announcement-form">
                <input type="hidden" name="type" value="time">
                <div class="col-sm-auto ">
                    <label for="" class="form-label">Time</label>
                    <input class="form-control" id="time-input" type="time" name="time">
                </div>
                <div class="mb-3">
                    <label for="" class="form-label">Announcement Message</label>
                    <input class="form-control" id="time-input-text" type="text" name="text" required></textarea>
                </div>
                <div class="mb-3">
                    <button class="btn btn-primary">Add</button>
                </div>
            </form>
        </div>

        <hr>

        <div class="row">
            <h3>Minutes Before Announcement</h3>
            <p><i>Add a minutes before announcement that will send a message X minutes before Banana Time (Note: The time the message is sent will change depending on Banana Time)</i></p>
            <form method="POST" class="row" id="mins-before-announcement-form">
                <input type="hidden" name="type" value="mins_before">
                <div class="col-sm-auto ">
                    <label for="" class="form-label">Minutes Before</label>
                    <input class="form-control" id="mins-before-input" type="number" name="mins_before" min="1" max="1440" step="1" required>
                </div>
                <div class="mb-3">
                    <label for="" class="form-label">Announcement Message</label>
                    <input class="form-control" id="mins-before-text-input" type="text" name="text" required>
                </div>
                <div class="mb-3">
                    <button class="btn btn-primary">Add</button>
                </div>
            </form>
        </div>
    `;

    // Get the main content div and update it with the new content
    const mainContent = document.getElementById("main-content");
    mainContent.innerHTML = '';
    mainContent.appendChild(content);
}