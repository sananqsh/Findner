from fastapi import FastAPI

from app.routes import api_router
from app.database import create_tables

app = FastAPI()

app.include_router(api_router)

# Server startup event
@app.on_event("startup")
def startup_event():
    create_tables()
