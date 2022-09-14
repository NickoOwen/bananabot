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
# global appBananaTime
bananaTime = datetime.time(15, 30, 0)

# global morningAnnouncementTime
morningAnnouncementTime = datetime.time(10, 30, 0)

# global announcements
announcements = [
    MinsUntilAnnouncement(60, "60 mins test"),
    MinsUntilAnnouncement(30, "30 mins test")
]


# Define Logger Functions
logger = logging.getLogger('script_logger')

def log(err, msg) -> None:
    """Log messages that are parsed through the parameter
    
    Keyword arguments:
    err -- error message
    msg -- message to display
    """
    if err is not None:
        logger.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        logger.info("Message produced: %s" % (str(msg)))

def create_logger(logging_level):
    """Create the logger to use within the program
    
    Keyword arguments:
    logging_level -- level at which to log the message, i.e. DEBUG, INFO, WARN, ERROR.
    """
    logger.setLevel(logging_level)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'))
    logger.addHandler(handler)

create_logger(logging.DEBUG)


# Flask Routes
app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        formId = request.form['formId']
        logger.debug("Form ID: " + str(formId))

        if formId == 'bananaTime':
            setBananaTime(request.form['bananaTime'])
            logger.info("New banana time: " + str(bananaTime))
        elif formId == 'morningAnnouncementTime':
            setMorningAnnouncementTime(request.form['morningAnnouncementTime'])
            logger.info("New morning announcemenet time: " + str(morningAnnouncementTime))
        

        return redirect(url_for('home'))

    return render_template('index.html',
        bananaTime = bananaTime,
        morningAnnouncementTime = morningAnnouncementTime,
        announcements = announcements)

@app.route('/about')
def about():
    return render_template('about.html')


def setBananaTime(time):
    globals()['bananaTime'] = time
    # Probs need code here to update all minBefore announcements

def setMorningAnnouncementTime(time):
    globals()['morningAnnouncementTime'] = time


# Main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)