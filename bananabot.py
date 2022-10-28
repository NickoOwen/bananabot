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
workers = []
active = False

timeAnnouncements = {
    "morningAnnouncement": TimeAnnouncement(datetime.time(10, 0, 0), "Banana Time is at 15:30 today!"),
    "bananaTime": TimeAnnouncement(datetime.time(15, 30, 0), "Banana Time!")
}

minsBeforeAnnouncements = {
    60: MinsBeforeAnnouncement(60, "60 Minutes until Banana Time!"),
    30: MinsBeforeAnnouncement(30, "30 Minutes until Banana Time!"),
    10: MinsBeforeAnnouncement(10, "10 Minutes until Banana Time!")
}


# Banana Time Functions
def start():
    for announcement in timeAnnouncements.values():
        worker = TimeAnnouncementWorker(announcement.time, announcement.text)
        worker.start()
        workers.append(worker)
    
    for announcement in minsBeforeAnnouncements.values():
        worker = MinsBeforeAnnouncementWorker(announcement.minsBefore, announcement.text, timeAnnouncements['bananaTime'].time)
        worker.start()
        workers.append(worker)

def stop():
    for worker in workers:
        worker.terminate()
    
    globals()['workers'] = []

def update():
    if active:
        stop()
        start()

def stringToTime(newTime):
    t = time.strptime(newTime, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)

def setBananaTime(time):
    app.logger.debug("Requested banana time " + time)
    timeAnnouncements['bananaTime'].time = stringToTime(time)
    app.logger.info("New banana time set at " + str(timeAnnouncements['bananaTime'].time))

    update()

def setMorningAnnouncementTime(time):
    timeAnnouncements['morningAnnouncement'].time = stringToTime(time)
    update() # TODO have this just restart the morning announcement worker

def addMinsBeforeAnnouncement(minsBefore, text):
    mins = int(minsBefore)

    if mins in minsBeforeAnnouncements:
        app.logger.warning("Cannot add new announcement as one already exists for " + str(mins) + " minutes before")
        # TODO Somehow alert the user of this
    else:
        minsBeforeAnnouncements[mins] = MinsBeforeAnnouncement(mins, text)

        if active:
            worker = MinsBeforeAnnouncementWorker(mins, text, timeAnnouncements['bananaTime'].time)
            worker.start()
            workers.append(worker)

        app.logger.info("Added new announcement " + str(mins) + " minutes before banana time")

def removeMinsBeforeAnnouncement(minsBefore):
    minsBeforeAnnouncements.pop(int(minsBefore))
    app.logger.info("Removed announcement for " + str(minsBefore) + " minutes before banana time")

def toggleStatus():
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
        timeAnnouncements = timeAnnouncements,
        minsBeforeAnnouncements = minsBeforeAnnouncements,
        status = active)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin', methods=('GET', 'POST'))
@auth.login_required
def admin():
    if request.method == 'POST':
        formId = request.form['formId']
        app.logger.debug("Form ID: " + str(formId))
        if formId == 'bananaTime':
            setBananaTime(request.form['bananaTime'])
        elif formId == 'morningAnnouncementTime':
            setMorningAnnouncementTime(request.form['morningAnnouncementTime'])
        elif formId == 'announcement':
            addMinsBeforeAnnouncement(request.form['minsBefore'], request.form['message'])
        elif formId == 'deleteAnnouncement':
            removeMinsBeforeAnnouncement(request.form['minsBefore'])
        elif formId == 'status':
            toggleStatus()

        return redirect(url_for('admin'))

    return render_template('admin.html',
        bananaTime = timeAnnouncements['bananaTime'].time.strftime("%H:%M"),
        morningAnnouncementTime = timeAnnouncements['morningAnnouncement'].time.strftime("%H:%M"),
        minsBeforeAnnouncements = minsBeforeAnnouncements,
        status = active)


# Main
if __name__ == "__main__":
    print("Admin Password: " + pw)
    app.run(host='0.0.0.0', port='8000', debug=True, use_reloader=False)