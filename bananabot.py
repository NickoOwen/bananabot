import datetime
import time
import requests
import logging
from multiprocessing import Process
from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# Authentication
auth = HTTPBasicAuth()

user = 'user'
pw = 'password'

users = {
    user: generate_password_hash(pw)
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

# Classes
class MinsBeforeAnnouncement:
    def __init__(self, minsBefore, text):
        self.minsBefore = minsBefore
        self.text = text

class MinsBeforeAnnouncementWorker(Process):
    def __init__(self, minsBefore, text):
        super(MinsBeforeAnnouncementWorker, self).__init__()
        self.minsBefore = minsBefore
        self.text = text

    def run(self):
        while True:
            currentTime = datetime.datetime.now()
            normalisedBananaTime = datetime.datetime.combine(datetime.date.today(), timeAnnouncements['bananaTime'].time)
            time_delta = normalisedBananaTime - currentTime
            announcementTime = normalisedBananaTime - datetime.timedelta(minutes = self.minsBefore)
            
            sleepTime = announcementTime - currentTime
            sleepTimeSeconds = sleepTime.seconds
            print("[" + str(datetime.datetime.now()) + "] DEBUG - Announcement for " + str(self.minsBefore) + " minutes before sleeping for seconds: " + str(sleepTimeSeconds))
            time.sleep(sleepTimeSeconds)

            print(self.text)
            # curl chat app here with self.text

            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work

class TimeAnnouncement:
    def __init__(self, time, text):
        self.time = time
        self.text = text

class TimeAnnouncementWorker(Process):
    def __init__(self, time, text):
        super(TimeAnnouncementWorker, self).__init__()
        self.time = time
        self.text = text

    def run(self):
        while True:
            currentTime = datetime.datetime.now()
            normalisedBananaTime = datetime.datetime.combine(datetime.date.today(), timeAnnouncements['bananaTime'].time)
            
            announcementTime = datetime.datetime.combine(datetime.date.today(), self.time)
            
            sleepTime = announcementTime - currentTime
            sleepTimeSeconds = sleepTime.seconds
            print("[" + str(datetime.datetime.now()) + "] DEBUG Announcement for " + str(self.time) + " sleeping for seconds: " + str(sleepTimeSeconds))
            time.sleep(sleepTimeSeconds + 1) # Offset by 1 second

            print(self.text)
            # curl chat app here with self.text

            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work


# Banana Time Variables
workers = []
status = True # TODO Finish implementing status functionality. Determins whether or not the bot will send announcements

timeAnnouncements = {
    "morningAnnouncement": TimeAnnouncement(datetime.time(10, 0, 0), "Banana Time is at 15:30 today!"),
    "bananaTime": TimeAnnouncement(datetime.time(15, 30, 0), "Banana Time!")
}

minsBeforeAnnouncements = {
    60: MinsBeforeAnnouncement(60, "60 mins test"),
    30: MinsBeforeAnnouncement(30, "30 mins test")
}


# Banana Time Functions
def start():
    for announcement in timeAnnouncements.values():
        worker = TimeAnnouncementWorker(announcement.time, announcement.text)
        worker.start()
        workers.append(worker)
    
    for announcement in minsBeforeAnnouncements.values():
        worker = MinsBeforeAnnouncementWorker(announcement.minsBefore, announcement.text)
        worker.start()
        workers.append(worker)

def update():
    # Terminate running workers, reset the workers array, recreate the workers
    for worker in workers:
        worker.terminate()
    
    globals()['workers'] = []
    start()

def formatTime(newTime):
    t = time.strptime(newTime, "%H:%M") # TODO Format this properly so seconds are removed
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)

def setBananaTime(time):
    app.logger.debug("Requested banana time " + time)
    timeAnnouncements['bananaTime'].time = formatTime(time)
    app.logger.info("New banana time set at " + str(timeAnnouncements['bananaTime'].time))

    update()

def setMorningAnnouncementTime(time):
    timeAnnouncements['morningAnnouncement'].time = formatTime(time)
    update() # TODO have this just restart the morning announcement worker

def addMinsBeforeAnnouncement(minsBefore, text):
    mins = int(minsBefore)

    if mins in minsBeforeAnnouncements:
        app.logger.warning("Cannot add new announcement as one already exists for " + str(mins) + " minutes before")
        # TODO Somehow alert the user of this
    else:
        minsBeforeAnnouncements[mins] = MinsBeforeAnnouncement(mins, text)

        worker = MinsBeforeAnnouncementWorker(mins, text)
        worker.start()
        workers.append(worker)

        app.logger.info("Added new announcement " + str(mins) + " minutes before banana time")

def removeMinsBeforeAnnouncement(minsBefore):
    minsBeforeAnnouncements.pop(int(minsBefore))
    app.logger.info("Removed announcement for " + str(minsBefore) + " minutes before banana time")

def setStatus(newStatus):
    status = newStatus
    if newStatus:
        app.logger.info("BananaBot is now Active")
    else:
        app.logger.info("BananaBot is now Inactive")


# Flask Routes
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',
        bananaTime = timeAnnouncements['bananaTime'].time,
        morningAnnouncementTime = timeAnnouncements['morningAnnouncement'].time,
        minsBeforeAnnouncements = minsBeforeAnnouncements,
        status = status)

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
            setStatus('status' in request.form)

        return redirect(url_for('admin'))

    return render_template('admin.html',
        bananaTime = timeAnnouncements['bananaTime'].time,
        morningAnnouncementTime = timeAnnouncements['morningAnnouncement'].time,
        minsBeforeAnnouncements = minsBeforeAnnouncements,
        status = status)


# Main
if __name__ == "__main__":
    start()
    app.run(host='0.0.0.0', port='8000', debug=True, use_reloader=False)