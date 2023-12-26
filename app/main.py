from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from models import AppState
from api import endpoints
from utilities import initial_setup

# Call get_instance to ensure config is loaded
AppState.get_instance()

# Call update to start workers if app is ACTIVE
initial_setup()

app = FastAPI(docs_url=None, redoc_url=None)

# Import API endpoints and mount the static directory
app.include_router(endpoints.router)
app.mount("/static", StaticFiles(directory="static"), name="static")