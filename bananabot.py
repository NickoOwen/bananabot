import datetime
import time
import requests
import logging
from flask import Flask, render_template, request, redirect, url_for

# Classes
class MinsUntilAnnouncement:
    def __init__(self, minsBefore, text):
        self.minsBefore = minsBefore
        self.text = text

class TimeAnnouncement:
    def __init__(self, time, text):
        self.time = time
        self.text = text


# Banana Time Variables
bananaTime = datetime.time(15, 30, 0)

morningAnnouncementTime = datetime.time(10, 30, 0)

announcements = {
    60: MinsUntilAnnouncement(60, "60 mins test"),
    30: MinsUntilAnnouncement(30, "30 mins test")
}


# Banana Time Functions
def setBananaTime(time):
    globals()['bananaTime'] = time
    # Probs need code here to update all minBefore announcements

def setMorningAnnouncementTime(time):
    globals()['morningAnnouncementTime'] = time

def addMinsBeforeAnnouncement(minsBefore, message):
    mins = int(minsBefore)
    if mins in announcements:
        app.logger.warning("Cannot add new announcement as one already exists for " + str(mins) + " minutes before")
        # TODO Somehow alert the user of this
    else:
        announcements[mins] = MinsUntilAnnouncement(mins, message)
        app.logger.info("Added new announcement " + str(mins) + " minutes before banana time")

def removeMinsBeforeAnnouncement(minsBefore):
    announcements.pop(int(minsBefore))
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
            app.logger.info("New banana time: " + str(bananaTime))

        elif formId == 'morningAnnouncementTime':
            setMorningAnnouncementTime(request.form['morningAnnouncementTime'])
            app.logger.info("New morning announcemenet time: " + str(morningAnnouncementTime))

        elif formId == 'announcement':
            addMinsBeforeAnnouncement(request.form['minsBefore'], request.form['message'])
        
        elif formId == 'deleteAnnouncement':
            removeMinsBeforeAnnouncement(request.form['minsBefore'])

        return redirect(url_for('home'))

    return render_template('index.html',
        bananaTime = bananaTime,
        morningAnnouncementTime = morningAnnouncementTime,
        announcements = announcements)

@app.route('/about')
def about():
    return render_template('about.html')


# Main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)