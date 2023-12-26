from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from models import AppState
from api import endpoints
from utilities import initial_setup, stop

# Load the app
AppState.get_instance()
initial_setup()

app = FastAPI(docs_url=None, redoc_url=None)

# Import API endpoints and mount the static directory
app.include_router(endpoints.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Called after the app is closed to ensure any workers are stopped
@app.on_event("shutdown")
async def cleanup_tasks():
    stop()