import datetime
import time
import random
import string
import secrets
import bcrypt
import logging

from logging.config import fileConfig

from fastapi import FastAPI, status, Request, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from announcement import *

#### Setup Logger ####
fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


#### Banana Time Variables ####
announcements = {}  # Stores the announcements
workers = {}        # Stores the workers
active = False      # Stores the current status of the system (i.e. whether bananabot needs to send requests)

# Create the banana time announcement
banana_time_announcement = Announcement(datetime.time(15, 30, 0), "# @HERE Banana Time!")
banana_time_announcement.id = "banana_time"

# Create the default announcements
default_announcements = [
    banana_time_announcement,
    Announcement(datetime.time(10, 0, 0), "Banana time is at 15:30 today!"),
    MinsBeforeAnnouncement(60, "Banana time is in 60 minutes!"),
    MinsBeforeAnnouncement(30, "Banana time is in 30 minutes!"),
    MinsBeforeAnnouncement(10, "Banana time is in 10 minutes!")
]

# Add the default announcements to the announcements dictionary
for announcement in default_announcements:
    announcements[announcement.id] = announcement


#### Banana Time Functions ####
def start():
    """Creates all the workers using the data from announcements. Returns True if successful"""

    if workers:
        logger.warning("Found running workers when attempting to create workers. Expected 'workers' to be empty")
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
        logger.warning("Tried to stop workers when no workers exist")
        return False

    for key in workers:
        workers[key].terminate()
    
    workers = {}
    return True

def update():
    """Terminates and re-creates all workers so they are updated with the latest system changes"""
    
    if active:
        logger.debug("Updating workers...")
        stop()
        start()

def string_to_time(new_time):
    """Takes a string as input and returns a datetime.time object"""

    t = time.strptime(new_time, "%H:%M")
    return datetime.time(hour = t.tm_hour, minute = t.tm_min)

def set_banana_time(time):
    """Sets banana time"""

    logger.debug(f"Requested banana time: {time}")
    Announcement.banana_time = string_to_time(time)
    announcements['banana_time'].time = Announcement.banana_time    
    logger.info(f"New banana time set at {str(Announcement.banana_time)}")

    # Call update so any running workers can be updated
    update()

def set_banana_time_text(text):
    """Sets the text for the banana time announcement"""

    logger.info(f"Requested banana time text: {text}")
    announcements['banana_time'].text = text

    # Call update so any running workers can be updated
    update()
        
def add_time_announcement(time, text):
    """Adds a new announcement with the given time and text"""

    # logger.info(f"Adding new announcement for {time} with message: {text}")
    new_announcement = Announcement(string_to_time(time), text)
    announcements[new_announcement.id] = new_announcement

    if active:
        # logger.debug(f"Creating worker for new announcement with ID {new_announcement.id}")
        worker = AnnouncementWorker(new_announcement)
        workers[worker.id] = worker
        workers[worker.id].start()

    return new_announcement.id

def add_mins_before_announcement(mins_before, text):
    """Adds a new announcement for the given 'mins_before' banana time with the given text"""

    logger.info(f"Adding new announcement for {mins_before} minutes before banana time with message: {text}")
    mins_before = int(mins_before)

    new_announcement = MinsBeforeAnnouncement(mins_before, text)
    announcements[new_announcement.id] = new_announcement

    if active:
        logger.debug(f"Creating worker for new announcement with ID {new_announcement.id}")
        worker = MinsBeforeAnnouncementWorker(new_announcement)
        workers[worker.id] = worker
        workers[worker.id].start()

    return new_announcement.id

def instant_message(text):
    """Sends a new message instantly"""

    logger.info(f"Sending instant message with message: {text}")
    Announcement.send_message(text)

def remove_announcement(id):
    """Removes the announcement with the given id. Returns True if successful"""

    if id == 'banana_time':
        logger.warning("Attempted to remove banana_time announcement. This action is not permitted")
        return False
    
    if id not in announcements:
        logger.warning("Attempted to remove a non-existent announcement")
        return

    id = int(id)
    announcements.pop(id)

    if active:
        logger.info(f"Terminating worker with ID {str(id)}")
        workers[id].terminate()
        workers.pop(id)

    logger.info(f"Announcement with ID {str(id)} has been removed")
    return True

