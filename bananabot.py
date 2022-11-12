import datetime
import time
import random
import string
from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from announcements import *

# Authentication
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


# Banana Time Variables
announcements = {}
workers = {}
active = False

banana_time_announcement = Announcement(datetime.time(15, 30, 0), "# @HERE Banana Time!", datetime.time(15, 30, 0))
banana_time_announcement.id = "banana_time"


# Initial announcements
initial_announcements = [
    banana_time_announcement,
    Announcement(datetime.time(10, 0, 0), "Banana time is at 15:30 today!", datetime.time(15, 30, 0)),
    MinsBeforeAnnouncement(60, "Banana time is in 60 minutes!", datetime.time(15, 30, 0)),
    MinsBeforeAnnouncement(30, "Banana time is in 30 minutes!", datetime.time(15, 30, 0)),
    MinsBeforeAnnouncement(10, "Banana time is in 10 minutes!", datetime.time(15, 30, 0))
]

for announcement in initial_announcements:
    announcements[announcement.id] = announcement


# Banana Time Functions
def get_banana_time():
    return announcements['banana_time'].time

def start():
    for key in announcements:
        if isinstance(announcements[key], MinsBeforeAnnouncement):
            worker = MinsBeforeAnnouncementWorker(announcements[key].id, announcements[key].mins_before, announcements[key].text, announcements[key].banana_time)
            workers[worker.id] = worker
            workers[worker.id].start()
        else:
            worker = AnnouncementWorker(announcements[key].id, announcements[key].time, announcements[key].text, announcements[key].banana_time)
            workers[worker.id] = worker
            workers[worker.id].start()


def stop():
    for key in workers:
        workers[key].terminate()
    
    globals()['workers'] = {}

def update():
    if active:
        stop()
        start()

def string_to_time(new_time):
    t = time.strptime(new_time, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)

def set_banana_time(time):
    app.logger.debug("Requested banana time " + time)
    time = string_to_time(time)
    announcements['banana_time'].time = time
    announcements['banana_time'].banana_time = time
    
    # Update all the announcements
    for key in announcements:
        announcements[key].banana_time = get_banana_time()
            
    app.logger.info("New banana time set at " + str(get_banana_time()))

    update()

def set_banana_time_text(text):
    announcements['banana_time'].text = text

    if active:
        workers['banana_time'].text = text

def add_announcement(time, text):
    new_announcement = Announcement(string_to_time(time), text, get_banana_time())
    announcements[new_announcement.id] = new_announcement

    if active:
        worker = AnnouncementWorker(new_announcement.id, new_announcement.time, new_announcement.text, new_announcement.banana_time)
        workers[worker.id] = worker
        workers[worker.id].start()

def add_mins_before_announcement(mins_before, text):
    mins_before = int(mins_before)

    new_announcement = MinsBeforeAnnouncement(mins_before, text, get_banana_time())
    announcements[new_announcement.id] = new_announcement

    app.logger.info("Added new announcement " + str(mins_before) + " minutes before banana time")

    if active:
        worker = MinsBeforeAnnouncementWorker(new_announcement.id, new_announcement.mins_before, new_announcement.text, new_announcement.banana_time)
        workers[worker.id] = worker
        workers[worker.id].start()

def remove_announcement(id):
    if id == 'banana_time':
        app.logger.warn("Attempted to remove banana_time announcement. This action is not permitted")
        return

    id = int(id)
    announcements.pop(id)

    if active:
        workers[id].terminate()
        workers.pop(id)

    app.logger.info("Removed announcement with ID: " + str(id))

def toggle_status():
    if not globals()['active']:
        globals()['active'] = True
        start()
        app.logger.info("BananaBot is now Active")
    else:
        globals()['active'] = False
        stop()
        app.logger.info("BananaBot is now Inactive")


# Flask Routes
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',
        banana_time = get_banana_time().strftime("%H:%M"),
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
        app.logger.debug("Form ID: " + str(form_id))

        if form_id == 'status':
            toggle_status()
        elif form_id == 'set_banana_time':
            set_banana_time(request.form['banana_time'])
        elif form_id == 'set_banana_time_text':
            set_banana_time_text(request.form['text'])
        elif form_id == 'remove_announcement':
            remove_announcement(request.form['announcement_id'])
        elif form_id == 'add_announcement':
            add_announcement(request.form['time'], request.form['text'])
        elif form_id == 'add_mins_before_announcement':
            add_mins_before_announcement(request.form['mins_before'], request.form['text'])

        return redirect(url_for('admin'))

    return render_template('admin.html',
        announcements = announcements,
        status = active)


# Main
if __name__ == "__main__":
    print("Admin Password: " + pw)
    app.run(host='0.0.0.0', port='8000', debug=True, use_reloader=False)