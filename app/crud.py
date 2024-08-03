# project/app/crud.py

from typing import List
from .models import Application

db: List[Application] = []
current_id = 1
def create_application(app_data: Application) -> Application:
    global current_id
    app_data.id = current_id
    current_id += 1
    db.append(app_data)
    return app_data

def read_applications() -> List[Application]:
    return db

def update_application(app_id: int, app_data: Application) -> Application:
    for app in db:
        if app.id == app_id:
            app.name = app_data.name
            app.description = app_data.description
            return app
    return None

def delete_application(app_id: int) -> Application:
    for app in db:
        if app.id == app_id:
            db.remove(app)
            return app
    return None