def toggle_status():
    """Toggles the status of the system (active). Returns the new value of active"""
    
    global active

    if not active:
        active = True
        start()
        logger.info("BananaBot is now ACTIVE")
    else:
        active = False
        stop()
        logger.info("BananaBot is now INACTIVE")
    
    return active

def update_selected_days(new_selected_days):
    """Updates the selected_days with new_selected_days"""

    logger.info(f"Updating selected days with: { new_selected_days }")

    # Update selected_days
    Announcement.selected_days = new_selected_days
    logger.info(f"Updated days: {str(Announcement.selected_days)}")
    
    # Call so any current workers can be updated
    update()


#### Authentication ####
security = HTTPBasic()

username = b"admin"
password = ""
salt = bcrypt.gensalt()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Validate username
    current_username_bytes = credentials.username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, username
    )

    # Validate hashed passwords 
    current_password_bytes = bcrypt.hashpw(credentials.password.encode("utf8"), salt)
    is_correct_password = secrets.compare_digest(
        current_password_bytes, password
    )

    # Throw exception if credentials are incorrect
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    

#### FastAPI Setup ####
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    global password

    # Generate random password and print it, then encode
    password = ''.join(random.choice(string.ascii_letters) for i in range(10))
    print(f"Admin Password: { password }")

    # Hash the password and store the hash
    password = bcrypt.hashpw(password.encode("utf8"), salt)


#### API Endpoints ####
@app.post('/toggle-status', status_code=status.HTTP_200_OK)
def update_status(dependencies = Depends(get_current_user)):
    return toggle_status()


@app.get('/banana-time', status_code=status.HTTP_200_OK)
def get_banana_time():
    return Announcement.banana_time


@app.post('/banana-time', status_code=status.HTTP_200_OK)
def post_banana_time(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    set_banana_time(banana_time_data.time)
    return Announcement.banana_time


@app.post('/banana-text', status_code=status.HTTP_200_OK)
def post_banana_text(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    set_banana_time_text(banana_time_data.text)
    return announcements['banana_time'].text


@app.get('/selected-days', status_code=status.HTTP_200_OK)
def get_selected_days(dependencies = Depends(get_current_user)):
    return Announcement.selected_days


@app.post('/selected-days', status_code=status.HTTP_200_OK)
def post_selected_days(new_days: SelectedDaysData, dependencies = Depends(get_current_user)):
    new_days = {
        "monday": new_days.monday == "on",
        "tuesday": new_days.tuesday == "on",
        "wednesday": new_days.wednesday == "on",
        "thursday": new_days.thursday == "on",
        "friday": new_days.friday == "on",
        "saturday": new_days.saturday == "on",
        "sunday": new_days.sunday == "on"
    }

    update_selected_days(new_days)
    return Announcement.selected_days


@app.get('/announcements')
def get_announcements(dependencies = Depends(get_current_user)):
    return announcements


@app.post('/announcements', status_code=status.HTTP_201_CREATED)
def post_announcements(announcement: AnnouncementData, dependencies = Depends(get_current_user)):
    match announcement.type:
        case 'time':
            return announcements[add_time_announcement(announcement.time, announcement.text)]
        case 'mins_before':
            return announcements[add_mins_before_announcement(announcement.mins_before, announcement.text)]
        case 'instant':
            Announcement.send_message(announcement.text)
            return
        
    # Raise exception if none of the above conditions were satisfied


@app.delete('/announcements/{announcement_id}', status_code=status.HTTP_200_OK)
def delete_announcement(announcement_id: int, dependencies = Depends(get_current_user)):
    remove_announcement(announcement_id)


#### Web Pages ####
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "banana_time": Announcement.banana_time.strftime("%H:%M")
        })


@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, dependencies = Depends(get_current_user)):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "announcements": announcements,
        "status": active,
        "selected_days": Announcement.selected_days
    })
