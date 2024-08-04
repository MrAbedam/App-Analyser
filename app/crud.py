from typing import List
from .models import Application
import json
import os

DATA_PATH = "sample.json"


def load_db() -> List[Application]:
    """Load the database from the JSON file."""
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as infile:
                data = json.load(infile)
                return [Application(**item) for item in data]
        except Exception as e:
            print(f"Error loading database: {e}")
    return []


def save_db(db: List[Application]):
    """Save the database to the JSON file."""
    try:
        # Convert Application objects to dictionaries
        data = [app.__dict__ for app in db]
        with open(DATA_PATH, "w") as outfile:
            json.dump(data, outfile, indent=4)
    except Exception as e:
        print(f"Error saving database: {e}")

def create_application(app_data: Application) -> Application:
    db = load_db()
    current_id = max((app.id for app in db), default=1) + 1
    app_data.id = current_id
    db.append(app_data)
    save_db(db)
    return app_data

def read_applications() -> List[Application]:
    return load_db()

def update_application(app_id: int, app_data: Application) -> Application:
    db = load_db()
    for app in db:
        if app.id == app_id:
            app.name = app_data.name
            save_db(db)
            return app
    return None

def delete_application(app_id: int) -> Application:
    db = load_db()
    for app in db:
        if app.id == app_id:
            db.remove(app)
            save_db(db)
            return app
    return None
