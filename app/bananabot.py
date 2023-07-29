import datetime
import time
import random
import string
import secrets
import bcrypt
import logging
import yaml
import os
from logging.config import fileConfig

from fastapi import FastAPI, status, Request, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from announcement import *

#### Setup Logger ####
fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


#### BananaBot Variables ####
announcements = {}  # Stores the announcements
workers = {}        # Stores the workers
active = False      # Stores the current status of the system (i.e. whether bananabot needs to send requests)

username = b"admin"
password = ""
salt = ""

state_file = './config/state.yaml'

# Register Announcement constructor with YAML parser
def announcement_constructor(loader, node):
    data = loader.construct_mapping(node)
    return Announcement(**data)

yaml.add_constructor('tag:yaml.org,2002:python/object:announcement.Announcement', announcement_constructor, Loader=yaml.SafeLoader)

def loadConfig():
    """Loads the saved configuration from the YAML file"""

    try:
        with open(state_file, 'r') as file:
            config = yaml.safe_load(file)

        if config is not None:
            global active, announcements, username, password, salt
            active = config.get('active', False)
            username = config.get('username', '')
            password = config.get('password', '')
            salt = config.get('salt', '')

            announcements_data = config.get('announcements', {})
            announcements = {}

            for announcement in announcements_data:
                text = announcement['text']
                time = datetime.datetime.strptime(announcement['time'], '%H:%M:%S').time() if announcement['time'] else None
                mins_before = announcement['mins_before'] if 'mins_before' in announcement else None

                announcement = Announcement(text, time=time, mins_before=mins_before)
                announcement.id = announcement['id']

                announcements[announcement.id] = announcement

            print('Config loaded successfully')
        else:
            print('No saved configuration found')

    except FileNotFoundError:
        print('No saved configuration found')
    except Exception as e:
        print('An error occurred while loading the configuration:', str(e))

def saveConfig():
    """Saves the current state of the app"""

    print('Saving config')

    # Serialise announcements
    yaml_announcements = []

    for announcement in announcements.values():
        yaml_announcements.append(serialiseAnnouncement(announcement))


    # Create a dictionary with the variables
    config = {
        'active': active,
        'announcements': yaml_announcements,
        'username': username,
        'password': password,
        'salt': salt
    }

    # Save the configuration to the YAML file
    with open(state_file, 'w') as file:
        yaml.dump(config, file)

#### Load State ####
# If app state is saved load it, otherwise setup with default state
if os.path.exists(state_file):
    # TODO load the state from state_file
    print("App state exists")
    loadConfig()
else:
    print("App state does not exist")
    # Create the banana time announcement
    banana_time_announcement = Announcement("@HERE Banana Time!", time=datetime.time(15, 30, 0))
    banana_time_announcement.id = "banana_time"

    # Create the default announcements
    default_announcements = [
        banana_time_announcement,
        Announcement("Banana time is at 15:30 today!", time=datetime.time(10, 0, 0)),
        Announcement("Banana time is in 60 minutes!", mins_before=60),
        Announcement("Banana time is in 30 minutes!", mins_before=30),
        Announcement("Banana time is in 10 minutes!", mins_before=10)
    ]

    # Add the default announcements to the announcements dictionary
    for announcement in default_announcements:
        announcements[announcement.id] = announcement

    # Generate credentials
    # password = ''.join(random.choice(string.ascii_letters) for i in range(10))
    password = '12345' # TODO make this random
    print(f'Admin Password: ', password)
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode("utf8"), salt)


    # Create the config directory if it doesn't exist
    os.makedirs(os.path.dirname('./config'), exist_ok=True)
    saveConfig()





#### Banana Time Functions ####
def start(): # done
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


def stop(): # done
    """Stop all running workers. Returns True if successful"""

    global workers

    # Check if the workers dictionary is empty
    if not workers:
        logger.warning("Tried to stop workers when no workers exist")
        return False

    for key in workers:
        workers[key].stop_event.set()
    
    workers = {}
    return True


