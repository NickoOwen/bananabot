from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Loads all the app code
from api import endpoints
from utilities import initialSetup

# Call update to start workers if app is ACTIVE
initialSetup()

app = FastAPI(docs_url=None, redoc_url=None)

# Import API endpoints and mount the static directory
app.include_router(endpoints.router)
app.mount("/static", StaticFiles(directory="static"), name="static")