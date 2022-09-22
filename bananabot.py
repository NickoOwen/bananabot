import datetime
import time
import requests
import logging
from multiprocessing import Process
from flask import Flask, render_template, request, redirect, url_for

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
            time.sleep(10)
            # currentTime = datetime.datetime.now()
            # normalisedBananaTime = datetime.datetime.combine(datetime.date.today(), timeAnnouncements['bananaTime'].time)
            # # time_delta = normalisedBananaTime - currentTime
            # announcementTime = datetime.datetime.combine(datetime.date.today(), self.time)
            # sleepTime = announcementTime - currentTime
            # sleepTimeSeconds = sleepTime.seconds
            # print("Sleeping for " + str(sleepTimeSeconds))
            # time.sleep(sleepTimeSeconds)

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
            # time_delta = normalisedBananaTime - currentTime
            announcementTime = datetime.datetime.combine(datetime.date.today(), self.time)
            
            sleepTime = announcementTime - currentTime
            sleepTimeSeconds = sleepTime.seconds
            time.sleep(sleepTimeSeconds + 1)

            print(self.text)
            # Sleep until next day warning
            time.sleep(1) # This is a hacky way to make it work


# Banana Time Variables
workers = []

timeAnnouncements = {
    "morningAnnouncement": TimeAnnouncement(datetime.time(10, 0, 0), "1030 announ"),
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
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        # worker.daemon = True
        worker.start()
        workers.append(worker)
    
    for announcemenet in minsBeforeAnnouncements.values():
        worker = MinsBeforeAnnouncementWorker(announcemenet.minsBefore, announcemenet.text)
        
        worker.start()
        workers.append(worker)

def update():
    # Terminate running workers, reset the workers array, recreate the workers
    for worker in workers:
        worker.terminate()
    
    globals()['workers'] = []
    start()

def formatTime(newTime):
    t = time.strptime(newTime, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)

def setBananaTime(time):
    app.logger.debug("Requested banana time " + time)
    timeAnnouncements['bananaTime'].time = formatTime(time)
    app.logger.info("New banana time set at " + str(timeAnnouncements['bananaTime'].time))

    update()

def setMorningAnnouncementTime(time):
    timeAnnouncements['morningAnnouncement'].time = formatTime(time)
    update() # TODO have this just restart the morning announcement worker

def addMinsBeforeAnnouncement(minsBefore, message):
    mins = int(minsBefore)

    if mins in minsBeforeAnnouncements:
        app.logger.warning("Cannot add new announcement as one already exists for " + str(mins) + " minutes before")
        # TODO Somehow alert the user of this
    else:
        minsBeforeAnnouncements[mins] = MinsBeforeAnnouncement(mins, message)
        app.logger.info("Added new announcement " + str(mins) + " minutes before banana time")

def removeMinsBeforeAnnouncement(minsBefore):
    minsBeforeAnnouncements.pop(int(minsBefore))
    app.logger.info("Removed announcement for " + str(minsBefore) + " minutes before banana time")


# Flask Routes
app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        formId = request.form['formId']
        app.logger.debug("Form ID: " + str(formId))

        if formId == 'bananaTime':
            setBananaTime(request.form['bananaTime'])
            # app.logger.info("New banana time: " + str(request.form['bananaTime']))

        elif formId == 'morningAnnouncementTime':
            setMorningAnnouncementTime(request.form['morningAnnouncementTime'])
            # app.logger.info("New morning announcemenet time: " + str(morningAnnouncementTime))

        elif formId == 'announcement':
            addMinsBeforeAnnouncement(request.form['minsBefore'], request.form['message'])
        
        elif formId == 'deleteAnnouncement':
            removeMinsBeforeAnnouncement(request.form['minsBefore'])

        return redirect(url_for('home'))

    return render_template('index.html',
        bananaTime = timeAnnouncements['bananaTime'].time,
        morningAnnouncementTime = timeAnnouncements['morningAnnouncement'].time,
        minsBeforeAnnouncements = minsBeforeAnnouncements)

@app.route('/about')
def about():
    return render_template('about.html')


# Main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)