def update(): # done
    """Stops and re-creates all workers so they are updated with the latest system changes"""
    
    if active:
        logger.debug("Updating workers...")
        stop()
        start()


def string_to_time(new_time): # done
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
    saveConfig()


def set_banana_time_text(text):
    """Sets the text for the banana time announcement"""

    logger.info(f"Requested banana time text: {text}")
    announcements['banana_time'].text = text

    # Call update so any running workers can be updated
    update()
        

def add_time_announcement(time, text):
    """Adds a new announcement with the given time and text"""

    logger.info(f"Adding new announcement for {time} with message: {text}")
    new_announcement = Announcement(string_to_time(time), text)
    announcements[new_announcement.id] = new_announcement

    if active:
        logger.debug(f"Creating worker for new announcement with ID {new_announcement.id}")
        worker = AnnouncementWorker(new_announcement)
        workers[worker.id] = worker
        workers[worker.id].start()

    saveConfig()
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
        logger.warning("Attempted to remove the banana time announcement. This action is not permitted")
        return False
    
    if id not in announcements:
        logger.warning("Attempted to remove a non-existent announcement")
        return False

    id = int(id)
    announcements.pop(id)

    if active:
        logger.info(f"Terminating worker with ID {str(id)}")
        workers[id].stop_event.set()
        workers.pop(id)

    logger.info(f"Announcement with ID {str(id)} has been removed")
    return True


def toggle_status(): # done
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


def update_selected_days(new_selected_days): # done
    """Updates the selected_days with new_selected_days"""

    logger.info(f"Updating selected days with: { new_selected_days }")

    # Update selected_days
    Announcement.selected_days = new_selected_days
    logger.debug(f"Updated days: {str(Announcement.selected_days)}")
    
    # Call so any current workers can be updated
    update()


#### Authentication ####
security = HTTPBasic()

# username = b"admin"
# password = ""
# salt = bcrypt.gensalt()

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
app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    global password

    # Generate random password and print it, then encode
    # password = ''.join(random.choice(string.ascii_letters) for i in range(10))
    # print(f"Admin Password: { password }")

    # Hash the password and store the hash
    # if password == '':
    #     password = bcrypt.hashpw(password.encode("utf8"), salt)


#### API Endpoints ####
@app.get("/favicon.ico", status_code=status.HTTP_200_OK)
async def get_favicon():
    return FileResponse("static/images/bb-transparent.png")


@app.get("/profile-picture", status_code=status.HTTP_200_OK)
async def get_profile_picture():
    return FileResponse("static/images/bb-white-background.png")


@app.get('/status', status_code=status.HTTP_200_OK)
def get_status(dependencies = Depends(get_current_user)):
    return active


@app.post('/toggle-status', status_code=status.HTTP_200_OK)
def update_status(dependencies = Depends(get_current_user)):
    return toggle_status()


@app.get('/banana-time', status_code=status.HTTP_200_OK)
def get_banana_time():
    return Announcement.banana_time


@app.post('/banana-time', status_code=status.HTTP_200_OK)
def post_banana_time(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    # Check that time is set
    if(banana_time_data.time == None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unrecognised announcement type"
        )
    
    set_banana_time(banana_time_data.time)
    return Announcement.banana_time


@app.get('/banana-text', status_code=status.HTTP_200_OK)
def get_banana_text():
    return announcements["banana_time"].text


@app.post('/banana-text', status_code=status.HTTP_200_OK)
def post_banana_text(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    # Check that text is set
    if(banana_time_data.text == None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unrecognised announcement type"
        )

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
        
    # Raise exception if the type is unknown
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unrecognised announcement type"
        )


@app.delete('/announcements/{announcement_id}', status_code=status.HTTP_200_OK)
def delete_announcement(announcement_id: int, dependencies = Depends(get_current_user)):
    if(remove_announcement(announcement_id) == False):
        # Raise exception if the type is unknown
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not remove announcement"
            )
    

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
async def get_healthcheck():
    return {"status": "healthy"}


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
        "status": active,
        "selected_days": Announcement.selected_days
    })
