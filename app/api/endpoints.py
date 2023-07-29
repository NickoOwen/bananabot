import secrets
import bcrypt

from fastapi import APIRouter
from fastapi import status, Request, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models import Announcement, AnnouncementData, BananaTimeData, SelectedDaysData, appState, saveConfig
from utilities import toggle_status, string_to_time, update, add_worker, remove_announcement

router = APIRouter()
security = HTTPBasic()

templates = Jinja2Templates(directory="templates")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Validate username
    current_username_bytes = credentials.username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, appState.username
    )

    # Validate hashed passwords 
    current_password_bytes = bcrypt.hashpw(credentials.password.encode("utf8"), appState.salt)
    is_correct_password = secrets.compare_digest(
        current_password_bytes, appState.password
    )

    # Throw exception if credentials are incorrect
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

# TODO remove if not needed
# @router.on_event("startup")
# def startup_event():
#     global password

    # Generate random password and print it, then encode
    # password = ''.join(random.choice(string.ascii_letters) for i in range(10))
    # print(f"Admin Password: { password }")

    # Hash the password and store the hash
    # if password == '':
    #     password = bcrypt.hashpw(password.encode("utf8"), salt)


#### API Endpoints ####
@router.get("/favicon.ico", status_code=status.HTTP_200_OK)
async def get_favicon():
    return FileResponse("static/images/bb-transparent.png")


@router.get("/profile-picture", status_code=status.HTTP_200_OK)
async def get_profile_picture():
    return FileResponse("static/images/bb-white-background.png")


@router.get('/status', status_code=status.HTTP_200_OK)
def get_status(dependencies = Depends(get_current_user)):
    return appState.active


@router.post('/toggle-status', status_code=status.HTTP_200_OK)
def update_status(dependencies = Depends(get_current_user)):
    return toggle_status()


@router.get('/banana-time', status_code=status.HTTP_200_OK)
def get_banana_time():
    return appState.banana_time


@router.post('/banana-time', status_code=status.HTTP_200_OK)
def post_banana_time(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    # Check that time is set
    if(banana_time_data.time == None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unrecognised announcement type"
        )
    
    appState.banana_time = string_to_time(banana_time_data.time)
    
    saveConfig(appState)
    return appState.banana_time


@router.get('/banana-text', status_code=status.HTTP_200_OK)
def get_banana_text():
    return appState.announcements['banana_time'].text


@router.post('/banana-text', status_code=status.HTTP_200_OK)
def post_banana_text(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    # Check that text is set
    if(banana_time_data.text == None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unrecognised announcement type"
        )

    appState.announcements['banana_time'].text = banana_time_data.text
    saveConfig(appState)
    return appState.announcements['banana_time'].text


@router.get('/selected-days', status_code=status.HTTP_200_OK)
def get_selected_days(dependencies = Depends(get_current_user)):
    return appState.selected_days


@router.post('/selected-days', status_code=status.HTTP_200_OK)
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

    appState.selected_days = new_days

    update()
    saveConfig(appState)
    return appState.selected_days


@router.get('/announcements')
def get_announcements(dependencies = Depends(get_current_user)):
    return appState.announcements


@router.post('/announcements', status_code=status.HTTP_201_CREATED)
def post_announcements(announcement: AnnouncementData, dependencies = Depends(get_current_user)):
    match announcement.type:
        case 'time':
            # Create the new announcement
            new_announcement = Announcement(announcement.text, time=string_to_time(announcement.time))
            appState.announcements[new_announcement.id] = new_announcement

            # Add a worker if the app is active
            if appState.active:
                add_worker(appState.announcements[new_announcement.id])

            return appState.announcements[new_announcement.id]
        case 'mins_before':
            # Create the new announcement
            new_announcement = Announcement(announcement.text, mins_before=announcement.mins_before)
            appState.announcements[new_announcement.id] = new_announcement

            # Add a worker if the app is active
            if appState.active:
                add_worker(appState.announcements[new_announcement.id])

            return appState.announcements[new_announcement.id]
        case 'instant':
            appState.send_message(announcement.text)
            return
        
    # Raise exception if the type is unknown
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unrecognised announcement type"
        )


@router.delete('/announcements/{announcement_id}', status_code=status.HTTP_200_OK)
def delete_announcement(announcement_id: str, dependencies = Depends(get_current_user)):
    if(remove_announcement(announcement_id) == False):
        # Raise exception if the type is unknown
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not remove announcement"
            )
    

@router.get('/healthcheck', status_code=status.HTTP_200_OK)
async def get_healthcheck():
    return {"status": "healthy"}


#### Web Pages ####
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print(f'appState: {appState}')
    return templates.TemplateResponse("index.html", {
        "request": request,
        "banana_time": appState.banana_time.strftime("%H:%M")
        })


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, dependencies = Depends(get_current_user)):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "status": appState.active,
        "selected_days": appState.selected_days
    })