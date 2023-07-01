import datetime
from models import AppConfig, loadConfig, Announcement

# Test area
appData: AppConfig = loadConfig()
workers = {}

print("active: ", appData.active)
print("username: ", appData.username)
print("password: ", appData.password)
print("salt: ", appData.salt)

announcement: Announcement
for announcement in appData.announcements.values():
    print('id: ', announcement.id)
    print('type: ', announcement.type)
    print('text: ', announcement.text)
    print('time: ', announcement.time)
    print('mins_before: ', announcement.mins_before)


# ACTUAL REQUIRED CODE
from fastapi import FastAPI
from api import endpoints

# Load the config and set other app variables
appData: AppConfig = loadConfig()
workers = {}

    # if anything else needs to access these they import from main
    # All functionality is then called from endpoints.py
    # Making use of utilities

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(endpoints.router)
