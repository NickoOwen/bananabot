import datetime
import time
import random
import string
from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from announcement import *

#### Authentication ####
auth = HTTPBasicAuth()

user = 'admin'
pw = ''.join(random.choice(string.ascii_letters) for i in range(10))

users = {
    user: generate_password_hash(pw)
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


#### Banana Time Variables ####
announcements = {}  # Stores the announcements
workers = {}        # Stores the workers
active = False      # Stores the current status of the system (i.e. whether bananabot needs to send requests)

# Create the banana time announcement
banana_time_announcement = Announcement(Announcement.banana_time, "# @HERE Banana Time!")
banana_time_announcement.id = "banana_time"

# Create the default announcements
default_announcements = [
    banana_time_announcement,
    Announcement(datetime.time(10, 0, 0), "# Banana time is at 15:30 today!"),
    MinsBeforeAnnouncement(60, "# Banana time is in 60 minutes!"),
    MinsBeforeAnnouncement(30, "# Banana time is in 30 minutes!"),
    MinsBeforeAnnouncement(10, "# Banana time is in 10 minutes!")
]

# Add the default announcements to the announcements dictionary
for announcement in default_announcements:
    announcements[announcement.id] = announcement


#### Banana Time Functions ####
def start():
    """Creates all the workers using the data from announcements. Returns True if successful"""

    if workers:
        app.logger.warning("Found running workers when attempting to create workers. Expected 'workers' to be empty")
        return False

    for key in announcements:
        if isinstance(announcements[key], MinsBeforeAnnouncement):
            worker = MinsBeforeAnnouncementWorker(announcements[key])
            workers[worker.id] = worker
            workers[worker.id].start()
        else:
            worker = AnnouncementWorker(announcements[key])
            workers[worker.id] = worker
            workers[worker.id].start()

    return True

def stop():
    """Terminates all running workers. Returns True if successful"""

    global workers

    # Check if the workers dictionary is empty
    if not workers:
        app.logger.warning("Tried to stop workers when no workers exist")
        return False

    for key in workers:
        workers[key].terminate()
    
    workers = {}
    return True

def update():
    """Terminates and re-creates all workers so they are updated with the latest system changes"""
    
    if active:
        app.logger.debug("Updating workers...")
        stop()
        start()

def string_to_time(new_time):
    """Takes a string as input and returns a datetime.time object"""

    t = time.strptime(new_time, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)

def set_banana_time(time):
    """Sets banana time"""

    app.logger.debug(f"Requested banana time: {time}")
    Announcement.banana_time = string_to_time(time)
    announcements['banana_time'].time = Announcement.banana_time    
    app.logger.info(f"New banana time set at {str(Announcement.banana_time)}")

    # Call update so any running workers can be updated
    update()

def set_banana_time_text(text):
    """Sets the text for the banana time announcement"""

    app.logger.debug(f"Requested banana time text: {text}")
    announcements['banana_time'].text = text

    # Call update so any running workers can be updated
    update()
        
def add_announcement(time, text):
    """Adds a new announcement with the given time and text"""

    app.logger.info(f"Adding new announcement for {time} with message: {text}")
    new_announcement = Announcement(string_to_time(time), text)
    announcements[new_announcement.id] = new_announcement

    if active:
        app.logger.debug(f"Creating worker for new announcement with ID {new_announcement.id}")
        worker = AnnouncementWorker(new_announcement)
        workers[worker.id] = worker
        workers[worker.id].start()

    return new_announcement.id

def add_mins_before_announcement(mins_before, text):
    """Adds a new announcement for the given 'mins_before' banana time with the given text"""

    app.logger.info(f"Adding new announcement for {mins_before} minutes before banana time with message: {text}")
    mins_before = int(mins_before)

    new_announcement = MinsBeforeAnnouncement(mins_before, text)
    announcements[new_announcement.id] = new_announcement

    if active:
        app.logger.debug(f"Creating worker for new announcement with ID {new_announcement.id}")
        worker = MinsBeforeAnnouncementWorker(new_announcement)
        workers[worker.id] = worker
        workers[worker.id].start()

    return new_announcement.id

def instant_message(text):
    """Sends a new message instantly"""

    app.logger.info(f"Sending instant message with message: {text}")
    InstantAnnouncement(text)

def remove_announcement(id):
    """Removes the announcement with the given id. Returns True if successful"""

    if id == 'banana_time':
        app.logger.warning("Attempted to remove banana_time announcement. This action is not permitted")
        return False

    id = int(id)
    announcements.pop(id)

    if active:
        app.logger.info(f"Terminating worker with ID {str(id)}")
        workers[id].terminate()
        workers.pop(id)

    app.logger.info(f"Announcement with ID {str(id)} has been removed")
    return True

def toggle_status():
    """Toggles the status of the system (active). Returns the new value of active"""
    
    global active

    if not active:
        active = True
        start()
        app.logger.info("BananaBot is now ACTIVE")
    else:
        active = False
        stop()
        app.logger.info("BananaBot is now INACTIVE")
    
    return active

def update_selected_days(new_selected_days):
    """Updates the selected_days with new_selected_days"""

    app.logger.info("Updating selected days")

    # Update selected_days
    Announcement.selected_days = new_selected_days
    app.logger.info(f"Updated days: {str(Announcement.selected_days)}")
    
    # Call so any current workers can be updated
    update()


#### Flask Routes ####
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',
        banana_time = Announcement.banana_time.strftime("%H:%M"),
        announcements = announcements,
        status = active)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin', methods=('GET', 'POST'))
@auth.login_required
def admin():
    if request.method == 'POST':
        form_id = request.form['form_id']
        app.logger.debug(f"POST received with form_id: {str(form_id)}")

        match form_id:
            case 'status':
                toggle_status()
            case 'set_banana_time':
                set_banana_time(request.form['banana_time'])
            case 'set_banana_time_text':
                set_banana_time_text(request.form['text'])
            case 'remove_announcement':
                remove_announcement(request.form['announcement_id'])
            case 'add_announcement':
                add_announcement(request.form['time'], request.form['text'])
            case 'instant_message':
                instant_message(request.form['text'])
            case 'add_mins_before_announcement':
                add_mins_before_announcement(request.form['mins_before'], request.form['text'])
            case 'day_selector':
                app.logger.debug(f"Selected days form: {str(request.form)}")
                update_selected_days(dict((day, request.form.get(day, False) == 'on') for day in Announcement.selected_days))
            case _:
                app.logger.error(f"form_id: {form_id} not recognised")

        return redirect(url_for('admin'))

    return render_template('admin.html',
        announcements = announcements,
        status = active,
        selected_days = Announcement.selected_days)


#### Main ####
if __name__ == "__main__":
    print("Admin Password: " + pw)
    del pw

    app.run(host='0.0.0.0', port='8000', debug=True, use_reloader=False)