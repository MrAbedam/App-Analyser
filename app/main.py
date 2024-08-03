# project/app/main.py

from fastapi import FastAPI, HTTPException
from typing import List
from .schemas import Application
from . import crud
from .database import init_db, reset_db

app = FastAPI()


@app.post("/applications/", response_model=Application)
def create_application(app_data: Application):
    return crud.create_application(app_data)

@app.get("/applications/", response_model=List[Application])
def read_applications():
    return crud.read_applications()

@app.put("/applications/{app_id}", response_model=Application)
def update_application(app_id: int, app_data: Application):
    updated_app = crud.update_application(app_id, app_data)
    if updated_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated_app

@app.delete("/applications/{app_id}", response_model=Application)
def delete_application(app_id: int):
    deleted_app = crud.delete_application(app_id)
    if deleted_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return deleted_app

#TODO : FIX RESET AND INIT OF DB
#START
@app.on_event("startup")
def on_startup():
    init_db()
@app.post("/reset/")
def reset_database():
    reset_db()
    return {"detail": "Database reset and initialized with sample data"}
#END