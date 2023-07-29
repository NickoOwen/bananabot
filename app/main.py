from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import endpoints

app = FastAPI(docs_url=None, redoc_url=None)

# Import API endpoints and mount the static directory
app.include_router(endpoints.router)
app.mount("/static", StaticFiles(directory="static"), name="static")