import secrets
import bcrypt

from fastapi import APIRouter
from fastapi import status, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models import AnnouncementData, BananaTimeData, SelectedDaysData, AppState
from utilities import toggle_status, update_banana_time, remove_announcement, add_announcement, update_banana_text, update_selected_days

router = APIRouter()
security = HTTPBasic()

templates = Jinja2Templates(directory="templates")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    app_state = AppState.get_instance()

    # Validate username
    current_username_bytes = credentials.username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, app_state.username
    )

    # Validate hashed passwords 
    current_password_bytes = bcrypt.hashpw(credentials.password.encode("utf8"), app_state.salt)
    is_correct_password = secrets.compare_digest(
        current_password_bytes, app_state.password
    )

    # Throw exception if credentials are incorrect
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


#### API Endpoints ####
@router.get("/favicon.ico", status_code=status.HTTP_200_OK)
async def get_favicon():
    return FileResponse("static/images/bb-transparent.png")


@router.get("/profile-picture", status_code=status.HTTP_200_OK)
async def get_profile_picture():
    return FileResponse("static/images/bb-white-background.png")


@router.get('/status', status_code=status.HTTP_200_OK)
def get_status(dependencies = Depends(get_current_user)):
    app_state = AppState.get_instance()
    return app_state.active


@router.post('/toggle-status', status_code=status.HTTP_200_OK)
def update_status(dependencies = Depends(get_current_user)):
    toggle_status()
    app_state = AppState.get_instance()
    return app_state.active


@router.get('/banana-time', status_code=status.HTTP_200_OK)
def get_banana_time():
    app_state = AppState.get_instance()
    return app_state.banana_time


@router.post('/banana-time', status_code=status.HTTP_200_OK)
def post_banana_time(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    # Check that time is set
    if(banana_time_data.time == None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No time was received with the data"
        )
    
    return update_banana_time(banana_time_data)


@router.get('/banana-text', status_code=status.HTTP_200_OK)
def get_banana_text():
    app_state = AppState.get_instance()
    return app_state.announcements['banana_time'].text


@router.post('/banana-text', status_code=status.HTTP_200_OK)
def post_banana_text(banana_time_data: BananaTimeData, dependencies = Depends(get_current_user)):
    # Check that text is set
    if(banana_time_data.text == None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No banana time text data was received"
        )
    
    return update_banana_text(banana_time_data)


@router.get('/selected-days', status_code=status.HTTP_200_OK)
def get_selected_days(dependencies = Depends(get_current_user)):
    app_state = AppState.get_instance()
    return app_state.selected_days


@router.post('/selected-days', status_code=status.HTTP_200_OK)
def post_selected_days(new_days: SelectedDaysData, dependencies = Depends(get_current_user)):
    return update_selected_days(new_days)


@router.get('/announcements')
def get_announcements(dependencies = Depends(get_current_user)):
    app_state = AppState.get_instance()
    return app_state.announcements


@router.post('/announcements', status_code=status.HTTP_201_CREATED)
def post_announcement(announcement: AnnouncementData, dependencies = Depends(get_current_user)):
    response = add_announcement(announcement)
    if (response == False):
        # Raise exception if the type is unknown
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unrecognised announcement type"
            )
    else:
        return response


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
    app_state: AppState = AppState.get_instance()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "banana_time": app_state.banana_time.strftime("%H:%M")
        })


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, dependencies = Depends(get_current_user)):
    app_state: AppState = AppState.get_instance()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "status": app_state.active,
        "selected_days": app_state.selected_days
    })
